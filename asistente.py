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
        footer { color: #FFD700 !important; text-align: center; }
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

# Mensaje de bienvenida automático
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    with st.chat_message("assistant"):
        bienvenida = """¡Bienvenido al Asistente Virtual del SENIAT! 🏛️

Estoy aquí para ayudarle con sus consultas tributarias. Puede preguntarme sobre:

✅ Registro de RIF
✅ Declaraciones de IVA e ISLR
✅ Retenciones
✅ Contribuyentes Especiales
✅ Solvencia Tributaria
✅ Sanciones y Recursos
✅ Facturación Fiscal

¿En qué le puedo ayudar hoy?"""
        st.write(bienvenida)
        st.session_state.mensajes.append({
            "role": "assistant",
            "content": bienvenida
        })

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if pregunta := st.chat_input("¿En qué le podemos ayudar?"):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un asistente virtual oficial del SENIAT (Servicio Nacional Integrado de Administración Aduanera y Tributaria de Venezuela).
                    Atiendes a los contribuyentes con información clara, precisa y amable sobre:
                    - Registro de RIF
                    - Declaraciones de IVA e ISLR
                    - Retenciones de IVA e ISLR
                    - Contribuyentes especiales
                    - Solvencia tributaria
                    - Sanciones y recursos tributarios
                    - Facturación fiscal
                    - Trámites en línea
                    Responde siempre en español, de forma clara, ordenada y amable.
                    Si no conoces la respuesta con certeza, indica al contribuyente que se dirija a la oficina del SENIAT más cercana o al portal oficial www.seniat.gob.ve"""
                }
            ] + st.session_state.mensajes
        )
        texto = respuesta.choices[0].message.content
        st.write(texto)
        st.session_state.mensajes.append({"role": "assistant", "content": texto})

# Pie de página
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFD700;'>
    🏛️ <b>SENIAT</b> - Servicio Nacional Integrado de Administración Aduanera y Tributaria<br>
    📞 0800-SENIAT (736428) | 🌐 www.seniat.gob.ve<br>
    📍 Venezuela
</div>
""", unsafe_allow_html=True)
