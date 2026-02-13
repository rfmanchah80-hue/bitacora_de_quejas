import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
st.set_page_config(page_title="SGI - Bitácora de Quejas", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .header-box { background-color: #f0f2f6; padding: 10px; border-radius: 10px; border-left: 5px solid #1e3a8a; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado oficial según tu referencia
st.markdown("""
    <div class="header-box">
        <h3 style='margin:0;'>BITÁCORA DE QUEJAS EXTERNAS</h3>
        <p style='margin:0; font-size:12px;'>AAC-FR-COR-001 | Rev. 03 | Vig. 07/02/2025 | Calidad Campo</p>
    </div>
    """, unsafe_allow_html=True)

# 2. NAVEGACIÓN LATERAL
with st.sidebar:
    menu = st.radio("MENÚ PRINCIPAL", ["📊 KPI's", "📝 NUEVO REGISTRO", "📂 BITÁCORA"])

# 3. LÓGICA DE PÁGINAS
if menu == "📊 KPI's":
    st.subheader("Dashboard de Rendimiento")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MES", "FEB")
    m2.metric("RECIBIDAS", "15")
    m3.metric("PROCEDENTES", "10")
    m4.metric("META ATENCIÓN", "6 Días")
    st.info("Gráficos de Mapeo y Tendencias se visualizarán aquí.")

elif menu == "📝 NUEVO REGISTRO":
    # Sistema de pasos según tu presentación
    if 'step' not in st.session_state: st.session_state.step = 1

    if st.session_state.step == 1:
        st.markdown("#### Paso 1: Datos Generales")
        with st.container():
            c1, c2 = st.columns(2)
            folio = c1.text_input("Folio", value="001-2026")
            planta = c2.selectbox("Planta", ["108", "122", "124", "132"])
            if st.button("Continuar →"): st.session_state.step = 2

    elif st.session_state.step == 2:
        st.markdown("#### Paso 2: Calidad y Mapeo")
        col_m, col_n = st.columns(2)
        mapeo_si = col_m.radio("¿Requiere Mapeo?", ["No", "Si"])
        
        if mapeo_si == "Si":
            num_mapeos = col_n.number_input("N° de mapeos (Máx 11)", min_value=1, max_value=11, value=1)
            for i in range(int(num_mapeos)):
                st.file_uploader(f"Insertar imagen de mapeo {i+1}", type=['jpg', 'png'])
        
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("← Atrás"): st.session_state.step = 1
        if col_btn2.button("Finalizar y Guardar"):
            st.success("Registro Guardado Exitosamente")
            st.session_state.step = 1

elif menu == "📂 BITÁCORA":
    st.subheader("Histórico de Quejas")
    # Conexión real (usando tus Secrets configurados)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="quejas")
        st.dataframe(df, use_container_width=True)
    except:
        st.warning("Conecta tus Secrets para ver los datos reales.")
