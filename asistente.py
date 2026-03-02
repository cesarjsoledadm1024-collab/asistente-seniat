import streamlit as st
from groq import Groq
from datetime import datetime
import re

st.set_page_config(
    page_title="Asistente Virtual SENIAT",
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
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
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", width=200)

st.title("🏛️ Asistente Virtual SENIAT")
st.caption("Atención al contribuyente - Consultas tributarias")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Asistente",
    "🧮 Calculadora",
    "📅 Fechas",
    "📖 Glosario",
    "📋 Guías",
    "🔍 Verificar RIF"
])

with tab1:
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        bienvenida = """¡Bienvenido al Asistente Virtual del SENIAT! 🏛️

Estoy aquí para ayudarle con sus consultas tributarias. Puede preguntarme sobre:

✅ Registro de RIF  ✅ Declaraciones de IVA e ISLR  ✅ Retenciones
✅ Contribuyentes Especiales  ✅ Solvencia Tributaria  ✅ Sanciones y Recursos

¿En qué le puedo ayudar hoy?"""
        st.session_state.mensajes.append({"role": "assistant", "content": bienvenida})

    col_a, col_b = st.columns([4, 1])
    with col_b:
        if st.button("🗑️ Limpiar chat"):
            st.session_state.mensajes = []
            st.rerun()

    

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
                        Atiendes contribuyentes con informacion sobre RIF, IVA, ISLR, retenciones,
                        contribuyentes especiales, solvencia tributaria, sanciones y tramites en linea.
                        Responde en español, de forma clara y amable.
                        Si no estas seguro, indica al contribuyente que visite www.seniat.gob.ve"""
                    }
                ] + st.session_state.mensajes
            )
            texto = respuesta.choices[0].message.content
            st.write(texto)
            st.session_state.mensajes.append({"role": "assistant", "content": texto})
        st.rerun()

with tab2:
    st.markdown("## 🧮 Calculadora Tributaria")
    st.markdown("---")
    calc_tipo = st.selectbox("Selecciona el impuesto:", ["IVA (16%)", "Retencion IVA 75%", "Retencion IVA 100%", "ISLR (estimado)"])
    monto = st.number_input("Monto en Bolivares (Bs):", min_value=0.0, format="%.2f")
    if st.button("🔢 Calcular"):
        if monto > 0:
            if calc_tipo == "IVA (16%)":
                impuesto = monto * 0.16
                total = monto + impuesto
                st.success(f"Monto base: Bs. {monto:,.2f}\nIVA (16%): Bs. {impuesto:,.2f}\nTotal: Bs. {total:,.2f}")
            elif calc_tipo == "Retencion IVA 75%":
                iva = monto * 0.16
                retencion = iva * 0.75
                pagar = iva - retencion
                st.success(f"Monto base: Bs. {monto:,.2f}\nIVA: Bs. {iva:,.2f}\nRetencion 75%: Bs. {retencion:,.2f}\nIVA a pagar: Bs. {pagar:,.2f}")
            elif calc_tipo == "Retencion IVA 100%":
                iva = monto * 0.16
                st.success(f"Monto base: Bs. {monto:,.2f}\nIVA: Bs. {iva:,.2f}\nRetencion 100%: Bs. {iva:,.2f}\nIVA a pagar: Bs. 0.00")
            elif calc_tipo == "ISLR (estimado)":
                if monto <= 1000: tasa = 0.06
                elif monto <= 1500: tasa = 0.09
                elif monto <= 2000: tasa = 0.12
                elif monto <= 2500: tasa = 0.16
                elif monto <= 3000: tasa = 0.20
                else: tasa = 0.34
                islr = monto * tasa
                st.success(f"Monto anual: Bs. {monto:,.2f}\nTasa: {tasa*100:.0f}%\nISLR estimado: Bs. {islr:,.2f}")
                st.info("Calculo estimado. Consulte con un especialista tributario.")
        else:
            st.warning("Ingresa un monto mayor a 0")

with tab3:
    st.markdown("## 📅 Fechas de Declaracion")
    st.markdown("---")
    hoy = datetime.now()
    st.markdown(f"### Hoy es: {hoy.strftime('%d/%m/%Y')}")
    tipo = st.selectbox("Tipo de contribuyente:", ["Contribuyente Ordinario", "Contribuyente Especial"])
    if tipo == "Contribuyente Ordinario":
        st.info("IVA: Dentro de los 15 dias habiles del mes siguiente")
        st.info("ISLR: Personas Naturales hasta el 31 de Marzo de cada año")
        st.warning("Retenciones IVA: Se enteran los lunes y martes segun ultimo digito del RIF")
    else:
        st.info("IVA 1ra quincena (1-15): declarar entre dias 16 y 20 del mismo mes")
        st.info("IVA 2da quincena (16-31): declarar entre dias 1 y 5 del mes siguiente")
        st.markdown("""
