import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# 1. CONFIGURACIÓN DE PÁGINA Y SEGURIDAD
st.set_page_config(page_title="Auditoría Fiscal 2025", page_icon="🔒", layout="wide")

USUARIOS_AUTORIZADOS = {"admin": "admin123"}

# 2. EL SÚPER-PROMPT MAESTRO (El Cerebro)
SUPER_PROMPT = """
Eres un Auditor Fiscal y Contable Senior (normativa española 2025). Tu objetivo es cruzar todos los documentos que suba el usuario para optimizar su factura fiscal y calcular el Impuesto sobre Sociedades.
REGLA DE ORO: NO INVENTES DATOS. Si falta algo, pon 'N/D'. Usa formato europeo (1.250,50 €).
Al recibir la instrucción 'ANALIZAR', genera ESTRICTAMENTE 5 módulos:
MÓDULO 1: DASHBOARD DE SALUD FINANCIERA (Liquidez, Endeudamiento, ROA, ROE con iconos ✅⚠️❌).
MÓDULO 2: INFORME EJECUTIVO Y ESTRATEGIA FISCAL (Diagnóstico y ahorro).
MÓDULO 3: TABLA DE AUDITORÍA Y ACCIÓN HUMANA (Hallazgo, Fórmula, Impacto Fiscal, Asiento Contable).
MÓDULO 4: ESQUEMA DE LIQUIDACIÓN MODELO 200 (Tabla completa desde Resultado Contable hasta Cuota Diferencial).
MÓDULO 5: BLOQUE CSV DESCARGABLE (Con las fórmulas y resultados).
"""

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# --- PANTALLA DE LOGIN ---
if not st.session_state.autenticado:
    st.title("🔒 Acceso Restringido")
    with st.container():
        usuario = st.text_input("👤 Usuario")
        clave = st.text_input("🔑 Contraseña", type="password")
        if st.button("Entrar al Sistema"):
            if usuario in USUARIOS_AUTORIZADOS and USUARIOS_AUTORIZADOS[usuario] == clave:
                st.session_state.autenticado = True
                st.session_state.usuario_actual = usuario
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
else:
    # --- PANTALLA PRINCIPAL ---
    st.sidebar.success(f"✅ Conectado como: **{st.session_state.usuario_actual}**")
    
    # AQUÍ ESTÁ LA CAJA PARA TU LLAVE (Seguro y privado)
    api_key = st.sidebar.text_input("🔑 Pega tu API Key de Google aquí:", type="password")
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🏛️ Software de Auditoría e Ingeniería Fiscal 2025")
    st.markdown("Sube tus documentos (PDF, CSV, JPG) y el motor cruzará los datos.")
    st.divider()

    # Subida múltiple de archivos
    archivos_subidos = st.file_uploader("Arrastra aquí Balance, PyG, Modelo 200, etc.", accept_multiple_files=True)

    if st.button("🚀 COMENZAR ANÁLISIS", type="primary", use_container_width=True):
        if not api_key:
            st.error("⚠️ Faltan las llaves del motor. Pega tu API Key en el menú de la izquierda.")
        elif not archivos_subidos:
            st.warning("⚠️ Debes subir al menos un documento para empezar.")
        else:
            try:
                # Conectar con Google Gemini
                genai.configure(api_key=api_key)
                modelo = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=SUPER_PROMPT)
                
                with st.spinner('Analizando contabilidad, aplicando normativa 2025 y generando tablas... (Puede tardar hasta 1 minuto)'):
                    
                    archivos_para_gemini = []
                    
                    # Truco para que Gemini lea los archivos desde Streamlit
                    for archivo in archivos_subidos:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=archivo.name) as tmp_file:
                            tmp_file.write(archivo.getvalue())
                            ruta_temp = tmp_file.name
                        
                        # Subir a la memoria de Google
                        archivo_g = genai.upload_file(ruta_temp)
                        archivos_para_gemini.append(archivo_g)
                    
                    # La orden final a la IA
                    instruccion = ["ANALIZAR"] + archivos_para_gemini
                    respuesta = modelo.generate_content(instruccion)
                    
                    st.success("¡Análisis Completado con Éxito!")
                    st.divider()
                    
                    # IMPRIMIR EL RESULTADO REAL
                    st.markdown(respuesta.text)

            except Exception as e:
                st.error(f"❌ Ha ocurrido un error de conexión: {e}")
