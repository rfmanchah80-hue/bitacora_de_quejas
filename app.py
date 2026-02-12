import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="SGI - Bitácora de Quejas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILO PERSONALIZADO (CSS)
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1e3a8a; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #1e3a8a; }
    .stButton>button {
        background-color: #1e3a8a;
        color: white;
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .stForm {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (MENU)
with st.sidebar:
    st.markdown("## **SGI** BITÁCORA QUEJAS")
    st.divider()
    menu = st.radio(
        "NAVEGACIÓN",
        ["📊 DASHBOARD", "📝 NUEVA QUEJA", "📂 BITÁCORA"],
        label_visibility="collapsed"
    )

# 4. LÓGICA DE PÁGINAS
if menu == "📊 DASHBOARD":
    st.title("RESUMEN EJECUTIVO")
    st.write("ESTADO DEL SISTEMA: 🟢 **SINCRONIZADO**")
    
    col_año = st.columns([1, 4])
    with col_año[0]:
        st.selectbox("AÑO:", [2024, 2025, 2026])

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("MES", "FEB")
    m2.metric("RECIBIDAS", "12")
    m3.metric("PROCEDENTES", "8")
    m4.metric("PROM. ATENCIÓN", "4.5 d")
    m5.metric("TONS. RECLAM", "450")
    m6.metric("TONS. ACEPT", "380")

    st.subheader("PROMEDIO TIEMPO DE ATENCIÓN (META 6 DÍAS)")
    st.info("Aquí se desplegará la gráfica de barras una vez conectada la BD.")

elif menu == "📝 NUEVA QUEJA":
    st.subheader("BITÁCORA DE QUEJAS EXTERNAS")
    st.caption("IDENTIFICACIÓN: AAC-FR-COR-001 | REVISIÓN: 03 | VIGENCIA: 07/02/2025")

    with st.form("form_queja"):
        c1, c2 = st.columns(2)
        folio = c1.text_input("🔢 FOLIO", value="001-2026")
        clasificacion = c2.selectbox("🏷️ CLASIFICACIÓN", ["CALIDAD", "SERVICIO"])

        t1, t2, t3, t4 = st.columns(4)
        f_recepcion = t1.date_input("📅 RECEPCIÓN", value=date.today())
        f_atencion = t2.date_input("📅 ATENCIÓN", value=None)
        f_informe = t3.date_input("📅 INFORME", value=None)
        f_cierre = t4.date_input("📅 CIERRE", value=None)
        
        # Cálculo de días TR si hay fechas
        dias_tr = (f_atencion - f_recepcion).days if f_atencion and f_recepcion else 0
        st.warning(f"Días TR Calculados: {dias_tr}")

        d1, d2, d3 = st.columns(3)
        cliente = d1.text_input("🏢 CLIENTE")
        zona = d2.selectbox("📍 ZONA", ["Norte", "Sur", "Centro", "Exportación"])
        asesor = d3.text_input("👤 ASESOR")

        d4, d5, d6, d7 = st.columns(4)
        defecto = d4.text_input("⚠️ DEFECTO")
        producto = d5.text_input("📦 PRODUCTO")
        caracteristicas = d6.text_input("🔍 CARACTERÍSTICAS")
        planta = d7.selectbox("🏭 PLANTA", ["108", "122", "124", "132"])

        f1, f2, f3, f4, f5 = st.columns(5)
        factura = f1.text_input("📄 FACTURA")
        medio = f2.selectbox("📞 MEDIO ATN", ["Correo", "Visita"])
        solucion = f3.selectbox("💡 SOLUCIÓN", ["Devolución", "Nota de Crédito", "No aplica"])
        doctos = f4.text_input("📑 DOCTOS", value="N/A")
        transporte = f5.text_input("🚛 TRANSPORTE", value="N/A")

        st.markdown("#### 📂 REPOSITORIO DE EVIDENCIAS")
        e1, e2, e3, e4 = st.columns(4)
        ev_alerta = e1.file_uploader("EMAIL ALERTA", type=['pdf', 'msg'])
        ev_notif = e2.file_uploader("EMAIL NOTIFICACIÓN", type=['pdf', 'msg'])
        ev_contesta = e3.file_uploader("EMAIL CONTESTACIÓN", type=['pdf', 'msg'])
        ev_informe = e4.file_uploader("EMAIL INFORME", type=['pdf', 'msg'])

        submit = st.form_submit_button("GUARDAR REGISTRO")
        
        if submit:
            st.success(f"Registro {folio} procesado localmente. Configure las credenciales para guardar en la nube.")

elif menu == "📂 BITÁCORA":
    st.header("CONSULTA DE QUEJAS")
    st.write("Visualización de la hoja 'quejas' de BDReportesQuejas.")
    # Espacio para st.dataframe(df)    
    
    try:
        # Crear la conexión usando los secretos que acabas de configurar
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Leer la pestaña 'quejas'
        df = conn.read(worksheet="quejas")
        
        # Mostrar la tabla con estilo profesional
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        st.info("Asegúrate de haber compartido el archivo con el correo de la cuenta de servicio.")
