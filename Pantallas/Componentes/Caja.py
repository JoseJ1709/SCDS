import streamlit as st
from pathlib import Path

def cargar_estilos():
    """Carga los estilos CSS del header"""
    css_path = Path(__file__).parent.parent / "Estilos" / "caja.css"

    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def cargar_caja():
    cargar_estilos()
    caja = st.container()
    with caja:
        st.markdown('<div class="caja1">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
