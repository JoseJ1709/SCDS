# Código encargado del renderizado de páginas con Streamlit

# main.py

import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from Pantallas.Componentes.Boton import boton

# Importar funciones de interpolación
import Algoritmos.interpolacion.python.lagrange as lagrange
from Algoritmos.interpolacion.python.diferenciasdiv import newton_interpolation
from Algoritmos.interpolacion.python.trazadorescub import trazadores_cubicos_naturales, evaluar_spline

def load_global_styles():
    """Carga los estilos globales desde global.css"""
    css_path = Path(__file__).parent / "Pantallas" / "Estilos" / "global.css"

    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    css_boton = Path(__file__).parent / "Pantallas" / "Estilos" / "boton.css"

    with open(css_boton, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

st.set_page_config(
    page_title="Palma Africana - Monitor Térmico",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_global_styles()

# ============================================
# INICIALIZAR SESSION STATE
# ============================================

if 'accion_actual' not in st.session_state:
    st.session_state.accion_actual = None

if 'datos_procesados' not in st.session_state:
    st.session_state.datos_procesados = None

if 'datos_originales' not in st.session_state:
    # Datos por defecto
    st.session_state.datos_originales = pd.DataFrame({
        'Tiempo (min)': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
        'Temperatura (°C)': [22.1, 23.5, 25.8, 27.3, 28.9, 30.2, 29.8, 28.5, 26.7, 25.1, 23.8, 22.5]
    })

if 'punto_reconstruccion' not in st.session_state:
    st.session_state.punto_reconstruccion = None

if 'resultado_reconstruccion' not in st.session_state:
    st.session_state.resultado_reconstruccion = None


# ============================================
# FUNCIONES DE INTERPOLACIÓN
# ============================================

def interpolacion(xi, yi, x):
    """
    Aplica todos los métodos de interpolación a los datos dados.
    
    Parámetros:
    xi : array_like - Puntos x conocidos
    yi : array_like - Valores y conocidos en los puntos xi
    x : array_like - Puntos x donde se desea evaluar la interpolación
    
    Retorna:
    tuple : (yLagrange, yNewton, yTrazadorCubico)
    """
    # Interpolación de Lagrange
    yLagrange = lagrange.lagrange_interpolation(xi, yi, x)
    
    # Interpolación de Newton
    yNewton = newton_interpolation(xi, yi, x, None)
    
    # Trazadores cúbicos
    coef = trazadores_cubicos_naturales(xi, yi)
    yTrazadorCubico = evaluar_spline(xi, coef, x)

    return yLagrange, yNewton, yTrazadorCubico

def evaluar_precision(xi, yi):
    """
    Evalúa la precisión de los métodos de interpolación usando validación cruzada.
    
    Parámetros:
    xi : array_like - Puntos x conocidos
    yi : array_like - Valores y conocidos
    
    Retorna:
    str - Nombre del método más preciso
    """
    n = len(xi)
    errores = {'lagrange': [], 'newton': [], 'spline': []}

    for i in range(n):
        # Separar punto de prueba
        xTrain = xi[:i] + xi[i+1:]
        yTrain = yi[:i] + yi[i+1:]
        xTest = xi[i]
        yReal = yi[i]

        # Lagrange
        y_pred_l = lagrange.lagrange_interpolation(xTrain, yTrain, xTest)
        errores['lagrange'].append(abs(yReal - y_pred_l))

        # Newton
        y_pred_n = newton_interpolation(xTrain, yTrain, xTest)
        errores['newton'].append(abs(yReal - y_pred_n))

        # Spline
        coef = trazadores_cubicos_naturales(xTrain, yTrain)
        y_pred_s = evaluar_spline(xTrain, coef, xTest)
        errores['spline'].append(abs(yReal - y_pred_s))

    # Calcular error promedio (MAE)
    for metodo, e in errores.items():
        st.write(f"{metodo:10s} → Error medio: {np.mean(e):.15f}")

    # Método con menor error
    mejor = min(errores, key=lambda k: np.mean(errores[k]))
    return mejor


# ============================================
# FUNCIONES DE PROCESAMIENTO
# ============================================

def comparacion(datos):
    """Compara datos de temperatura usando interpolación"""
    st.success(f"✅ Comparando datos: {datos}")

    # Usar datos de la tabla
    df = st.session_state.datos_originales
    h = df['Tiempo (min)'].values.tolist()
    t_original = df['Temperatura (°C)'].values.tolist()

    # Generar puntos para interpolación
    h_interp = np.linspace(min(h), max(h), 100).tolist()
    
    try:
        # Aplicar todos los métodos de interpolación
        t_lagrange, t_newton, t_trazadores = interpolacion(h, t_original, h_interp)
        
        # Evaluar cuál método es más preciso
        mejor_metodo = evaluar_precision(h, t_original)
        
        st.success(f"🎯 **Método más preciso**: {mejor_metodo.upper()}")
        
        # Seleccionar los datos interpolados del mejor método
        if mejor_metodo == 'lagrange':
            t_mejor = t_lagrange
        elif mejor_metodo == 'newton':
            t_mejor = t_newton
        else:  # 'spline'
            t_mejor = t_trazadores

        st.session_state.accion_actual = 'comparacion'
        st.session_state.datos_procesados = {
            'tiempo': h,
            'tiempo_interp': h_interp,
            'original': t_original,
            'interpolado': t_mejor,
            'lagrange': t_lagrange,
            'newton': t_newton,
            'trazadores': t_trazadores,
            'mejor_metodo': mejor_metodo,
            'titulo': '📊 Comparación de Datos - Interpolación',
            'tipo': 'comparacion'
        }

        return {"status": "success", "accion": "comparacion", "mejor_metodo": mejor_metodo}

    except Exception as e:
        st.error(f"❌ Error en la interpolación: {str(e)}")
        # Fallback a interpolación lineal simple
        h_interp = np.linspace(min(h), max(h), 100)
        t_interpolado = np.interp(h_interp, h, t_original)
        
        st.session_state.accion_actual = 'comparacion'
        st.session_state.datos_procesados = {
            'tiempo': h,
            'tiempo_interp': h_interp.tolist(),
            'original': t_original,
            'interpolado': t_interpolado.tolist(),
            'mejor_metodo': 'lineal (fallback)',
            'titulo': '📊 Comparación de Datos - Interpolación Lineal',
            'tipo': 'comparacion'
        }
        
        return {"status": "warning", "accion": "comparacion", "mejor_metodo": "lineal"}


def reconstruccion(datos):
    """Reconstruye señal de temperatura usando interpolación"""
    st.success(f"✅ Reconstruyendo señal: {datos}")

    # Usar datos de la tabla 
    df = st.session_state.datos_originales
    h = df['Tiempo (min)'].values.tolist()
    t = df['Temperatura (°C)'].values.tolist()

    # Generar puntos para reconstrucción
    h_new = np.linspace(min(h), max(h), 200).tolist()
    
    try:
        # Aplicar todos los métodos de interpolación
        t_lagrange, t_newton, t_trazadores = interpolacion(h, t, h_new)
        
        # Evaluar cuál método es más preciso para reconstrucción
        mejor_metodo = evaluar_precision(h, t)
        
        st.success(f"🎯 **Método más preciso para reconstrucción**: {mejor_metodo.upper()}")
        
        # Seleccionar los datos reconstruidos del mejor método
        if mejor_metodo == 'lagrange':
            t_reconstruido = t_lagrange
        elif mejor_metodo == 'newton':
            t_reconstruido = t_newton
        else:  # 'spline'
            t_reconstruido = t_trazadores

        st.session_state.accion_actual = 'reconstruccion'
        st.session_state.datos_procesados = {
            'tiempo': h,
            'tiempo_recon': h_new,
            'temp': t,
            'temp_recon': t_reconstruido,
            'lagrange': t_lagrange,
            'newton': t_newton,
            'trazadores': t_trazadores,
            'mejor_metodo': mejor_metodo,
            'titulo': '🔄 Reconstrucción de Señal - Interpolación',
            'tipo': 'reconstruccion'
        }

        return {"status": "success", "accion": "reconstruccion", "mejor_metodo": mejor_metodo}

    except Exception as e:
        st.error(f"❌ Error en la reconstrucción por interpolación: {str(e)}")
        # Fallback a interpolación lineal simple de numpy
        h_new = np.linspace(min(h), max(h), 200)
        t_reconstruido = np.interp(h_new, h, t)
        
        st.session_state.accion_actual = 'reconstruccion'
        st.session_state.datos_procesados = {
            'tiempo': h,
            'tiempo_recon': h_new.tolist(),
            'temp': t,
            'temp_recon': t_reconstruido.tolist(),
            'mejor_metodo': 'lineal (fallback)',
            'titulo': '🔄 Reconstrucción de Señal - Interpolación Lineal',
            'tipo': 'reconstruccion'
        }
        
        return {"status": "warning", "accion": "reconstruccion", "mejor_metodo": "lineal"}


def generar_reconstruccion_punto():
    """Genera la reconstrucción para un punto específico"""
    if st.session_state.punto_reconstruccion is not None:
        try:
            df = st.session_state.datos_originales
            h = df['Tiempo (min)'].values.tolist()
            t = df['Temperatura (°C)'].values.tolist()
            
            punto = st.session_state.punto_reconstruccion
            
            # Aplicar interpolación al punto específico
            t_lagrange, t_newton, t_trazadores = interpolacion(h, t, [punto])
            
            # Obtener el mejor método
            mejor_metodo = st.session_state.datos_procesados.get('mejor_metodo', 'spline')
            
            # Seleccionar el resultado del mejor método
            if mejor_metodo == 'lagrange':
                resultado = t_lagrange[0]
            elif mejor_metodo == 'newton':
                resultado = t_newton[0]
            else:  # 'spline'
                resultado = t_trazadores[0]
            
            st.session_state.resultado_reconstruccion = {
                'punto': punto,
                'temperatura': resultado,
                'metodo': mejor_metodo,
                'todos_metodos': {
                    'lagrange': t_lagrange[0],
                    'newton': t_newton[0],
                    'spline': t_trazadores[0]
                }
            }
            
            st.success(f"✅ Reconstrucción generada para t = {punto} min")
            
        except Exception as e:
            st.error(f"❌ Error en la reconstrucción del punto: {str(e)}")


def analizar(datos):
    """Analiza temperatura y estrés térmico"""
    st.success(f"✅ Analizando temperatura: {datos}")

    # Usar datos de la tabla
    df = st.session_state.datos_originales
    h = df['Tiempo (min)'].values
    t = df['Temperatura (°C)'].values
    umbral = datos.get('umbral', 29.0)

    st.session_state.accion_actual = 'analisis'
    st.session_state.datos_procesados = {
        'tiempo': h,
        'temp': t,
        'umbral': umbral,
        'titulo': '🌡️ Análisis de Estrés Térmico',
        'tipo': 'analisis'
    }

    return {"status": "success", "accion": "analisis"}


def prediccion(datos):
    """Predice temperatura futura"""
    st.success(f"✅ Generando predicción: {datos}")

    # Usar datos de la tabla
    df = st.session_state.datos_originales
    h_historico = df['Tiempo (min)'].values
    t_historico = df['Temperatura (°C)'].values

    # Simular predicción simple (promedio móvil)
    ultimo_tiempo = h_historico[-1]
    h_futuro = np.array([ultimo_tiempo + 5, ultimo_tiempo + 10,
                         ultimo_tiempo + 15, ultimo_tiempo + 20])
    t_futuro = np.array([t_historico[-1] - 1, t_historico[-1] - 2,
                         t_historico[-1] - 3, t_historico[-1] - 3.5])

    st.session_state.accion_actual = 'prediccion'
    st.session_state.datos_procesados = {
        'tiempo_hist': h_historico,
        'temp_hist': t_historico,
        'tiempo_fut': h_futuro,
        'temp_fut': t_futuro,
        'titulo': '🪄 Predicción de Temperatura',
        'tipo': 'prediccion'
    }

    return {"status": "success", "accion": "prediccion"}


def exportar_datos(datos):
    """Exporta datos"""
    df = st.session_state.datos_originales
    csv = df.to_csv(index=False)

    st.success(f"✅ Exportando {len(df)} registros")
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"datos_temperatura_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    return {"status": "exported", "registros": len(df)}


def importar_datos(datos):
    """Importa datos desde archivo CSV"""
    st.info(f"📤 Importando datos desde archivo")

    uploaded = st.file_uploader("Selecciona archivo CSV", type=['csv'], key="uploader")

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)

            # Validar columnas
            if 'Tiempo (min)' in df.columns and 'Temperatura (°C)' in df.columns:
                st.session_state.datos_originales = df
                st.success(f"✅ Archivo cargado: {len(df)} registros")
                st.rerun()
            else:
                st.error("❌ El archivo debe tener columnas: 'Tiempo (min)' y 'Temperatura (°C)'")
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")

    return {"status": "waiting"}


def generar_reporte(datos):
    """Genera reporte PDF"""
    st.success(f"✅ Generando reporte en formato {datos.get('formato', 'PDF')}")
    st.balloons()

    # Aquí irían las funciones para generar PDF
    df = st.session_state.datos_originales
    st.info(f"📄 Reporte generado con {len(df)} registros")

    return {"status": "report_generated"}


# ============================================
# FUNCIÓN PARA RENDERIZAR GRÁFICAS
# ============================================

def renderizar_visualizacion():
    """Renderiza la visualización según la acción actual"""

    if st.session_state.accion_actual is None:
        st.markdown("""
            <div style="
                background: white;
                border-radius: 15px;
                padding: 4rem;
                text-align: center;
                border: 2px dashed #bdc3c7;
                min-height: 400px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                <h2 style="color: #95a5a6; margin-bottom: 1rem;">
                    📊 Contenedor de Visualización
                </h2>
                <p style="color: #7f8c8d; font-size: 1.1rem;">
                    Presiona un botón de operación para visualizar los resultados
                </p>
                <p style="color: #bdc3c7; font-size: 0.9rem; margin-top: 1rem;">
                    Comparación | Reconstrucción | Análisis | Predicción
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    datos = st.session_state.datos_procesados
    tipo = datos.get('tipo')

    st.markdown('<div class="contenedor-visualizacion">', unsafe_allow_html=True)
    st.markdown(f"### {datos.get('titulo', 'Visualización')}")

    fig = go.Figure()

    if tipo == 'comparacion':
        fig.add_trace(go.Scatter(
            x=datos['tiempo'],
            y=datos['original'],
            mode='markers',
            name='Datos Originales',
            marker=dict(size=10, color='#e74c3c')
        ))
        fig.add_trace(go.Scatter(
            x=datos['tiempo_interp'],
            y=datos['interpolado'],
            mode='lines',
            name=f'Interpolado ({datos.get("mejor_metodo", "lineal").upper()})',
            line=dict(color='#3498db', width=2)
        ))

    elif tipo == 'reconstruccion':
        fig.add_trace(go.Scatter(
            x=datos['tiempo'],
            y=datos['temp'],
            mode='markers',
            name='Puntos Originales',
            marker=dict(size=10, color='#e74c3c')
        ))
        fig.add_trace(go.Scatter(
            x=datos['tiempo_recon'],
            y=datos['temp_recon'],
            mode='lines',
            name='Señal Reconstruida',
            line=dict(color='#2ecc71', width=2)
        ))
        
        # Mostrar punto de reconstrucción específico si existe
        if st.session_state.resultado_reconstruccion is not None:
            punto = st.session_state.resultado_reconstruccion['punto']
            temperatura = st.session_state.resultado_reconstruccion['temperatura']
            metodo = st.session_state.resultado_reconstruccion['metodo']
            
            fig.add_trace(go.Scatter(
                x=[punto],
                y=[temperatura],
                mode='markers',
                name=f'Punto Reconstruido ({metodo.upper()})',
                marker=dict(size=15, color='#9b59b6', symbol='star'),
                hovertemplate=f'<b>Tiempo:</b> {punto} min<br><b>Temperatura:</b> {temperatura:.2f}°C<br><b>Método:</b> {metodo.upper()}<extra></extra>'
            ))

    elif tipo == 'analisis':
        fig.add_trace(go.Scatter(
            x=datos['tiempo'],
            y=datos['temp'],
            mode='lines+markers',
            name='Temperatura',
            line=dict(color='#3498db', width=2)
        ))
        fig.add_hline(
            y=datos['umbral'],
            line_dash="dash",
            line_color="#e74c3c",
            annotation_text=f"Umbral: {datos['umbral']}°C"
        )

    elif tipo == 'prediccion':
        fig.add_trace(go.Scatter(
            x=datos['tiempo_hist'],
            y=datos['temp_hist'],
            mode='lines+markers',
            name='Histórico',
            line=dict(color='#3498db', width=2),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=datos['tiempo_fut'],
            y=datos['temp_fut'],
            mode='lines+markers',
            name='Predicción',
            line=dict(color='#9b59b6', width=2, dash='dash'),
            marker=dict(size=8)
        ))

    fig.update_layout(
        xaxis_title="Tiempo (minutos)",
        yaxis_title="Temperatura (°C)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Mostrar información adicional para reconstrucción
    if tipo == 'reconstruccion':
        mostrar_panel_reconstruccion()

    col1, col2, col3 = st.columns(3)

    if tipo in ['comparacion', 'reconstruccion', 'analisis']:
        with col1:
            temp_max = np.max(datos.get('temp', datos.get('original', [0])))
            st.metric("🌡️ Temp. Máxima", f"{temp_max:.2f}°C")

        with col2:
            temp_min = np.min(datos.get('temp', datos.get('original', [0])))
            st.metric("❄️ Temp. Mínima", f"{temp_min:.2f}°C")

        with col3:
            temp_avg = np.mean(datos.get('temp', datos.get('original', [0])))
            st.metric("📊 Promedio", f"{temp_avg:.2f}°C")

    st.markdown('</div>', unsafe_allow_html=True)


def mostrar_panel_reconstruccion():
    """Muestra el panel para reconstrucción de puntos específicos"""
    st.markdown("---")
    st.markdown("### 🔍 Reconstrucción de Punto Específico")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input para el punto a reconstruir
        tiempo_min = st.session_state.datos_originales['Tiempo (min)'].min()
        tiempo_max = st.session_state.datos_originales['Tiempo (min)'].max()
        
        punto = st.number_input(
            "Ingrese el tiempo (min) para reconstruir:",
            min_value=float(tiempo_min),
            max_value=float(tiempo_max),
            value=float((tiempo_min + tiempo_max) / 2),
            step=1.0,
            format="%.1f",
            key="input_punto_reconstruccion"
        )
        
        st.session_state.punto_reconstruccion = punto
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Generar Reconstrucción", use_container_width=True):
            generar_reconstruccion_punto()
    
    # Mostrar resultados si existen
    if st.session_state.resultado_reconstruccion is not None:
        resultado = st.session_state.resultado_reconstruccion
        st.success(f"**Resultado de la reconstrucción:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "⏱️ Tiempo", 
                f"{resultado['punto']} min"
            )
        
        with col2:
            st.metric(
                "🌡️ Temperatura Reconstruida", 
                f"{resultado['temperatura']:.2f}°C"
            )
        
        with col3:
            st.metric(
                "⚙️ Método", 
                resultado['metodo'].upper()
            )
        
        # Mostrar comparación de todos los métodos
        with st.expander("📊 Comparación de Métodos"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lagrange", f"{resultado['todos_metodos']['lagrange']:.4f}°C")
            with col2:
                st.metric("Newton", f"{resultado['todos_metodos']['newton']:.4f}°C")
            with col3:
                st.metric("Spline", f"{resultado['todos_metodos']['spline']:.4f}°C")


# ============================================
# FUNCIÓN PARA RENDERIZAR TABLA DE DATOS
# ============================================

def renderizar_tabla_datos():
    """Renderiza la tabla editable de datos"""

    st.markdown('<div class="contenedor-tabla">', unsafe_allow_html=True)

    st.markdown("### 📋 Datos de Temperatura")

    col_info, col_acciones = st.columns([7, 3])

    with col_info:
        st.markdown(f"""
            <p style="color: #7f8c8d; margin-bottom: 1rem;">
                Total de registros: <strong>{len(st.session_state.datos_originales)}</strong> | 
                Rango: <strong>{st.session_state.datos_originales['Tiempo (min)'].min():.0f} - {st.session_state.datos_originales['Tiempo (min)'].max():.0f} min</strong>
            </p>
        """, unsafe_allow_html=True)

    with col_acciones:
        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("➕ Agregar Fila", use_container_width=True):
                nueva_fila = pd.DataFrame({
                    'Tiempo (min)': [0.0],
                    'Temperatura (°C)': [0.0]
                })
                st.session_state.datos_originales = pd.concat(
                    [st.session_state.datos_originales, nueva_fila],
                    ignore_index=True
                )
                st.rerun()

        with col_btn2:
            if st.button("🗑️ Limpiar Todo", use_container_width=True):
                st.session_state.datos_originales = pd.DataFrame({
                    'Tiempo (min)': [],
                    'Temperatura (°C)': []
                })
                st.rerun()

    # Editor de datos
    df_editado = st.data_editor(
        st.session_state.datos_originales,
        use_container_width=True,
        num_rows="dynamic",  # Permite agregar/eliminar filas
        column_config={
            "Tiempo (min)": st.column_config.NumberColumn(
                "⏱️ Tiempo (min)",
                help="Tiempo en minutos",
                min_value=0,
                max_value=1000,
                step=1,
                format="%.1f"
            ),
            "Temperatura (°C)": st.column_config.NumberColumn(
                "🌡️ Temperatura (°C)",
                help="Temperatura en grados Celsius",
                min_value=-50,
                max_value=100,
                step=0.1,
                format="%.2f"
            ),
        },
        hide_index=False,
        key="editor_datos"
    )

    # Actualizar session_state si hubo cambios
    if not df_editado.equals(st.session_state.datos_originales):
        st.session_state.datos_originales = df_editado
        st.success("✅ Datos actualizados correctamente")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# MAIN
# ============================================

def main():
    """Función principal"""

    st.markdown("""
        <h1 style="text-align: center; margin-bottom: 0.5rem;">
            🌴 Sistema de Análisis Térmico
        </h1>
    """, unsafe_allow_html=True)

    # ========== FILA DE BOTONES ==========
    Operaciones, col_botones_rojos = st.columns([6, 4], gap="medium")

    with Operaciones:
        st.markdown("<h4 style='text-align: center;'>📊 Panel de Operaciones</h4>", unsafe_allow_html=True)
        subcol1, subcol2, subcol3, subcol4 = st.columns(4)

        with subcol1:
            if st.button("📊 Comparación", key="btn_comparacion", type="primary", use_container_width=True):
                comparacion({"metodo": "interpolacion"})

        with subcol2:
            if st.button("🔄 Reconstrucción", key="btn_reconstruccion", type="primary", use_container_width=True):
                reconstruccion({"puntos": 200})
                # Limpiar resultado anterior al generar nueva reconstrucción
                st.session_state.resultado_reconstruccion = None

        with subcol3:
            if st.button("🌡️ Analizar", key="btn_analizar", type="primary", use_container_width=True):
                analizar({"umbral": 29.0})

        with subcol4:
            if st.button("🪄 Predicción", key="btn_prediccion", type="primary", use_container_width=True):
                prediccion({"horizonte": 30})

    with col_botones_rojos:
        st.markdown("<h4 style='text-align: center;'> ⚠️ Acciones </h4>", unsafe_allow_html=True)
        subcol5, subcol6, subcol7 = st.columns(3)

        with subcol5:
            if st.button("📦 Exportar", key="btn_exportar", type="secondary", use_container_width=True):
                exportar_datos({"formato": "csv"})

        with subcol6:
            if st.button("🚀 Importar", key="btn_importar", type="secondary", use_container_width=True):
                importar_datos({"tipo": "csv"})

        with subcol7:
            if st.button("📄 Reporte", key="btn_reporte", type="secondary", use_container_width=True):
                generar_reporte({"formato": "pdf"})

    st.markdown("<br>", unsafe_allow_html=True)

    # ========== CONTENEDOR DE VISUALIZACIÓN ==========
    renderizar_visualizacion()

    st.markdown("<br>", unsafe_allow_html=True)

    # ========== TABLA DE DATOS ==========
    renderizar_tabla_datos()


if __name__ == "__main__":
    main()