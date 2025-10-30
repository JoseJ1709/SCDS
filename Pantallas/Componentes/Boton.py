# Pantallas/Componentes/Boton.py

import streamlit as st
from pathlib import Path


def cargar_estilos():
    css_path = Path(__file__).parent.parent / "Estilos" / "boton.css"

    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def boton(funcion, nombre_btn="Ejecutar", datos=None, tipo="primary"):
    if tipo == "primary":
        clicked = st.button(
            nombre_btn,
            key=f"btn_{nombre_btn}_{id(funcion)}",
            type="primary"
        )
    else:
        clicked = st.button(
            nombre_btn,
            key=f"btn_{nombre_btn}_{id(funcion)}",
            type="secondary"
        )

    if clicked:
        if datos is not None:
            resultado = funcion(datos)
        else:
            resultado = funcion()

        return resultado

    return None