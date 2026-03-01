import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Asistente Virtual SENIAT",
    page_icon="🏛️",
    layout="wide"
)

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

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Menú lateral
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("## 📋 Temas Tributarios")
    st.markdown("""
    **Puedes consultar sobre:**
    
    📌 Registro de RIF
    
    📌 Declaraciones de IVA
    
    📌 Declaraciones de ISLR
    
    📌 Retenciones de IVA e ISLR
    
    📌 Contribuyentes Especiales
    
    📌 Solvencia Tributaria
    
    📌 Sanciones y Recursos
    
    📌 Facturación Fiscal
    
    📌 Trámites en Línea
    """)
    st.markdown("---")
    st.markdown("**🌐 Portal Oficial**")
    st.markdown("[www.seniat.gob.ve](http://www.seniat.gob.ve)")

# Logo y título
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=200)

st.title("🏛️ Asistente Virtual SENIAT")
st.caption("Atención al contribuyente - Consultas tributarias")

# Inicializar mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    bienvenida = """¡Bienvenido al Asistente Virtual del SENIAT! 🏛️

Estoy aquí para ayudarle con sus consultas tributarias. Puede preguntarme sobre:

✅ Registro de RIF  ✅ Declaraciones de IVA e ISLR  ✅ Retenciones
✅ Contribuyentes Especiales  ✅ Solvencia Tributaria  ✅ Sanciones y Recursos

¿En qué le puedo ayudar hoy?"""
    st.session_state.mensajes.append({"role": "assistant", "content": bienvenida})

# Preguntas frecuentes
st.markdown("### 💬 Preguntas Frecuentes")
preguntas = [
    "¿Cuáles son los requisitos para obtener el RIF?",
    "¿Cómo declaro el IVA en el portal del SENIAT?",
    "¿Cuándo vence la declaración de ISLR?",
    "¿Qué es un contribuyente especial?",
    "¿Cómo obtengo la solvencia tributaria?",
    "¿Cuáles son las sanciones por no declarar a tiempo?",
    "¿Cómo recupero mi clave del portal SENIAT?",
    "¿Cuál es el porcentaje del IVA en Venezuela?",
]

col1, col2 = st.columns(2)
for i, pregunta in enumerate(preguntas):
    if i % 2 == 0:
        with col1:
            if st.button(pregunta, key=f"btn_{i}"):
                st.session_state.pregunta_rapida = pregunta
    else:
        with col2:
            if st.button(pregunta, key=f"btn_{i}"):
                st.session_state.pregunta_rapida = pregunta

st.markdown("---")

# Mostrar mensajes
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Procesar pregunta rápida o escrita
pregunta_actual = None

if "pregunta_rapida" in st.session_state and st.session_state.pregunta_rapida:
    pregunta_actual = st.session_state.pregunta_rapida
    st.session_state.pregunta_rapida = None

if entrada := st.chat_input("¿En qué le podemos ayudar?"):
    pregunta_actual = entrada

if pregunta_actual:
    st.session_state.mensajes.append({"role": "user", "content": pregunta_actual})
    with st.chat_message("user"):
        st.write(pregunta_actual)

    with st.chat_message("assistant"):
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un asistente virtual oficial del SENIAT (Venezuela).
                    Atiendes contribuyentes con información sobre:
                    - Registro de RIF
                    - Declaraciones de IVA e ISLR
                    - Retenciones de IVA e ISLR
                    - Contribuyentes especiales
                    - Solvencia tributaria
                    - Sanciones y recursos tributarios
                    - Facturación fiscal
                    - Trámites en línea
                    Responde en español, de forma clara y amable.
                    Si no estás seguro, indica al contribuyente que visite www.seniat.gob.ve"""
                }
            ] + st.session_state.mensajes
        )
        texto = respuesta.choices[0].message.content
        st.write(texto)
        st.session_state.mensajes.append({"role": "assistant", "content": texto})
    st.rerun()

# Pie de página
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFD700;'>
    🏛️ <b>SENIAT</b> - Servicio Nacional Integrado de Administración Aduanera y Tributaria<br>
    📞 0800-SENIAT (736428) | 🌐 www.seniat.gob.ve<br>
    📍 Venezuela
</div>
""", unsafe_allow_html=True)
