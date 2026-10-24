import streamlit as st
from google import genai
from google.genai import types
import datetime

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA (CSS)
# ==========================================
st.set_page_config(
    page_title="Rincón de Girasoles y Tortugas 🌻🐢",
    page_icon="🌻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bloque de CSS personalizado: Crema, Amarillo Girasol y Verde Tortuga
st.markdown("""
<style>
    /* Fondo principal en tono crema cálido */
    .stApp {
        background-color: #FFFDF5;
        color: #2C3E2D;
    }
    
    /* Barra lateral en tono verde tortuga suave */
    [data-testid="stSidebar"] {
        background-color: #EBF3E8;
        border-right: 3px solid #F4C430;
    }
    
    /* Títulos y encabezados */
    h1, h2, h3 {
        color: #3A5F43 !important;
        font-family: 'Georgia', serif;
    }
    
    /* Botón principal estilo Girasol y Tortuga */
    .stButton > button {
        background: linear-gradient(135deg, #FFD54F 0%, #F4C430 100%);
        color: #2C3E2D !important;
        border: 2px solid #4A7C59 !important;
        border-radius: 25px !important;
        padding: 0.6rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 10px rgba(74, 124, 89, 0.15) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4A7C59 0%, #3A5F43 100%) !important;
        color: #FFFDF5 !important;
        border-color: #F4C430 !important;
        transform: translateY(-2px);
    }
    
    /* Estilo para las Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #EBF3E8;
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFDF5;
        border-radius: 10px;
        padding: 10px 20px;
        color: #3A5F43;
        font-weight: 600;
        border: 1px solid #C5DEC9;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #F4C430 !important;
        color: #2C3E2D !important;
        border: 2px solid #3A5F43 !important;
    }
    
    /* Cajas de debate y expanders */
    .streamlit-expanderHeader {
        background-color: #FFF8DC !important;
        border-radius: 10px !important;
        border: 1px solid #F4C430 !important;
        color: #2C3E2D !important;
        font-weight: bold !important;
    }
    
    /* Tarjetas personalizadas */
    .custom-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #F4C430;
        border-right: 2px solid #EBF3E8;
        border-top: 2px solid #EBF3E8;
        border-bottom: 2px solid #EBF3E8;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    
    .divider-custom {
        text-align: center;
        margin: 1.5rem 0;
        font-size: 1.4rem;
        letter-spacing: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BARRA LATERAL (API KEY Y CONFIGURACIÓN)
# ==========================================
with st.sidebar:
    st.markdown("## 🌻 Configuración 🐢")
    st.markdown("Bienvenido al planificador de citas a paso lento pero seguro, buscando siempre el sol.")
    
    api_key = st.text_input(
        "🔑 Tu API Key de Google Gemini:",
        type="password",
        help="Pega aquí tu clave gratuita obtenida en aistudio.google.com"
    )
    
    st.markdown("""
    <div style="background-color: #FFFDF5; padding: 12px; border-radius: 10px; border: 1px dashed #4A7C59; font-size: 0.88rem;">
        <b>¿Cómo conseguir tu API Key gratis?</b><br>
        1. Entra a <a href="https://aistudio.google.com/apikey" target="_blank">Google AI Studio</a>.<br>
        2. Inicia sesión con tu cuenta de Google.<br>
        3. Haz clic en <b>Create API Key</b> y cópiala aquí. ¡Es 100% gratis! 🌻
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider-custom'>🌻🐢🌻</div>", unsafe_allow_html=True)
    st.markdown("### 🤖 El Consejo de IAs:")
    st.markdown("""
    - **🌻 Agente 1 (Romántico Creativo):** Diseña paseos mágicos, atmósfera y detalles especiales.
    - **🍽️ Agente 2 (Crítico Gastronómico):** Selecciona las mejores propuestas culinarias para cada comida.
    - **🐢 Agente 3 (Juez Tortuga Sabia):** Une ambos mundos y estructura el itinerario final en 3 presupuestos.
    """)

# ==========================================
# 3. ENCABEZADO Y FORMULARIO DE ENTRADA
# ==========================================
st.markdown("<h1 style='text-align: center;'>🌻 Planificador de Citas: Girasoles y Tortugas 🐢</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.15rem; color: #4A7C59;'><i>Porque los mejores momentos se disfrutan sin prisa 🐢 y mirando hacia la luz 🌻</i></p>", unsafe_allow_html=True)
st.markdown("<div class='divider-custom'>🌻🐢🌻🐢🌻</div>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        idea_usuario = st.text_area(
            "🌻 ¿Cuál es su idea, zona o antojo para la cita?",
            placeholder="Ej: Queremos ir a comer pastas caseras el sábado por una zona tranquila con árboles, o pasear cerca del río...",
            height=120
        )
        
    with col2:
        fecha_cita = st.date_input(
            "🐢 ¿Qué día será la cita?",
            value=datetime.date.today() + datetime.timedelta(days=1)
        )
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_nombre = dias_semana[fecha_cita.weekday()]
        st.caption(f"✨ Día seleccionado: **{dia_nombre} ({fecha_cita.strftime('%d/%m/%Y')})**")
        
        sugerencia_completa = st.checkbox("🌻 Sugerencia de Día Completo (Incluir todas las comidas)", value=True)
        
        if sugerencia_completa:
            comidas_seleccionadas = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
            st.multiselect(
                "🍽️ Comidas incluidas:",
                options=["Desayuno", "Almuerzo", "Merienda", "Cena"],
                default=["Desayuno", "Almuerzo", "Merienda", "Cena"],
                disabled=True
            )
        else:
            comidas_seleccionadas = st.multiselect(
                "🍽️ Elige qué comidas incluir:",
                options=["Desayuno", "Almuerzo", "Merienda", "Cena"],
                default=["Almuerzo", "Cena"]
            )

st.write("")
boton_planificar = st.button("🌻🐢 ¡Convocar al Consejo de IAs y Armar Itinerario! 🐢🌻")

# ==========================================
# 4. LÓGICA MULTI-AGENTE ("CONSENSO DE IAs")
# ==========================================
def llamar_agente(client, system_prompt, user_prompt):
    """Ejecuta una llamada al modelo Gemini 2.5 Flash con instrucciones de sistema."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.75,
        )
    )
    return response.text

if boton_planificar:
    if not api_key:
        st.warning("🐢 ¡Alto ahí, pequeña tortuga! Por favor ingresa tu API Key gratuita de Google Gemini en la barra lateral izquierda para despertar a los agentes. 🌻")
    elif not idea_usuario.strip():
        st.warning("🌻 Por favor escribe alguna idea, zona, ciudad o antojo en el campo de texto para que las IAs puedan inspirarse.")
    elif not comidas_seleccionadas:
        st.warning("🍽️ Selecciona al menos una comida (o marca 'Sugerencia de Día Completo') para armar el recorrido.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            comidas_str = ", ".join(comidas_seleccionadas)
            contexto_base = (
                f"Pedido/Zona/Antojo de la pareja: '{idea_usuario}'.\n"
                f"Día de la cita: {dia_nombre} ({fecha_cita.strftime('%d/%m/%Y')}).\n"
                f"Comidas que deben incluirse obligatoriamente: {comidas_str}."
            )

            # Barra de progreso y estado interactivo
            with st.status("🌻🐢 El Consejo de IAs está deliberando tu cita perfecta...", expanded=True) as status:
                
                # --- AGENTE 1: EL ROMÁNTICO CREATIVO ---
                st.write("🌻 **Turno 1:** *El Romántico Creativo* está diseñando paseos, actividades y sorpresas...")
                sys_agente_1 = (
                    "Eres 'El Romántico Creativo' 🌻. Tu especialidad es diseñar experiencias inolvidables en pareja, "
                    "paseos con encanto, actividades originales (mañana, tarde y noche), miradores, jardines, juegos de conversación "
                    "y pequeños gestos románticos. Propón ideas adaptables a tres niveles de presupuesto (Bajo, Medio y Alto) "
                    "que conecten con la zona o antojo del usuario."
                )
                propuesta_romantica = llamar_agente(
                    client,
                    sys_agente_1,
                    f"Analiza este pedido y propón actividades y paseos románticos para mañana, tarde y noche:\n{contexto_base}"
                )

                # --- AGENTE 2: EL CRÍTICO GASTRONÓMICO ---
                st.write("🍽️ **Turno 2:** *El Crítico Gastronómico* está seleccionando al menos 2 opciones por comida...")
                sys_agente_2 = (
                    "Eres 'El Crítico Gastronómico' 🍽️🌻. Tu especialidad es recomendar lugares específicos o conceptos gastronómicos "
                    "detallados, platos estrella y maridajes para citas románticas. Para CADA comida solicitada "
                    f"({comidas_str}), debes proponer AL MENOS 2 OPCIONES distintas dentro de cada nivel de presupuesto "
                    "(Presupuesto Bajo, Presupuesto Medio y Presupuesto Alto), respetando el antojo y la ubicación del usuario."
                )
                propuesta_gastronomica = llamar_agente(
                    client,
                    sys_agente_2,
                    f"Analiza este pedido y propón las opciones gastronómicas detalladas para {comidas_str}:\n{contexto_base}"
                )

                # --- AGENTE 3: EL JUEZ TORTUGA SABIA ---
                st.write("🐢 **Turno 3:** *El Juez Tortuga Sabia* está evaluando ambas propuestas y sellando el consenso final...")
                sys_agente_3 = (
                    "Eres 'El Juez Tortuga Sabia' 🐢🌻, el mediador supremo de las citas románticas. "
                    "Tu trabajo es leer las propuestas de 'El Romántico Creativo' y 'El Crítico Gastronómico', llegar a un consenso "
                    "armonioso y redactar el itinerario definitivo de día completo.\n\n"
                    "REGLA DE FORMATO ESTRICTA E INQUEBRANTABLE:\n"
                    "Debes dividir tu respuesta en EXACTAMENTE 4 bloques separados por la etiqueta exacta `===SEPARADOR_TORTUGA===`.\n"
                    "- BLOQUE 1: Un breve veredicto sabio y tierno (máximo 1 párrafo) explicando cómo fusionaste las ideas de ambos agentes.\n"
                    "- BLOQUE 2: El itinerario completo para **🐢 Presupuesto Bajo (Económico y encantador)**.\n"
                    "- BLOQUE 3: El itinerario completo para **🌻 Presupuesto Medio (Equilibrado)**.\n"
                    "- BLOQUE 4: El itinerario completo para **✨ Presupuesto Alto (Lujo / Especial)**.\n\n"
                    "Dentro de CADA presupuesto (Bloques 2, 3 y 4) DEBES incluir:\n"
                    "1. Cronograma dividido en **🌅 Mañana**, **☀️ Tarde** y **🌙 Noche**.\n"
                    f"2. Para cada comida seleccionada ({comidas_str}), incluye **Opción A** y **Opción B** (al menos 2 opciones de lugares o propuestas gastronómicas concretas con platos recomendados y rango de precios estimado).\n"
                    "3. Al menos 2 opciones de paseos o actividades románticas integradas en el horario.\n"
                    "4. Un '🐢 Consejo de la Tortuga Sabia' al final de cada presupuesto."
                )
                prompt_juez = (
                    f"DATOS DEL USUARIO:\n{contexto_base}\n\n"
                    f"--- PROPUESTA DEL AGENTE 1 (ROMÁNTICO CREATIVO) ---\n{propuesta_romantica}\n\n"
                    f"--- PROPUESTA DEL AGENTE 2 (CRÍTICO GASTRONÓMICO) ---\n{propuesta_gastronomica}\n\n"
                    "Recuerda separar los 4 bloques exactamente con el texto: ===SEPARADOR_TORTUGA==="
                )
                consenso_final = llamar_agente(client, sys_agente_3, prompt_juez)

                status.update(label="🌻🐢 ¡Consenso alcanzado! Aquí tienes tu itinerario romántico.", state="complete", expanded=False)

            # ==========================================
            # 5. DESPLEGABLE CON EL DEBATE INTERNO
            # ==========================================
            st.markdown("<div class='divider-custom'>🌻🐢🌻</div>", unsafe_allow_html=True)
            
            with st.expander("🔍 Ver el Debate Interno del Consejo de IAs (Cómo se pusieron de acuerdo) 🌻🐢"):
                col_deb1, col_deb2 = st.columns(2)
                with col_deb1:
                    st.markdown("### 🌻 Agente 1: El Romántico Creativo")
                    st.info(propuesta_romantica)
                with col_deb2:
                    st.markdown("### 🍽️ Agente 2: El Crítico Gastronómico")
                    st.success(propuesta_gastronomica)
                
                partes = consenso_final.split("===SEPARADOR_TORTUGA===")
                if len(partes) >= 1:
                    st.markdown("### 🐢🌻 Veredicto del Agente 3 (El Juez Tortuga Sabia)")
                    st.warning(partes[0].strip())

            # ==========================================
            # 6. SALIDA EN PESTAÑAS (3 PRESUPUESTOS)
            # ==========================================
            st.markdown("## 🌻 Tu Itinerario de Cita Consensuado 🐢")
            st.caption(f"Plan diseñado para el **{dia_nombre} {fecha_cita.strftime('%d/%m/%Y')}** • Comidas incluidas: **{comidas_str}**")

            tab_bajo, tab_medio, tab_alto = st.tabs([
                "🐢 Presupuesto Bajo (Económico y encantador)",
                "🌻 Presupuesto Medio (Equilibrado)",
                "✨ Presupuesto Alto (Lujo / Especial)"
            ])

            if len(partes) >= 4:
                with tab_bajo:
                    st.markdown(f"<div class='custom-card'>{partes[1].strip()}</div>", unsafe_allow_html=True)
                with tab_medio:
                    st.markdown(f"<div class='custom-card'>{partes[2].strip()}</div>", unsafe_allow_html=True)
                with tab_alto:
                    st.markdown(f"<div class='custom-card'>{partes[3].strip()}</div>", unsafe_allow_html=True)
            else:
                # Fallback seguro por si el modelo omite algún separador
                with tab_bajo:
                    st.markdown(consenso_final)
                with tab_medio:
                    st.info("🌻 Revisa la primera pestaña para ver el documento unificado del Juez Tortuga.")
                with tab_alto:
                    st.info("✨ Revisa la primera pestaña para ver el documento unificado del Juez Tortuga.")

        except Exception as e:
            st.error(f"🐢 Ups, ocurrió un error al conectar con la API: {e}")
            st.info("Verifica que tu API Key de Google AI Studio esté bien copiada y sin espacios extra.")