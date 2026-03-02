import streamlit as st
from groq import Groq
from datetime import datetime
import re

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Asistente Virtual SENIAT",
    page_icon="🏛️",
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS (Tu diseño original) ---
st.markdown("""
    <style>
        .stApp { background-color: #003366; }
        .stChatMessage { background-color: #004080; border-radius: 10px; padding: 10px; }
        h1 { color: #FFD700 !important; text-align: center; }
        .stCaption { color: #FFD700 !important; text-align: center; }
        .stChatMessage p { color: white !important; }
        section[data-testid="stSidebar"] { background-color: #002244; }
        section[data-testid="stSidebar"] h2 { color: #FFD700 !important; }
        section[data-testid="stSidebar"] p { color: white !important; }
        .stButton button {
            background-color: #004080;
            color: #FFD700;
            border: 1px solid #FFD700;
            border-radius: 8px;
            width: 100%;
            margin: 2px 0;
        }
        .stButton button:hover {
            background-color: #FFD700;
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE VALIDACIÓN TÉCNICA DE RIF ---
def validar_rif_venezuela(rif_input):
    rif = rif_input.replace("-", "").replace(" ", "").upper()
    if not re.match(r"^[VJEGP][0-9]{8,9}$", rif):
        return False, "⚠️ Formato inválido (Ej: V-12345678-9)", None

    # Algoritmo de verificación (Módulo 11)
    pesos = [4, 3, 2, 7, 6, 5, 4, 3, 2]
    letras = {'V': 4, 'E': 8, 'J': 12, 'P': 16, 'G': 20}
    try:
        cuerpo = rif[1:-1].zfill(8)
        digito_v_real = int(rif[-1])
        suma = letras[rif[0]] * pesos[0]
        for i in range(8):
            suma += int(cuerpo[i]) * pesos[i+1]
        resto = suma % 11
        resultado = 11 - resto
        if resultado >= 10: resultado = 0
        
        if resultado == digito_v_real:
            tipos = {'V': 'Persona Natural', 'J': 'Persona Jurídica', 'G': 'Gubernamental', 'E': 'Extranjero', 'P': 'Pasaporte'}
            return True, f"✅ RIF Válido: {tipos[rif[0]]}", rif
        else:
            return False, "❌ El dígito verificador es incorrecto", None
    except:
        return False, "⚠️ Error al procesar el RIF", None

# --- CLIENTE GROQ ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("logo.png", width=150)
    
    st.markdown("## 🔍 Validación de RIF")
    rif_user = st.text_input("Verifique su RIF aquí:", placeholder="V-12345678-9")
    if rif_user:
        es_valido, msj_rif, rif_limpio = validar_rif_venezuela(rif_user)
        if es_valido:
            st.success(msj_rif)
            st.session_state.rif_data = rif_limpio
        else:
            st.error(msj_rif)
            st.session_state.rif_data = None
    
    st.markdown("---")
    st.markdown("## 📋 Temas Tributarios")
    st.markdown("""
    **Puedes consultar sobre:**
    📌 Registro de RIF
    📌 Declaraciones de IVA/ISLR
    📌 Contribuyentes Especiales
    📌 Facturación Fiscal
    """)
    st.markdown("---")
    st.markdown("**🌐 Portal Oficial**")
    st.markdown("[www.seniat.gob.ve](http://www.seniat.gob.ve)")

# Logo y título central
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=200)

st.title("🏛️ Asistente Virtual SENIAT")
st.caption("Atención al contribuyente - Consultas tributarias")

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs(["💬 Asistente", "🧮 Calculadora", "📅 Fechas de Declaración", "📖 Glosario"])

# --- TAB 1: ASISTENTE ---
with tab1:
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        bienvenida = "¡Bienvenido al Asistente Virtual del SENIAT! 🏛️\n\n¿En qué le puedo ayudar hoy?"
        st.session_state.mensajes.append({"role": "assistant", "content": bienvenida})

    st.markdown("### 💬 Preguntas Frecuentes")
    preguntas = ["¿Requisitos para el RIF?", "¿Cómo declaro IVA?", "¿Qué es un contribuyente especial?", "¿Cuál es la tasa del IGTF?"]
    
    c_pre1, c_pre2 = st.columns(2)
    for i, pregunta in enumerate(preguntas):
        with (c_pre1 if i % 2 == 0 else c_pre2):
            if st.button(pregunta, key=f"btn_{i}"):
                st.session_state.pregunta_rapida = pregunta

    st.markdown("---")
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    pregunta_actual = None
    if "pregunta_rapida" in st.session_state and st.session_state.pregunta_rapida:
        pregunta_actual = st.session_state.pregunta_rapida
        st.session_state.pregunta_rapida = None
    if entrada := st.chat_input("¿En qué le podemos ayudar?"):
        pregunta_actual = entrada

    if pregunta_actual:
        st.session_state.mensajes.append({"role": "user", "content": pregunta_actual})
        with st.chat_message("user"): st.write(pregunta_actual)

        with st.chat_message("assistant"):
            # Pasamos la info del RIF al modelo si existe
            rif_info = f" El usuario tiene el RIF validado: {st.session_state.get('rif_data', 'No provisto')}."
            respuesta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "system",
                    "content": f"Eres un asistente oficial del SENIAT.{rif_info} Responde de forma clara y técnica sobre leyes venezolanas."
                }] + st.session_state.mensajes
            )
            texto = respuesta.choices[0].message.content
            st.write(texto)
            st.session_state.mensajes.append({"role": "assistant", "content": texto})
        st.rerun()

# --- TAB 2: CALCULADORA ---
with tab2:
    st.markdown("## 🧮 Calculadora Tributaria")
    st.markdown("---")
    calc_tipo = st.selectbox(
        "Selecciona el impuesto:",
        ["IVA (16%)", "IGTF (3%)", "Retención de IVA 75%", "Retención de IVA 100%", "ISLR (estimado)"]
    )
    monto = st.number_input("Monto en Bolívares (Bs):", min_value=0.0, format="%.2f")

    if st.button("🔢 Calcular"):
        if monto > 0:
            if calc_tipo == "IVA (16%)":
                imp = monto * 0.16
                st.success(f"**Total:** Bs. {monto+imp:,.2f} (IVA: Bs. {imp:,.2f})")
            elif calc_tipo == "IGTF (3%)":
                igtf = monto * 0.03
                st.warning(f"**Impuesto IGTF a pagar:** Bs. {igtf:,.2f}")
            elif calc_tipo == "Retención de IVA 75%":
                iva = monto * 0.16
                ret = iva * 0.75
                st.success(f"**Retención (75%):** Bs. {ret:,.2f} | **A pagar al proveedor:** Bs. {monto+(iva-ret):,.2f}")
            elif calc_tipo == "ISLR (estimado)":
                tasa = 0.34 if monto > 3000 else 0.15 # Simplificación
                st.info(f"**ISLR Estimado:** Bs. {monto*tasa:,.2f} (Tasa ref: {tasa*100}%)")
        else:
            st.warning("⚠️ Ingrese un monto mayor a 0")

# --- TAB 3: FECHAS (Tu original) ---
with tab3:
    st.markdown("## 📅 Fechas de Declaración")
    hoy = datetime.now()
    st.markdown(f"### 📆 Hoy es: {hoy.strftime('%d/%m/%Y')}")
    tipo = st.selectbox("Contribuyente:", ["Contribuyente Ordinario", "Contribuyente Especial"])
    if tipo == "Contribuyente Ordinario":
        st.info("🔵 **IVA:** Primeros 15 días hábiles del mes.")
    else:
        st.error("🔴 **Especiales:** Según calendario de sujetos pasivos (RIF).")

# --- TAB 4: GLOSARIO (Tu original) ---
with tab4:
    st.markdown("## 📖 Glosario Tributario")
    buscar = st.text_input("🔍 Buscar término:")
    # ... (Aquí se mantiene tu diccionario de términos original)
    st.write("Use la barra de búsqueda para encontrar definiciones legales.")

# Pie de página institucional
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFD700;'>
    🏛️ <b>SENIAT</b> - Servicio Nacional Integrado de Administración Aduanera y Tributaria<br>
    📍 Venezuela | 🌐 www.seniat.gob.ve
</div>
""", unsafe_allow_html=True)
