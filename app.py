import streamlit as st
from google import genai
from google.genai import types
import datetime

# ==========================================
# 1. CONFIGURACIÓN Y API KEY DESDE SECRETS
# ==========================================
st.set_page_config(
    page_title="Citas Girasol & Tortuga 🌻🐢",
    page_icon="🌻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Lee la clave directamente de los Secrets de Streamlit sin usar variables borradas
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = ""

# ==========================================
# 2. ESTÉTICA LIMPIA Y MINIMALISTA (CSS)
# ==========================================
st.markdown("""
<style>
    .stApp {
        background-color: #FFFDF7;
        color: #2C3E2D;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}
    
    .titulo-principal {
        text-align: center;
        color: #3A5F43;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitulo {
        text-align: center;
        color: #6B8E78;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }
    
    .stButton > button {
        background-color: #F4C430 !important;
        color: #2C3E2D !important;
        border: 2px solid #3A5F43 !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        width: 100%;
        transition: 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #3A5F43 !important;
        color: #FFFDF7 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #EBF3E8;
        border-radius: 10px;
        padding: 8px 16px;
        color: #2C3E2D;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F4C430 !important;
        color: #2C3E2D !important;
        border-bottom: 3px solid #3A5F43 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. INTERFAZ SIMPLE (SOLO LO ESENCIAL)
# ==========================================
st.markdown("<div class='titulo-principal'>🌻 Planificador de Citas 🐢</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitulo'>Armamos tu día ideal a fuego lento, con 3 presupuestos a medida</div>", unsafe_allow_html=True)

with st.container(border=True):
    idea_usuario = st.text_input(
        "🌻 1. ¿Qué tienen ganas de hacer o comer, y por qué zona?",
        placeholder="Ej: Comer pastas el sábado por una zona linda con árboles..."
    )
    
    col
