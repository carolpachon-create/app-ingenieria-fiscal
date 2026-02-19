import streamlit as st
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Auditoría Fiscal 2025", page_icon="🔒", layout="wide")

# 2. BASE DE DATOS DE USUARIOS (Solo el administrador)
USUARIOS_AUTORIZADOS = {
    "admin": "admin123"
}

# 3. SISTEMA DE SEGURIDAD (Estado de la sesión)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# --- PANTALLA DE LOGIN (La puerta blindada) ---
if not st.session_state.autenticado:
    st.title("🔒 Acceso Restringido")
    st.markdown("Por favor, identifícate para acceder al motor de Ingeniería Fiscal.")
    
    with st.container():
        usuario = st.text_input("👤 Usuario")
        clave = st.text_input("🔑 Contraseña", type="password")
        
        if st.button("Entrar al Sistema"):
            if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario] == clave:
                st.session_state.autenticado = True
                st.session_state.usuario_actual = usuario
                st.success("Acceso concedido. Cargando motor fiscal...")
                time.sleep(1)
                st.rerun() # Refresca la página para entrar
            else:
                st.error("❌ Credenciales incorrectas. Acceso denegado.")

# --- PANTALLA PRINCIPAL (El Salón de la App) ---
else:
    # Menú lateral para cerrar sesión
    st.sidebar.success(f"✅ Conectado como: **{st.session_state.usuario_actual}**")
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🏛️ Software de Auditoría e Ingeniería Fiscal 2025")
    st.markdown("Sube los documentos contables. El sistema acepta PDF, Excel, CSV e imágenes.")
    st.divider()

    # Botones de subida de archivos
    col1, col2, col3 = st.columns(3)
    with col1:
        archivo_balance = st.file_uploader("1. Balance / PyG", type=['csv', 'pdf', 'xlsx'])
    with col2:
        archivo_sumas = st.file_uploader("2. Sumas y Saldos", type=['csv', 'pdf'])
    with col3:
        archivo_otros = st.file_uploader("3. Modelo 200 / Otros", type=['pdf', 'jpg'])

    st.divider()

    # El botón mágico
    if st.button("🚀 COMENZAR ANÁLISIS", type="primary", use_container_width=True):
        if not archivo_balance and not archivo_sumas and not archivo_otros:
            st.warning("⚠️ Debes subir al menos un documento para empezar.")
        else:
            with st.spinner('Analizando contabilidad y cruzando normativa fiscal 2025...'):
                time.sleep(3) # Simulamos el tiempo de espera de la IA
                
                st.success("¡Análisis completado!")
                
                # --- AQUÍ VA EL RESULTADO BONITO ---
                st.header("📊 Módulo 1: Dashboard de Salud Financiera")
                m1, m2, m3 = st.columns(3)
                m1.metric("Liquidez General", "1.85 ✅", "Óptimo")
                m2.metric("Endeudamiento", "45% ✅", "Sano")
                m3.metric("ROA (Económica)", "12% 🚀", "("💡 **Conclusión:** La empresa presenta una estructura financiera muy sólida, sin riesgo de quiebra a corto plazo y con una excelente rentabilidad sobre sus activos.")