| Ultimo digito RIF | Dia de enteramiento |
|---|---|
| 0 y 1 | Lunes |
| 2 y 3 | Martes |
| 4 y 5 | Miercoles |
| 6 y 7 | Jueves |
| 8 y 9 | Viernes |
        """)
    st.error("Consecuencias por declarar fuera de tiempo: Multa de 10 UT por mes de retraso, intereses moratorios y posible cierre del establecimiento.")

with tab4:
    st.markdown("## 📖 Glosario Tributario SENIAT")
    st.markdown("---")
    buscar = st.text_input("🔍 Buscar termino:", placeholder="Escribe un termino tributario...")
    terminos = {
        "IVA": "Impuesto al Valor Agregado: Impuesto indirecto que grava la venta de bienes y servicios. Tasa general 16%.",
        "ISLR": "Impuesto Sobre la Renta: Impuesto directo que grava los enriquecimientos netos de personas naturales y juridicas.",
        "RIF": "Registro de Informacion Fiscal: Documento que identifica a personas naturales y juridicas ante el SENIAT.",
        "Contribuyente": "Persona natural o juridica obligada al pago de tributos por realizar actividades economicas gravadas.",
        "Contribuyente Especial": "Persona calificada por el SENIAT por su alto nivel de ingresos. Tiene obligaciones adicionales.",
        "Contribuyente Ordinario": "Persona que realiza actividades gravadas con IVA sin ser calificada como especial.",
        "Retencion": "Mecanismo por el cual el comprador descuenta un porcentaje del impuesto al momento del pago.",
        "Agente de Retencion": "Persona designada por el SENIAT para retener impuestos y enterarlos al fisco.",
        "Enteramiento": "Acto de depositar al SENIAT los impuestos retenidos dentro del plazo establecido.",
        "Debito Fiscal": "IVA que el vendedor cobra al comprador. Representa el impuesto que se debe al fisco.",
        "Credito Fiscal": "IVA pagado en compras. Se puede deducir del debito fiscal para calcular el IVA a pagar.",
        "Solvencia Tributaria": "Documento del SENIAT que certifica que el contribuyente esta al dia con sus obligaciones.",
        "Declaracion Sustitutiva": "Nueva declaracion que reemplaza una anterior cuando se detectan errores.",
        "Unidad Tributaria": "Valor en bolivares establecido por el SENIAT para calcular multas y sanciones.",
        "Ejercicio Fiscal": "Periodo de 12 meses para calcular y declarar impuestos.",
        "Factura Fiscal": "Documento que certifica una operacion comercial segun requisitos del SENIAT.",
        "Recurso Jerarquico": "Mecanismo legal para impugnar actos del SENIAT ante un superior jerarquico.",
        "SENIAT": "Servicio Nacional Integrado de Administracion Aduanera y Tributaria de Venezuela.",
        "Timbre Fiscal": "Impuesto por la realizacion de actos juridicos ante organismos publicos.",
        "Alicuota": "Porcentaje que se aplica sobre la base imponible para calcular el impuesto.",
    }
    if buscar:
        resultados = {k: v for k, v in terminos.items() if buscar.upper() in k.upper() or buscar.lower() in v.lower()}
        if resultados:
            for termino, definicion in resultados.items():
                st.info(f"**{termino}:** {definicion}")
        else:
            st.warning(f"No se encontro ningun termino relacionado con '{buscar}'")
    else:
        for termino, definicion in sorted(terminos.items()):
            with st.expander(f"📌 {termino}"):
                st.write(definicion)

with tab5:
    st.markdown("## 📋 Guias Paso a Paso de Tramites")
    st.markdown("---")
    tramite = st.selectbox("Selecciona el tramite:", [
        "Obtener el RIF por primera vez",
        "Actualizar datos del RIF",
        "Declarar IVA en el portal",
        "Declarar ISLR anual",
        "Obtener Solvencia Tributaria",
        "Recuperar clave del portal SENIAT",
        "Inscribirse como Contribuyente Especial",
        "Interponer Recurso Jerarquico",
        "Emitir Facturas Fiscales",
        "Solicitar Prorroga de Declaracion",
        "Registrar una Maquina Fiscal",
        "Solicitar Reintegro de Impuestos",
        "Cambiar Domicilio Fiscal",
        "Declarar Retenciones de ISLR",
    ])
    pasos_dict = {
        "Obtener el RIF por primera vez": [
            "Ingresa al portal www.seniat.gob.ve",
            "Haz clic en Sistemas en Linea",
            "Selecciona Registro de Contribuyentes",
            "Completa el formulario con tus datos personales",
            "Adjunta copia de Cedula de Identidad vigente",
            "Adjunta comprobante de domicilio",
            "Envia la solicitud y anota el numero de expediente",
            "Acude a la oficina del SENIAT con los documentos originales",
            "Retira tu RIF en 3 a 5 dias habiles",
        ],
        "Actualizar datos del RIF": [
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesion con tu usuario y clave",
            "Ve a Actualizacion de Datos",
            "Modifica los datos que necesitas actualizar",
            "Adjunta los documentos que soporten el cambio",
            "Confirma los cambios y guarda",
            "Imprime el comprobante de actualizacion",
        ],
        "Declarar IVA en el portal": [
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesion con tu RIF y clave",
            "Selecciona Declaracion y Pago de IVA",
            "Elige el periodo a declarar",
            "Ingresa el total de ventas del mes",
            "Ingresa el total de compras del mes",
            "El sistema calcula el IVA a pagar",
            "Verifica los montos y confirma",
            "Realiza el pago en el banco autorizado",
            "Guarda el comprobante",
        ],
        "Declarar ISLR anual": [
            "Reune todos tus comprobantes de ingresos del año",
            "Reune las retenciones de ISLR que te realizaron",
            "Ingresa al portal www.seniat.gob.ve",
            "Selecciona Declaracion de ISLR",
            "Elige el ejercicio fiscal a declarar",
            "Ingresa todos tus ingresos anuales",
            "Ingresa tus deducciones permitidas",
            "El sistema calcula el impuesto",
            "Confirma y envia la declaracion",
            "Realiza el pago si corresponde",
            "Guarda el comprobante",
        ],
        "Obtener Solvencia Tributaria": [
            "Verifica que estes al dia con todas tus declaraciones",
            "Verifica que no tengas deudas con el SENIAT",
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesion con tu RIF y clave",
            "Selecciona Solvencia Tributaria",
            "Haz clic en Solicitar Solvencia",
            "El sistema verifica tu estatus automaticamente",
            "Si estas solvente, descarga e imprime el documento",
        ],
        "Recuperar clave del portal SENIAT": [
            "Ingresa al portal www.seniat.gob.ve",
            "Haz clic en Olvidaste tu clave",
            "Ingresa tu numero de RIF",
            "Ingresa tu correo electronico registrado",
            "Revisa tu correo y sigue las instrucciones",
            "Si no tienes correo registrado, acude a la oficina del SENIAT con tu cedula",
        ],
        "Inscribirse como Contribuyente Especial": [
            "El SENIAT te notifica mediante carta oficial",
            "Recibes la notificacion de calificacion",
            "Acude a la Gerencia Regional de Tributos Internos",
            "Presenta tu RIF y cedula de identidad",
            "Firma la notificacion de calificacion",
            "A partir de ese momento cumples el calendario de Contribuyentes Especiales",
        ],
        "Interponer Recurso Jerarquico": [
            "Lee detenidamente el acto administrativo del SENIAT",
            "Tienes 25 dias habiles para interponer el recurso",
            "Redacta el escrito del recurso con tus argumentos",
            "Anexa todas las pruebas que soporten tu caso",
            "Presenta el escrito en la oficina del SENIAT que emitio el acto",
            "Solicita el sello de recibido en tu copia",
            "El SENIAT tiene 60 dias habiles para responder",
            "Si no responde se considera silencio administrativo negativo",
            "Puedes acudir al Tribunal Contencioso Tributario si es necesario",
        ],
        "Emitir Facturas Fiscales": [
            "Verifica que tu RIF este activo y vigente",
            "Asegurate de tener una maquina fiscal o sistema autorizado",
            "La factura debe contener: RIF, nombre o razon social, direccion fiscal",
            "Incluye numero de control correlativo",
            "Especifica descripcion del bien o servicio",
            "Indica el monto gravable, alicuota y monto del impuesto",
            "Entrega original al cliente y conserva la copia",
            "Registra la factura en tu libro de ventas",
        ],
        "Solicitar Prorroga de Declaracion": [
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesion con tu RIF y clave",
            "Ve a la seccion de Solicitudes",
            "Selecciona Prorroga de Declaracion",
            "Indica el tipo de declaracion y el periodo",
            "Explica el motivo de la solicitud",
            "Adjunta documentos que justifiquen la prorroga",
            "Envia la solicitud antes del vencimiento",
            "Espera la respuesta del SENIAT por correo o portal",
        ],
        "Registrar una Maquina Fiscal": [
            "Adquiere la maquina fiscal en un proveedor autorizado por el SENIAT",
            "El proveedor debe instalar y activar la maquina",
            "Ingresa al portal www.seniat.gob.ve",
            "Selecciona Registro de Maquinas Fiscales",
            "Ingresa el numero de serial de la maquina",
            "Completa los datos del establecimiento",
            "El SENIAT genera el certificado de registro",
            "Conserva el certificado en el establecimiento",
        ],
        "Solicitar Reintegro de Impuestos": [
            "Verifica que tienes creditos fiscales a tu favor",
            "Reune todas las facturas que soportan el credito",
            "Ingresa al portal www.seniat.gob.ve",
            "Selecciona Solicitud de Reintegro",
            "Completa el formulario con el monto a reintegrar",
            "Adjunta los documentos soporte",
            "El SENIAT tiene 60 dias para responder",
            "Si aprueban, el reintegro se realiza mediante cheque o transferencia",
        ],
        "Cambiar Domicilio Fiscal": [
            "Prepara el nuevo comprobante de domicilio",
            "Ingresa al portal www.seniat.gob.ve",
            "Inicia sesion con tu RIF y clave",
            "Ve a Actualizacion de Datos del RIF",
            "Modifica la direccion fiscal",
            "Adjunta el comprobante del nuevo domicilio",
            "Confirma los cambios",
            "Imprime el nuevo RIF actualizado",
        ],
        "Declarar Retenciones de ISLR": [
            "Reune todos los comprobantes de retenciones realizadas",
            "Ingresa al portal www.seniat.gob.ve",
            "Selecciona Declaracion de Retenciones de ISLR",
            "Elige el periodo a declarar",
            "Ingresa los datos de cada retencion realizada",
            "Verifica los montos totales",
            "Confirma y envia la declaracion",
            "Realiza el enteramiento en el banco autorizado",
            "Emite los comprobantes de retencion a cada proveedor",
            "Guarda el comprobante de declaracion",
        ],
    }
    pasos = pasos_dict.get(tramite, [])
    for i, paso in enumerate(pasos, 1):
        st.markdown(f"**Paso {i}:** {paso}")
    if tramite == "Interponer Recurso Jerarquico":
        st.error("Se recomienda asesorarse con un abogado tributario")
    if tramite == "Obtener Solvencia Tributaria":
        st.warning("Vigencia: La solvencia tiene una validez de 6 meses")

with tab6:
    st.markdown("## 🔍 Verificar Formato de RIF")
    st.markdown("---")
    st.markdown("""
| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Persona Natural | V-XXXXXXXX-X | V-12345678-9 |
| Persona Juridica | J-XXXXXXXX-X | J-12345678-9 |
| Gobierno | G-XXXXXXXX-X | G-20004036-0 |
| Extranjero | E-XXXXXXXX-X | E-12345678-9 |
| Pasaporte | P-XXXXXXXX-X | P-12345678-9 |
    """)
    rif = st.text_input("Ingresa el RIF:", placeholder="Ejemplo: V-12345678-9", max_chars=13).upper().strip()
    if st.button("🔍 Verificar RIF"):
        if rif:
            patron = r'^[VJGEP]-\d{8}-\d$'
            if re.match(patron, rif):
                tipos = {"V": "Persona Natural Venezolana", "J": "Persona Juridica", "G": "Organismo Gubernamental", "E": "Persona Natural Extranjera", "P": "Persona con Pasaporte"}
                st.success(f"RIF VALIDO\nRIF: {rif}\nTipo: {tipos.get(rif[0], 'Desconocido')}")
                st.info("Esta herramienta verifica el formato. Para verificar si el RIF esta activo visita www.seniat.gob.ve")
            else:
                st.error("RIF NO VALIDO. Formato correcto: X-XXXXXXXX-X (Ejemplo: V-12345678-9)")
        else:
            st.warning("Ingresa un RIF para verificar")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #FFD700;'>
    🏛️ <b>SENIAT</b> - Servicio Nacional Integrado de Administracion Aduanera y Tributaria<br>
    📞 0800-SENIAT (736428) | 🌐 www.seniat.gob.ve<br>
    📍 Venezuela
</div>
""", unsafe_allow_html=True)

