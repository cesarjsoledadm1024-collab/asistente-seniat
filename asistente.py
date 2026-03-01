import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Asistente Virtual SENIAT",
    page_icon="🏛️",
    layout="centered"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #003366;
        }
        .stChatMessage {
            background-color: #004080;
            border-radius: 10px;
            padding: 10px;
        }
        .stChatInput input {
            background-color: #004080;
            color: white;
            border: 2px solid #FFD700;
            border-radius: 10px;
        }
        h1 {
            color: #FFD700 !important;
            text-align: center;
        }
        .stCaption {
            color: #FFD700 !important;
            text-align: center;
        }
        section[data-testid="stSidebar"] {
            background-color: #002244;
        }
        .stChatMessage p {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🏛️ Asistente Virtual SENIAT")
st.caption("Atención al contribuyente - Consultas tributarias")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

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
                    Atiendes a los contribuyentes con información clara, precisa y amable sobre los siguientes temas:
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
