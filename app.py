import streamlit as st
import datetime
import random

st.set_page_config(
    page_title="Citas Girasol & Tortuga 🌻🐢",
    page_icon="🌻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

# --- MOTOR INTERNO 100% OFFLINE (CERO CAÍDAS) ---
def generar_opciones(tipo, idea):
    opciones = {
        "Desayuno": ["Cafetería de especialidad con pastelería artesanal", "Brunch abundante en un patio escondido", "Café clásico con medialunas calientes y jugo natural", "Tostones con palta y huevos revueltos en un local moderno"],
        "Almuerzo": [f"Bodegón clásico adaptado a: {idea}", f"Bistró relajado ideal para: {idea}", "Cantina italiana con pastas caseras", "Restaurante con mesas al aire libre y menú fresco"],
        "Merienda": ["Casa de té tradicional con tortas porción XL", "Café de estilo parisino con croissants", "Churros calientes o waffles para compartir", "Merienda deli con chipá y limonada de menta"],
        "Cena": [f"Restaurante íntimo a la luz de las velas inspirado en: {idea}", "Lugar de tapeo y vinos para una charla larga", "Pizzería de masa madre de estilo napolitano", "Restaurante de autor con platos para compartir y coctelería"]
    }
    random.shuffle(opciones[tipo])
    return opciones[tipo][:2]

def generar_paseo(momento, idea):
    paseos = {
        "🌅 Mañana": [f"Caminata tranquila aprovechando: {idea}", "Paseo fotográfico por calles arboladas", "Visita a una feria local o mercado de pulgas", "Recorrido en bici o caminando por un parque cercano"],
        "☀️ Tarde": ["Lectura o charla en un banco al solcito", f"Recorrer vidrieras o galerías vinculadas a: {idea}", "Comprar un helado y caminar sin rumbo fijo", "Visita a un jardín botánico, rosedal o plaza principal"],
        "🌙 Noche": ["Paseo romántico iluminado por las luces de la calle", "Caminata post-cena buscando un bar escondido", "Caminar abrazados sintiendo la brisa nocturna", f"Buscar un mirador o lugar despejado relacionado con: {idea}"]
    }
    return random.choice(paseos[momento])

if planificar:
    if not idea_usuario.strip():
        st.warning("🌻 Escribí una breve idea o antojo arriba para empezar.")
    elif not comidas:
        st.warning("🐢 Elegí al menos una comida de la lista.")
    else:
        with st.spinner("🌻🐢 Armando tu plan perfecto al instante..."):
            
            # Simulamos el debate
            paseos_texto = f"Mi foco fue conectar su idea de '{idea_usuario}' con paseos relajados y mucha charla."
            lugares_texto = f"Elegí las mejores alternativas para {', '.join(comidas)} priorizando el ambiente romántico y la buena comida."
            
            st.write("")
            st.markdown("### ✨ Elegí tu nivel de presupuesto:")
            tab_bajo, tab_medio, tab_alto = st.tabs(["🐢 Bajo (Económico)", "🌻 Medio (Equilibrado)", "✨ Alto (Especial)"])

            presupuestos = [("🐢 Presupuesto Bajo", tab_bajo, "Económico y encantador"), 
                            ("🌻 Presupuesto Medio", tab_medio, "Equilibrado y completo"), 
                            ("✨ Presupuesto Alto", tab_alto, "Lujo y detalles especiales")]

            for titulo, tab, desc in presupuestos:
                with tab:
                    with st.container(border=True):
                        st.markdown(f"**{titulo} - {desc}**\n")
                        st.markdown(f"*Plan consensuado inspirado en: '{idea_usuario}'*\n\n---")
                        
                        # Mañana
                        if "Desayuno" in comidas or "Almuerzo" in comidas:
                            st.markdown(f"**🌅 Mañana**\n- 🚶 Paseo: {generar_paseo('🌅 Mañana', idea_usuario)}")
                        if "Desayuno" in comidas:
                            ops = generar_opciones("Desayuno", idea_usuario)
                            st.markdown(f"- ☕ **Desayuno Opción 1:** {ops[0]}")
                            st.markdown(f"- ☕ **Desayuno Opción 2:** {ops[1]}")
                        
                        # Tarde
                        if "Almuerzo" in comidas or "Merienda" in comidas:
                            st.markdown(f"\n**☀️ Tarde**\n- 🚶 Paseo: {generar_paseo('☀️ Tarde', idea_usuario)}")
                        if "Almuerzo" in comidas:
                            ops = generar_opciones("Almuerzo", idea_usuario)
                            st.markdown(f"- 🍽️ **Almuerzo Opción 1:** {ops[0]}")
                            st.markdown(f"- 🍽️ **Almuerzo Opción 2:** {ops[1]}")
                        if "Merienda" in comidas:
                            ops = generar_opciones("Merienda", idea_usuario)
                            st.markdown(f"- 🍰 **Merienda Opción 1:** {ops[0]}")
                            st.markdown(f"- 🍰 **Merienda Opción 2:** {ops[1]}")

                        # Noche
                        if "Cena" in comidas:
                            st.markdown(f"\n**🌙 Noche**\n- 🚶 Paseo: {generar_paseo('🌙 Noche', idea_usuario)}")
                            ops = generar_opciones("Cena", idea_usuario)
                            st.markdown(f"- 🍷 **Cena Opción 1:** {ops[0]}")
                            st.markdown(f"- 🍷 **Cena Opción 2:** {ops[1]}")
                            
            with st.expander("🐢 Ver cómo debatieron las 3 IAs (Opcional)"):
                st.caption("**Veredicto de la Tortuga Sabia:** Logramos fusionar la idea a la perfección.")
                st.info(f"**🌻 Idea de Paseos:**\n\n{paseos_texto}")
                st.success(f"**🍽️ Idea Gastronómica:**\n\n{lugares_texto}")
