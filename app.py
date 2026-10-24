import streamlit as st
from google import genai
from google.genai import types
import datetime

st.set_page_config(
    page_title="Citas Girasol & Tortuga 🌻🐢",
    page_icon="🌻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Tomamos tu clave de Google Cloud que ya tiene facturación habilitada
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    API_KEY = ""

st.markdown("""
<style>
    .stApp { background-color: #FFFDF7; color: #2C3E2D; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    .titulo-principal { text-align: center; color: #3A5F43; font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; }
    .subtitulo { text-align: center; color: #6B8E78; font-size: 1rem; margin-bottom: 1.8rem; }
    .stButton > button { background-color: #F4C430 !important; color: #2C3E2D !important; border: 2px solid #3A5F43 !important; border-radius: 14px !important; padding: 0.75rem 1.5rem !important; font-weight: 700 !important; font-size: 1.05rem !important; width: 100%; transition: 0.2s ease-in-out; }
    .stButton > button:hover { background-color: #3A5F43 !important; color: #FFFDF7 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #EBF3E8; border-radius: 10px; padding: 8px 16px; color: #2C3E2D; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #F4C430 !important; color: #2C3E2D !important; border-bottom: 3px solid #3A5F43 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='titulo-principal'>🌻 Planificador de Citas 🐢</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Armamos tu día ideal a fuego lento, con 3 presupuestos a medida</div>", unsafe_allow_html=True)

with st.container(border=True):
    idea_usuario = st.text_input("🌻 1. ¿Qué tienen ganas de hacer o comer, y por qué zona?", placeholder="Ej: Comer pastas el sábado por una zona linda con árboles...")
    fecha_cita = st.date_input("🐢 2. ¿Qué día?", value=datetime.date.today() + datetime.timedelta(days=1))
    comidas = st.multiselect("🍽️ 3. ¿Qué comidas incluimos?", options=["Desayuno", "Almuerzo", "Merienda", "Cena"], default=["Desayuno", "Almuerzo", "Merienda", "Cena"])
    st.write("")
    planificar = st.button("🌻 Armar mi cita ideal 🐢")

def consultar_ia(client, rol_sistema, mensaje):
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=mensaje,
        config=types.GenerateContentConfig(
            system_instruction=rol_sistema,
            temperature=0.7,
        )
    )
    return resp.text

if planificar:
    if not API_KEY or not API_KEY.startswith("AQ."):
        st.error("🔑 Asegurate de poner tu clave oficial de Google (la que empieza con AQ.) en GEMINI_API_KEY dentro de los Secrets.")
    elif not idea_usuario.strip():
        st.warning("🌻 Escribe una breve idea o antojo arriba para empezar.")
    elif not comidas:
        st.warning("🐢 Elige al menos una comida de la lista.")
    else:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia_str = f"{dias[fecha_cita.weekday()]} {fecha_cita.strftime('%d/%m')}"
        comidas_str = ", ".join(comidas)
        pedido = f"Idea/Zona: {idea_usuario} | Día: {dia_str} | Comidas: {comidas_str}"

        try:
            # Conexión directa a Google Cloud con tu clave habilitada
            client = genai.Client(vertexai=True, api_key=API_KEY)

            with st.spinner("🌻🐢 Conectando con Gemini Premium..."):
                paseos = consultar_ia(client, "Eres 'El Romántico Creativo' 🌻. Propón paseos breves y encantadores (mañana, tarde y noche) para presupuestos bajo, medio y alto.", pedido)
                lugares = consultar_ia(client, f"Eres 'El Crítico Gastronómico' 🍽️. Propón 2 opciones concretas de lugares o menús por cada comida ({comidas_str}) para presupuesto bajo, medio y alto.", pedido)
                
                instruccion_juez = (
                    "Eres 'El Juez Tortuga Sabia' 🐢🌻. Une las ideas en un itinerario súper claro, breve y fácil de leer.\n"
                    "Separa tu respuesta en EXACTAMENTE 4 partes usando el texto exacto `===SEP===`:\n"
                    "Parte 1: Resumen de 2 líneas de cómo se pusieron de acuerdo.\n"
                    "Parte 2: Itinerario Presupuesto Bajo.\n"
                    "Parte 3: Itinerario Presupuesto Medio.\n"
                    "Parte 4: Itinerario Presupuesto Alto.\n\n"
                    "REGLA VISUAL PARA CADA PRESUPUESTO: Usa viñetas cortas y claras:\n"
                    "- **🌅 Mañana**, **☀️ Tarde** y **🌙 Noche**.\n"
                    f"- En cada comida ({comidas_str}), pon **Opción 1** y **Opción 2** con una descripción de 1 sola línea.\n"
                    "- Nada de textos largos; debe leerse de un vistazo."
                )
                consenso = consultar_ia(client, instruccion_juez, f"Pedido: {pedido}\nPaseos: {paseos}\nComidas: {lugares}\nUsa ===SEP=== entre las 4 partes.")

            partes = consenso.split("===SEP===")

            st.write("")
            st.markdown("### ✨ Elige tu nivel de presupuesto:")
            tab_bajo, tab_medio, tab_alto = st.tabs(["🐢 Bajo (Económico)", "🌻 Medio (Equilibrado)", "✨ Alto (Especial)"])

            if len(partes) >= 4:
                with tab_bajo:
                    with st.container(border=True): st.markdown(partes[1].strip())
                with tab_medio:
                    with st.container(border=True): st.markdown(partes[2].strip())
                with tab_alto:
                    with st.container(border=True): st.markdown(partes[3].strip())
            else:
                with tab_bajo: st.markdown(consenso)

            with st.expander("🐢 Ver cómo debatieron las 3 IAs (Opcional)"):
                if len(partes) >= 1: st.caption("**Veredicto de la Tortuga Sabia:** " + partes[0].strip())
                st.info(f"**🌻 Idea de Paseos:**\n\n{paseos}")
                st.success(f"**🍽️ Idea Gastronómica:**\n\n{lugares}")

        except Exception as e:
            st.error("⚠️ Error de conexión.")
            st.caption(f"Detalle técnico: {e}")
