import streamlit as st
from groq import Groq
import time
import uuid
import datetime

# ==============================================================================
# 1. CONFIGURACIÓN DEL ENTORNO Y PÁGINA SUPERIOR
# ==============================================================================
st.set_page_config(
    page_title="ZenBot OS | IA de Bienestar e Investigación",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. NUEVO SISTEMA DE CONEXIÓN: GROQ (LLAMA 3.1)
# ==============================================================================
# 🔑 PEGA AQUÍ TU CLAVE DE GROQ (Consíguela en console.groq.com) 🔑
API_KEY = "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"

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Falla crítica: No se pudo conectar con el servidor. {e}")

# ==============================================================================
# 3. MOTOR DE ESTILOS (PSICOLOGÍA DEL COLOR Y FIXES VISUALES)
# ==============================================================================
def inyectar_css_premium():
    st.markdown("""
    <style>
        /* Fondo General de la App: Degradado Verde Claro y Alegre */
        .stApp { 
            background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%) !important; 
        }
        
        /* Texto General */
        html, body, p, span, div, label, h1, h2, h3, h4, li, [data-testid="stMarkdownContainer"] p {
            color: #2e7d32 !important;
            font-family: 'Inter', sans-serif;
        }

        /* Ocultar elementos innecesarios */
        header[data-testid="stHeader"], footer { display: none !important; }

        //* -------------------------------------------------------------
           FIX DEFINITIVO PARA LA FLECHA EN INTERNET
           ------------------------------------------------------------- */
        /* Buscamos el botón de apertura por su icono de flecha nativo */
        button[data-testid="baseButton-header"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background-color: #558b2f !important; /* Círculo verde */
            border-radius: 50% !important;
            z-index: 9999999 !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            position: fixed !important;
            top: 15px !important;
            left: 15px !important;
            width: 40px !important;
            height: 40px !important;
        }
        
        /* Pintamos la flecha de color blanco para que resalte */
        button[data-testid="baseButton-header"] svg { 
            fill: #ffffff !important; 
            color: #ffffff !important; 
        }

        /* SIDEBAR BLANCO CON BORDE VERDE */
        section[data-testid="stSidebar"] { 
            background-color: #ffffff !important; 
            border-right: 4px solid #aed581;
        }
        
        /* BOTONES DEL MENÚ LATERAL */
        .stButton > button {
            border-radius: 20px !important;
            border: 2px solid #8bc34a !important;
            background-color: #f1f8e9 !important;
            color: #33691e !important;
            font-weight: 700 !important;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #dcedc8 !important;
            transform: translateY(-2px);
        }

        /* BURBUJAS DE CHAT DIFERENCIADAS */
        /* Usuario: Azul Cielo Suave */
        [data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"] p:contains("user")) {
            background-color: #e3f2fd !important;
            border: 2px solid #90caf9 !important;
            border-radius: 25px 25px 5px 25px !important;
        }
        /* ZenBot: Amarillo/Verde Crema Relajante */
        [data-testid="stChatMessage"]:has([data-testid="stMarkdownContainer"] p:contains("assistant")) {
            background-color: #f9fbe7 !important;
            border: 2px solid #d4e157 !important;
            border-radius: 25px 25px 25px 5px !important;
        }

/* -------------------------------------------------------------
           FIX: BARRA DE ESCRITURA TOTALMENTE INTEGRADA (CON ESQUINAS PERFECTAS)
           ------------------------------------------------------------- */
        /* El contenedor exterior de la franja negra inferior */
        [data-testid="stChatInputContainer"] {
            background-color: #121212 !important;
            border-top: 2px solid #7cb342 !important; /* Línea verde superior continua */
            padding: 15px 20px 25px 20px !important;
        }

        /* La caja donde escribes: Eliminamos cortes raros en las esquinas */
        [data-testid="stChatInput"] {
            background-color: #121212 !important; 
            border-radius: 20px !important; /* Esquinas pulidas y balanceadas */
            border: 2px solid #558b2f !important; /* Borde verde uniforme */
            box-shadow: none !important; 
            overflow: hidden !important; /* Esto corta cualquier residuo gris en las esquinas */
        }

        /* Ajuste fino para limpiar los bordes internos nativos de Streamlit */
        [data-testid="stChatInput"] > div {
            background-color: #121212 !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* El espacio interno de escritura */
        [data-testid="stChatInput"] textarea {
            color: #ffffff !important; /* Texto en blanco */
            background-color: #121212 !important;
            padding-top: 10px !important;
        }
        
        /* Texto informativo de fondo */
        [data-testid="stChatInput"] textarea::placeholder {
            color: #757575 !important;
        }

        /* Botón de enviar integrado (Flechita minimalista verde) */
        [data-testid="stChatInput"] button {
            background-color: transparent !important; 
            color: #7cb342 !important; 
        }

        /* -------------------------------------------------------------
           EXTRA FIX: FLECHA FLOTANTE DEL PANEL DE CONTROL
           ------------------------------------------------------------- */
        [data-testid="collapsedControl"] {
            background-color: #558b2f !important; 
            border-radius: 50% !important;
            z-index: 9999999 !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            position: fixed !important;
            top: 20px !important;
            left: 20px !important;
            width: 45px !important;
            height: 45px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        [data-testid="collapsedControl"] svg { fill: white !important; }
    </style>
    """, unsafe_allow_html=True)

# ─── AGREGA ESTA LÍNEA JUSTO AQUÍ (PEGADA AL BORDE IZQUIERDO) ───
inyectar_css_premium()

# ==============================================================================
# 4. GESTIÓN DE MEMORIA Y BASE DE DATOS LOCAL
# ==============================================================================
def iniciar_base_datos():
    if "historial_chats" not in st.session_state:
        st.session_state.historial_chats = {}
    if "chat_actual_id" not in st.session_state:
        crear_nueva_sesion()
    if "config_usuario" not in st.session_state:
        st.session_state.config_usuario = {"mood": "🌤️ Bien", "modo": "🧘 Modo Zen (Empatía)"}

def crear_nueva_sesion():
    nuevo_id = str(uuid.uuid4())
    st.session_state.historial_chats[nuevo_id] = {
        "titulo": "Nueva Búsqueda / Chat",
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mensajes": []
    }
    st.session_state.chat_actual_id = nuevo_id

iniciar_base_datos()

id_actual = st.session_state.chat_actual_id
chat_actual = st.session_state.historial_chats[id_actual]
mensajes = chat_actual["mensajes"]

# ==============================================================================
# 5. CEREBRO EXPERTO EN BURNOUT (Llama 3)
# ==============================================================================
def obtener_instrucciones_ia(mood):
    # Lógica de Empatía Dinámica
    if "Agotado" in mood:
        actitud = "El usuario está AGOTADO. Sé extremadamente gentil, comprensivo y no le exijas nada. Da respuestas muy cortas, ofrécele un refugio seguro y valida su cansancio profundamente."
        temperatura = 0.5
    elif "Regular" in mood:
        actitud = "El usuario se siente REGULAR. Escucha con atención, dale ánimos suaves y pregúntale si hay algo específico que le esté pesando hoy."
        temperatura = 0.6
    elif "Activo" in mood or "Bien" in mood:
        actitud = "El usuario se siente BIEN/ACTIVO. Mantén una energía positiva, constructiva y motivadora. Apoya sus proyectos o responde sus dudas con entusiasmo."
        temperatura = 0.7
    else:
        actitud = "El usuario se siente ZEN. Habla desde la paz, la tranquilidad y el mindfulness. Usa un tono filosófico y calmado."
        temperatura = 0.7

    instrucciones = f"""
    Eres ZenBot, un especialista avanzado en bienestar emocional y prevención del burnout.
    
    ESTADO ACTUAL DEL USUARIO: {mood}
    INSTRUCCIÓN DE COMPORTAMIENTO: {actitud}

    TUS DIRECTRICES PRINCIPALES:
    1. ESCUCHA ACTIVA Y VALIDACIÓN: Adapta tu respuesta a su estado actual. Hazle sentir escuchado.
    2. MICRO-HÁBITOS: No des respuestas gigantes que abrumen. Sé conciso.
    3. TONO AMIGABLE: Usa emojis relajantes (🌿, ✨, 💚, ☕) para hacer la lectura más suave.
    4. RESPUESTAS GENERALES CORTAS: Si te pregunta algo de conocimiento general (ej. "cuánto es 5x5" o "qué es la fotosíntesis"), respóndelo directa y amablemente.
    """
    return instrucciones, temperatura
def generar_titulo_inteligente(mensaje):
    try:
        respuesta = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Genera un título muy corto de 2 a 4 palabras que describa de qué trata este sentimiento o duda: '{mensaje}'. Solo el título, sin comillas."}],
            max_tokens=10
        )
        return respuesta.choices[0].message.content.strip()
    except:
        return "Chat Guardado 📝"

