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
    st.markdown("""
    <style>
      css = """
<style>
.stApp { background-color: #003366; }
.stChatMessage { background-color: #004080; border-radius: 15px; padding: 15px; border-left: 3px solid #FFD700; margin: 5px 0; }
h1 { color: #FFD700 !important; text-align: center; }
h2, h3 { color: #FFD700 !important; }
.stCaption { color: #FFD700 !important; text-align: center; }
.stChatMessage p { color: white !important; }
section[data-testid="stSidebar"] { background-color: #002244; border-right: 2px solid #FFD700; }
section[data-testid="stSidebar"] h2 { color: #FFD700 !important; }
section[data-testid="stSidebar"] p { color: white !important; }
.stButton button { background-color: #004080; color: #FFD700; border: 1px solid #FFD700; border-radius: 10px; width: 100%; margin: 3px 0; font-weight: bold; }
.stButton button:hover { background-color: #FFD700; color: #003366; }
.stTabs [data-baseweb="tab-list"] { background-color: #002244; border-radius: 10px; padding: 5px; }
.stTabs [data-baseweb="tab"] { color: #FFD700 !important; font-weight: bold; }
.stTabs [aria-selected="true"] { background-color: #004080 !important; border-radius: 8px; }
div[data-testid="stExpander"] { background-color: rgba(0,64,128,0.5); border: 1px solid #FFD700; border-radius: 10px; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)
""", unsafe_allow_html=True)
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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Asistente", "🧮 Calculadora", "📅 Fechas de Declaración", "📖 Glosario", "📋 Guías de Trámites"])

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
# Botón limpiar chat
col_limpiar = st.columns([4, 1])
with col_limpiar[1]:
    if st.button("🗑️ Limpiar chat"):
        st.session_state.mensajes = []
        st.rerun()
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
with tab4:
    st.markdown("## 📖 Glosario Tributario SENIAT")
    st.markdown("---")

    buscar = st.text_input("🔍 Buscar término:", placeholder="Escribe un término tributario...")

    terminos = {
        "IVA": "**Impuesto al Valor Agregado (IVA):** Impuesto indirecto que grava la venta de bienes y prestación de servicios. En Venezuela la tasa general es del 16%.",
        "ISLR": "**Impuesto Sobre la Renta (ISLR):** Impuesto directo que grava los enriquecimientos netos obtenidos por personas naturales y jurídicas durante el año fiscal.",
        "RIF": "**Registro de Información Fiscal (RIF):** Documento que identifica a las personas naturales y jurídicas ante el SENIAT para el cumplimiento de obligaciones tributarias.",
        "Contribuyente": "**Contribuyente:** Persona natural o jurídica obligada al pago de tributos por realizar actividades económicas gravadas por la ley.",
        "Contribuyente Especial": "**Contribuyente Especial:** Persona natural o jurídica calificada por el SENIAT por su alto nivel de ingresos o actividad económica. Tiene obligaciones adicionales.",
        "Contribuyente Ordinario": "**Contribuyente Ordinario:** Persona natural o jurídica que realiza actividades gravadas con IVA sin ser calificada como especial.",
        "Retención": "**Retención:** Mecanismo por el cual el comprador o pagador descuenta un porcentaje del impuesto al momento del pago y lo entera al SENIAT.",
        "Agente de Retención": "**Agente de Retención:** Persona o entidad designada por el SENIAT para retener impuestos a otros contribuyentes y enterarlos al fisco.",
        "Enteramiento": "**Enteramiento:** Acto de depositar o pagar al SENIAT los impuestos retenidos o recaudados dentro del plazo establecido.",
        "Débito Fiscal": "**Débito Fiscal:** IVA que el vendedor cobra al comprador en cada operación de venta. Representa el impuesto que se debe al fisco.",
        "Crédito Fiscal": "**Crédito Fiscal:** IVA pagado por el contribuyente en sus compras. Se puede deducir del débito fiscal para calcular el IVA a pagar.",
        "Solvencia Tributaria": "**Solvencia Tributaria:** Documento emitido por el SENIAT que certifica que el contribuyente está al día con sus obligaciones tributarias.",
        "Declaración Sustitutiva": "**Declaración Sustitutiva:** Nueva declaración que reemplaza una declaración anterior cuando se detectan errores u omisiones.",
        "Unidad Tributaria": "**Unidad Tributaria (UT):** Valor en bolívares establecido por el SENIAT para calcular multas, sanciones y algunos impuestos.",
        "Ejercicio Fiscal": "**Ejercicio Fiscal:** Período de 12 meses utilizado para calcular y declarar impuestos. Puede coincidir o no con el año calendario.",
        "Factura Fiscal": "**Factura Fiscal:** Documento que certifica una operación comercial y debe cumplir con los requisitos establecidos por el SENIAT.",
        "Recurso Jerárquico": "**Recurso Jerárquico:** Mecanismo legal para impugnar actos administrativos del SENIAT ante un superior jerárquico dentro de la misma institución.",
        "SENIAT": "**SENIAT:** Servicio Nacional Integrado de Administración Aduanera y Tributaria. Organismo del Estado venezolano encargado de recaudar los tributos nacionales.",
        "Timbre Fiscal": "**Timbre Fiscal:** Impuesto que se paga por la realización de ciertos actos jurídicos o administrativos ante organismos públicos.",
        "Alícuota": "**Alícuota:** Porcentaje o tasa que se aplica sobre la base imponible para calcular el monto del impuesto a pagar.",
    }

    if buscar:
        resultados = {k: v for k, v in terminos.items() if buscar.upper() in k.upper() or buscar.lower() in v.lower()}
        if resultados:
            for termino, definicion in resultados.items():
                st.info(definicion)
        else:
            st.warning(f"No se encontró ningún término relacionado con '{buscar}'")
    else:
        for termino, definicion in sorted(terminos.items()):
            with st.expander(f"📌 {termino}"):
                st.write(definicion)
with tab5:
    st.markdown("## 🔍 Consulta y Verificación de RIF")
    st.markdown("---")

    st.markdown("""
    El RIF (Registro de Información Fiscal) tiene el siguiente formato:
    
    | Tipo | Formato | Ejemplo |
    |------|---------|---------|
    | Persona Natural | V-XXXXXXXX-X | V-12345678-9 |
    | Persona Jurídica | J-XXXXXXXX-X | J-12345678-9 |
    | Gobierno | G-XXXXXXXX-X | G-20004036-0 |
    | Extranjero | E-XXXXXXXX-X | E-12345678-9 |
    | Pasaporte | P-XXXXXXXX-X | P-12345678-9 |
    """)

    st.markdown("---")
    st.markdown("### ✅ Verificar formato de RIF")

    rif = st.text_input(
        "Ingresa el RIF a verificar:",
        placeholder="Ejemplo: V-12345678-9",
        max_chars=13
    ).upper().strip()

    if st.button("🔍 Verificar RIF"):
        if rif:
            import re
            patron = r'^[VJGEP]-\d{8}-\d$'
            if re.match(patron, rif):
                tipo_rif = {
                    "V": "Persona Natural Venezolana",
                    "J": "Persona Jurídica",
                    "G": "Organismo Gubernamental",
                    "E": "Persona Natural Extranjera",
                    "P": "Persona con Pasaporte"
                }
                letra = rif[0]
                st.success(f"""
                ✅ **El formato del RIF es VÁLIDO**
                
                - 📋 RIF: **{rif}**
                - 👤 Tipo: **{tipo_rif.get(letra, 'Desconocido')}**
                - 🔤 Prefijo: **{letra}**
                """)
                st.info("""
                ℹ️ **Nota:** Esta herramienta solo verifica el **formato** del RIF.
                Para verificar si el RIF está activo y registrado, visita:
                🌐 **www.seniat.gob.ve → Consulta de RIF**
                """)
            else:
                st.error(f"""
                ❌ **El formato del RIF no es válido**
                
                El RIF debe tener el formato: **X-XXXXXXXX-X**
                
                Donde X es:
                - Primera letra: V, J, G, E o P
                - Luego un guión (-)
                - 8 números
                - Otro guión (-)
                - 1 número final
                
                Ejemplo correcto: **V-12345678-9**
                """)
        else:
            st.warning("⚠️ Por favor ingresa un RIF para verificar")

    st.markdown("---")
    st.markdown("### 📋 ¿Cómo obtener tu RIF?")
    with st.expander("Ver pasos para obtener el RIF"):
        st.markdown("""
        **Personas Naturales:**
        1. Ingresa a **www.seniat.gob.ve**
        2. Selecciona **"Registro de Contribuyentes"**
        3. Completa el formulario con tus datos
        4. Presenta la cédula de identidad en la oficina del SENIAT
        5. Recibe tu RIF en el momento
        
        **Personas Jurídicas:**
        1. Ingresa a **www.seniat.gob.ve**
        2. Selecciona **"Registro de Contribuyentes"**
        3. Completa el formulario con los datos de la empresa
        4. Presenta los documentos en la oficina del SENIAT:
           - Acta constitutiva
           - RIF del representante legal
           - Comprobante de domicilio
        5. Recibe tu RIF en el momento
        """)
with tab5:
    st.markdown("## 📋 Guías Paso a Paso de Trámites")
    st.markdown("---")

    tramite = st.selectbox(
        "Selecciona el trámite que deseas realizar:",
        [
            "Obtener el RIF por primera vez",
            "Actualizar datos del RIF",
            "Declarar IVA en el portal",
            "Declarar ISLR anual",
            "Obtener Solvencia Tributaria",
            "Recuperar clave del portal SENIAT",
            "Inscribirse como Contribuyente Especial",
            "Interponer Recurso Jerárquico",
        ]
    )

    if tramite == "Obtener el RIF por primera vez":
        st.markdown("### 📌 Cómo obtener el RIF por primera vez")
        st.success("**Personas Naturales:**")
        pasos = [
            "Ingresa al portal www.seniat.gob.ve",
            "Haz clic en 'Sistemas en Línea'",
            "Selecciona 'Registro de Contribuyentes'",
            "Completa el formulario con tus datos personales",
            "Adjunta copia de Cédula de Identidad vigente",
            "Adjunta comprobante de domicilio (factura de servicios)",
            "Envía la solicitud y anota el número de expediente",
            "Acude a la oficina del SENIAT más cercana con los documentos originales",
            "Retira tu RIF en un plazo de 3 a 5 días hábiles",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")

        st.warning("**Documentos necesarios:**\n- Cédula de Identidad original y copia\n- Comprobante de domicilio\n- Partida de nacimiento (menores de edad)")

    elif tramite == "Actualizar datos del RIF":
        st.markdown("### 📌 Cómo actualizar datos del RIF")
        pasos = [
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesión con tu usuario y clave",
            "Ve a 'Actualización de Datos'",
            "Modifica los datos que necesitas actualizar",
            "Adjunta los documentos que soporten el cambio",
            "Confirma los cambios y guarda",
            "Imprime el comprobante de actualización",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")

    elif tramite == "Declarar IVA en el portal":
        st.markdown("### 📌 Cómo declarar el IVA en el portal")
        pasos = [
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesión con tu RIF y clave",
            "Selecciona 'Declaración y Pago de IVA'",
            "Elige el período a declarar (mes y año)",
            "Ingresa el total de ventas del mes",
            "Ingresa el total de compras del mes",
            "El sistema calcula automáticamente el IVA a pagar",
            "Verifica los montos y confirma la declaración",
            "Realiza el pago en el banco autorizado",
            "Guarda el comprobante de declaración y pago",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")
        st.info("⏰ **Plazo:** Dentro de los 15 días hábiles del mes siguiente")

    elif tramite == "Declarar ISLR anual":
        st.markdown("### 📌 Cómo declarar el ISLR anual")
        pasos = [
            "Reúne todos tus comprobantes de ingresos del año",
            "Reúne las retenciones de ISLR que te realizaron",
            "Ingresa al portal www.seniat.gob.ve",
            "Selecciona 'Declaración de ISLR'",
            "Elige el ejercicio fiscal a declarar",
            "Ingresa todos tus ingresos anuales",
            "Ingresa tus deducciones permitidas",
            "El sistema calcula el impuesto a pagar",
            "Confirma y envía la declaración",
            "Realiza el pago si corresponde",
            "Guarda el comprobante",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")
        st.info("⏰ **Plazo:** Personas Naturales hasta el 31 de Marzo de cada año")

    elif tramite == "Obtener Solvencia Tributaria":
        st.markdown("### 📌 Cómo obtener la Solvencia Tributaria")
        pasos = [
            "Verifica que estés al día con todas tus declaraciones",
            "Verifica que no tengas deudas pendientes con el SENIAT",
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesión con tu RIF y clave",
            "Selecciona 'Solvencia Tributaria'",
            "Haz clic en 'Solicitar Solvencia'",
            "El sistema verifica tu estatus automáticamente",
            "Si estás solvente, descarga e imprime el documento",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")
        st.warning("⚠️ **Vigencia:** La solvencia tiene una validez de 6 meses")

    elif tramite == "Recuperar clave del portal SENIAT":
        st.markdown("### 📌 Cómo recuperar tu clave del portal")
        pasos = [
            "Ingresa al portal www.seniat.gob.ve",
            "Haz clic en '¿Olvidaste tu clave?'",
            "Ingresa tu número de RIF",
            "Ingresa tu correo electrónico registrado",
            "Revisa tu correo y sigue las instrucciones",
            "Si no tienes correo registrado, acude a la oficina del SENIAT más cercana con tu cédula",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")

    elif tramite == "Inscribirse como Contribuyente Especial":
        st.markdown("### 📌 Inscripción como Contribuyente Especial")
        st.info("ℹ️ La calificación de Contribuyente Especial la otorga el SENIAT, no se solicita directamente.")
        pasos = [
            "El SENIAT te notifica mediante carta o publicación oficial",
            "Recibes la notificación de calificación como Contribuyente Especial",
            "Acude a la Gerencia Regional de Tributos Internos",
            "Presenta tu RIF y cédula de identidad",
            "Firma la notificación de calificación",
            "A partir de ese momento cumples con el calendario de Contribuyentes Especiales",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")

    elif tramite == "Interponer Recurso Jerárquico":
        st.markdown("### 📌 Cómo interponer un Recurso Jerárquico")
        pasos = [
            "Recibe y lee detenidamente el acto administrativo del SENIAT",
            "Tienes 25 días hábiles para interponer el recurso",
            "Redacta el escrito del recurso con tus argumentos",
            "Anexa todas las pruebas que soporten tu caso",
            "Presenta el escrito en la oficina del SENIAT que emitió el acto",
            "Solicita el sello de recibido en tu copia",
            "El SENIAT tiene 60 días hábiles para responder",
            "Si no responde, se considera silencio administrativo negativo",
            "Puedes acudir al Tribunal Contencioso Tributario si es necesario",
        ]
        for i, paso in enumerate(pasos, 1):
            st.markdown(f"**Paso {i}:** {paso}")
        st.error("Importante: Se recomienda asesorarse con un abogado tributario")
                 

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFD700;'>

    🏛️ <b>SENIAT</b> - Servicio Nacional Integrado de Administración Aduanera y Tributaria<br>
    📞 0800-SENIAT (736428) | 🌐 www.seniat.gob.ve<br>
    📍 Venezuela
</div>
""", unsafe_allow_html=True)









