import streamlit as st
from groq import Groq
from datetime import datetime

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

# Pestañas
tab1, tab2, tab3 = st.tabs(["💬 Asistente", "🧮 Calculadora", "📅 Fechas de Declaración"])

with tab3:
    st.markdown("## 📅 Fechas de Declaración")
    st.markdown("---")

    hoy = datetime.now()
    mes_actual = hoy.month
    año_actual = hoy.year

    st.markdown(f"### 📆 Hoy es: {hoy.strftime('%d/%m/%Y')}")
    st.markdown("---")

    tipo = st.selectbox(
        "Selecciona el tipo de contribuyente:",
        ["Contribuyente Ordinario", "Contribuyente Especial"]
    )

    if tipo == "Contribuyente Ordinario":
        st.markdown("### 📌 Fechas para Contribuyentes Ordinarios")

        st.info("""
        **🔵 IVA - Declaración Mensual**
        - Se declara dentro de los **15 días hábiles** del mes siguiente
        - Ejemplo: IVA de Enero → declarar antes del 20 de Febrero aproximadamente
        """)

        st.info("""
        **🔵 ISLR - Declaración Anual**
        - Personas Naturales: **hasta el 31 de Marzo** de cada año
        - Personas Jurídicas: **dentro de los 3 meses** después del cierre del ejercicio fiscal
        """)

        st.warning("""
        **⚠️ Retenciones de IVA**
        - Se enteran los días **lunes y martes** de cada semana
        - Según el último dígito del RIF
        """)

    else:
        st.markdown("### 📌 Fechas para Contribuyentes Especiales")

        st.info("""
        **🔴 IVA - Declaración Quincenal**
        - Primera quincena (días 1-15): declarar entre los días **16 y 20** del mismo mes
        - Segunda quincena (días 16-31): declarar entre los días **1 y 5** del mes siguiente
        """)

        st.info("""
        **🔴 Retenciones de IVA**
        - Se enteran según el **último dígito del RIF**:
        
        | Último dígito RIF | Día de enteramiento |
        |---|---|
        | 0 y 1 | Lunes |
        | 2 y 3 | Martes |
        | 4 y 5 | Miércoles |
        | 6 y 7 | Jueves |
        | 8 y 9 | Viernes |
        """)

        st.info("""
        **🔴 ISLR - Declaración Anual**
        - Personas Naturales: **hasta el 31 de Marzo**
        - Personas Jurídicas: **dentro de los 3 meses** del cierre fiscal
        """)

    st.markdown("---")
    st.error("""
    **⚠️ Consecuencias por declarar fuera de tiempo:**
    - Multa por retraso: 10 Unidades Tributarias por cada mes de retraso
    - Intereses moratorios sobre el monto adeudado
    - Posible cierre temporal del establecimiento
    """)

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #FFD700;'>
    Para consultar el calendario oficial actualizado visita:<br>
    🌐 <b>www.seniat.gob.ve</b>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("## 🧮 Calculadora Tributaria")
    st.markdown("---")

    calc_tipo = st.selectbox(
        "Selecciona el impuesto a calcular:",
        ["IVA (16%)", "Retención de IVA 75%", "Retención de IVA 100%", "ISLR (estimado)"]
    )

    monto = st.number_input(
        "Ingresa el monto en Bolívares (Bs):",
        min_value=0.0,
        format="%.2f"
    )

    if st.button("🔢 Calcular"):
        if monto > 0:
            if calc_tipo == "IVA (16%)":
                impuesto = monto * 0.16
                total = monto + impuesto
                st.success(f"""
                **Resultado:**
                - 💰 Monto base: Bs. {monto:,.2f}
                - 📊 IVA (16%): Bs. {impuesto:,.2f}
                - 💵 Total a pagar: Bs. {total:,.2f}
                """)
            elif calc_tipo == "Retención de IVA 75%":
                iva = monto * 0.16
                retencion = iva * 0.75
                pagar = iva - retencion
                st.success(f"""
                **Resultado:**
                - 💰 Monto base: Bs. {monto:,.2f}
                - 📊 IVA (16%): Bs. {iva:,.2f}
                - ✂️ Retención (75%): Bs. {retencion:,.2f}
                - 💵 IVA a pagar: Bs. {pagar:,.2f}
                """)
            elif calc_tipo == "Retención de IVA 100%":
                iva = monto * 0.16
                st.success(f"""
                **Resultado:**
                - 💰 Monto base: Bs. {monto:,.2f}
                - 📊 IVA (16%): Bs. {iva:,.2f}
                - ✂️ Retención (100%): Bs. {iva:,.2f}
                - 💵 IVA a pagar: Bs. 0.00
                """)
            elif calc_tipo == "ISLR (estimado)":
                if monto <= 1000:
                    tasa = 0.06
                elif monto <= 1500:
                    tasa = 0.09
                elif monto <= 2000:
                    tasa = 0.12
                elif monto <= 2500:
                    tasa = 0.16
                elif monto <= 3000:
                    tasa = 0.20
                else:
                    tasa = 0.34
                islr = monto * tasa
                st.success(f"""
                **Resultado estimado:**
                - 💰 Monto anual: Bs. {monto:,.2f}
                - 📊 Tasa aplicada: {tasa*100:.0f}%
                - 💵 ISLR estimado: Bs. {islr:,.2f}
                """)
                st.info("⚠️ Este es un cálculo estimado. Consulte con un especialista tributario.")
        else:
            st.warning("⚠️ Por favor ingresa un monto mayor a 0")

with tab1:
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        bienvenida = """¡Bienvenido al Asistente Virtual del SENIAT! 🏛️

Estoy aquí para ayudarle con sus consultas tributarias. Puede preguntarme sobre:

✅ Registro de RIF  ✅ Declaraciones de IVA e ISLR  ✅ Retenciones
✅ Contribuyentes Especiales  ✅ Solvencia Tributaria  ✅ Sanciones y Recursos

¿En qué le puedo ayudar hoy?"""
        st.session_state.mensajes.append({"role": "assistant", "content": bienvenida})

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

    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

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

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFD700;'>
    🏛️ <b>SENIAT</b> - Servicio Nacional Integrado de Administración Aduanera y Tributaria<br>
    📞 0800-SENIAT (736428) | 🌐 www.seniat.gob.ve<br>
    📍 Venezuela
</div>
""", unsafe_allow_html=True)