def formatear_para_descarga(titulo, mensajes):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    texto_exportar = f"--- REPORTE DE BIENESTAR: ZENBOT ---\nTema: {titulo}\nFecha: {fecha}\n{'='*40}\n\n"
    for m in mensajes:
        autor = "TÚ" if m["role"] == "user" else "ZENBOT"
        texto_exportar += f"[{autor}]:\n{m['content']}\n\n{'-'*20}\n\n"
    return texto_exportar

# ==============================================================================
# 6. INTERFAZ DE USUARIO (UI)
# ==============================================================================
with st.sidebar:
    # NUEVO CONTENEDOR CON TÍTULO E ICONO ALINEADOS
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 25px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712139.png' width='55'>
            <h3 style='margin: 0; color: #F4F4F4; font-size: 1.15rem; line-height: 1.3;'>Prevención contra el burnout y estrés</h3>
        </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("Panel de Control")
# Menú vertical de estado de ánimo
    opciones_mood = ["😔 Agotado", "⛅ Regular", "🌤️ Bien", "☀️ Activo", "✨ Zen"]
    
    # Asegurarnos de que no haya error si el estado actual no está en la lista
    if st.session_state.config_usuario["mood"] not in opciones_mood:
        st.session_state.config_usuario["mood"] = "⛅ Regular"
        
    st.session_state.config_usuario["mood"] = st.radio(
        "¿Cómo te sientes hoy?", 
        options=opciones_mood,
        index=opciones_mood.index(st.session_state.config_usuario["mood"])
    )
    st.divider()
    
    st.markdown('<div class="btn-primario">', unsafe_allow_html=True)
    if st.button("➕ Iniciar Nueva Charla", use_container_width=True):
        crear_nueva_sesion()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 📂 Mis Conversaciones")
    chats_invertidos = list(st.session_state.historial_chats.items())[::-1]
    
    if len(chats_invertidos) == 0:
        st.caption("No hay charlas guardadas.")
    else:
        for chat_id, data in chats_invertidos:
            col_chat, col_borrar_sidebar = st.columns([8, 2])
            icono = "📌" if chat_id == id_actual else "🌿"
            
            with col_chat:
                if st.button(f"{icono} {data['titulo']}", key=f"sel_{chat_id}", use_container_width=True):
                    st.session_state.chat_actual_id = chat_id
                    st.rerun()
                    
            with col_borrar_sidebar:
                if st.button("🗑️", key=f"del_{chat_id}", help="Eliminar charla"):
                    del st.session_state.historial_chats[chat_id]
                    if st.session_state.chat_actual_id == chat_id:
                        if len(st.session_state.historial_chats) > 0:
                            st.session_state.chat_actual_id = list(st.session_state.historial_chats.keys())[-1]
                        else:
                            crear_nueva_sesion()
                    st.rerun()
           
    st.divider()
    st.markdown("#### 💾 Guardar Reflexiones")
    if len(mensajes) > 0:
        st.download_button(
            label="⬇️ Descargar Charla (.txt)",
            data=formatear_para_descarga(chat_actual["titulo"], mensajes),
            file_name=f"ZenBot_{chat_actual['titulo']}.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- B. ÁREA PRINCIPAL ---
col_titulo, col_borrar = st.columns([8, 2])
with col_titulo:
    st.markdown(f"## {chat_actual['titulo']}")
    st.caption(f"**Especialista en Burnout** 🌿 | **Inicio:** {chat_actual['fecha']}")
with col_borrar:
    if st.button("🧹 Limpiar Pantalla"):
        st.session_state.historial_chats[id_actual]["mensajes"] = []
        st.rerun()

st.markdown("---")

if not mensajes:
    st.info("🌿 **Espacio Seguro Iniciado:** Hola. Estoy aquí para ayudarte a manejar el estrés, prevenir el burnout profesional o simplemente escucharte si necesitas desahogarte. ¿Qué tienes en mente hoy?")

for msg in mensajes:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ------------------------------------------------------------------------------
# 7. PROCESAMIENTO Y GENERACIÓN (CON GROQ)
# ------------------------------------------------------------------------------
if pregunta := st.chat_input("Ingresa tu consulta o cuéntame cómo te sientes..."):
    
    if len(mensajes) == 0:
        st.session_state.historial_chats[id_actual]["titulo"] = generar_titulo_inteligente(pregunta)

    st.session_state.historial_chats[id_actual]["mensajes"].append({"role": "user", "content": pregunta})
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta)

    with st.chat_message("assistant", avatar="🤖"):
        caja_respuesta = st.empty()
        texto_acumulado = ""

        try:
            # AQUÍ ESTÁ LA CORRECCIÓN: Ahora solo le enviamos el "mood" (1 solo argumento)
            instrucciones_sistema, temperatura_ia = obtener_instrucciones_ia(st.session_state.config_usuario["mood"])
            
            # 2. Construir la memoria completa
            historial_api = [{"role": "system", "content": instrucciones_sistema}]
            for msg in st.session_state.historial_chats[id_actual]["mensajes"]:
                historial_api.append({"role": msg["role"], "content": msg["content"]})

            # 3. Llamar a Groq (Llama 3.1)
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=historial_api,
                stream=True,
                temperature=temperatura_ia,
                max_tokens=1500
            )
            
            # 4. Mostrar respuesta fluidamente
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    texto_acumulado += chunk.choices[0].delta.content
                    caja_respuesta.markdown(texto_acumulado + "▌")
                    time.sleep(0.005) 
            
            caja_respuesta.markdown(texto_acumulado)
            
            st.session_state.historial_chats[id_actual]["mensajes"].append(
                {"role": "assistant", "content": texto_acumulado}
            )
            
            if len(mensajes) <= 2:
                st.rerun()

        except Exception as error_api:
            st.error("⚠️ Error de conexión. Verifica tu clave de Groq.")
            st.code(str(error_api))