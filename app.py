import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Martínez Prop - Premium", layout="wide", initial_sidebar_state="collapsed")

# ESTILO DARK PROFESIONAL
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    .stApp { background-color: #0b0f1a; color: #e2e8f0; }
    .titulo-header { font-size: 38px; font-weight: 800; color: #ffffff; margin-bottom: 5px; }
    .precio-destacado { font-size: 30px; color: #38bdf8; font-weight: 700; margin-bottom: 20px; }
    .card-dato { background: #161d2f; padding: 20px; border-radius: 12px; border: 1px solid #2d3748; text-align: center; }
    .label-dato { font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .valor-dato { font-size: 18px; font-weight: 600; color: #f8fafc; }
    .btn-wa { background-color: #22c55e; color: white !important; padding: 18px; border-radius: 12px; display: block; text-align: center; font-weight: 700; text-decoration: none; margin-top: 30px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

def motor_ninja_argenprop(url):
    # Lista de navegadores para rotar y evitar bloqueos
    agentes = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    headers = {
        'User-Agent': random.choice(agentes),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-AR,es;q=0.9',
        'Referer': 'https://www.google.com.ar/'
    }

    try:
        session = requests.Session()
        # Simula una pausa humana
        time.sleep(random.uniform(2, 4))
        response = session.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        data = {
            "titulo": "", "precio": "Consultar", "desc": "", 
            "fotos": [], "m2": "-", "amb": "-", "dor": "-", "ban": "-", "coch": "-"
        }

        # Extracción de datos (Lógica Argenprop 2026)
        data["titulo"] = soup.find('h1', class_='titlebar__title').get_text().strip() if soup.find('h1') else "Propiedad Martínez Prop"
        data["precio"] = soup.find('p', class_='titlebar__price').get_text().strip() if soup.find('p', class_='titlebar__price') else "Consultar"
        
        # Características técnicas
        items = soup.find_all('li', class_='property-main-features-item')
        for item in items:
            val = item.find('strong').get_text().strip()
            lbl = item.find('p').get_text().lower()
            if "totales" in lbl: data["m2"] = val
            if "ambientes" in lbl: data["amb"] = val
            if "dormitorios" in lbl: data["dor"] = val
            if "baños" in lbl: data["ban"] = val
            if "cocheras" in lbl: data["coch"] = val

        # Descripción
        desc_div = soup.find('div', class_='section-description__text')
        data["desc"] = desc_div.get_text(separator="\n").strip() if desc_div else ""

        # GALERÍA COMPLETA DE FOTOS
        # Buscamos todas las imágenes que Argenprop precarga
        for img in soup.find_all('img'):
            src = img.get('data-flickity-lazyload') or img.get('src')
            if src and 'static.argenprop' in src and src not in data["fotos"]:
                data["fotos"].append(src)

        return data
    except Exception:
        return None

# --- SISTEMA DE PÁGINAS ---
if "view" in st.query_params:
    # VISTA DE LA FICHA (LA QUE VE EL CLIENTE)
    d = st.session_state.get('prop')
    a = st.session_state.get('agente')
    
    if d:
        col_f, _, col_i = st.columns([2.2, 0.1, 1])
        with col_f:
            st.markdown(f"<h1 class='titulo-header'>{d['titulo']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p class='precio-destacado'>{d['precio']}</p>", unsafe_allow_html=True)
            
            # Fotos: Una grande y las demás en grilla
            if d['fotos']:
                st.image(d['fotos'][0], use_container_width=True)
                if len(d['fotos']) > 1:
                    st.markdown("### Galería de fotos")
                    cols_fotos = st.columns(3)
                    for idx, furl in enumerate(d['fotos'][1:10]): # Limitamos a 9 fotos extra
                        cols_fotos[idx % 3].image(furl, use_container_width=True)
            
            st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
            st.markdown(f"### Descripción\n{d['desc']}")

        with col_i:
            st.markdown(f"""
                <div style='background:#161d2f; padding:25px; border-radius:15px; border:1px solid #2d3748; position:sticky; top:20px;'>
                    <p style='color:#38bdf8; font-weight:800; font-size:12px; margin-bottom:5px;'>CONTACTO</p>
                    <h2 style='margin:0; color:white;'>{a['nombre']}</h2>
                    <p style='color:#94a3b8;'>Martínez Propiedades</p>
                    <hr style='border:0; border-top:1px solid #2d3748; margin:20px 0;'>
                    <div style='display:grid; gap:10px;'>
                        <div class='card-dato'><span class='label-dato'>Sup. Total</span><br><span class='valor-dato'>{d['m2']}</span></div>
                        <div class='card-dato'><span class='label-dato'>Ambientes</span><br><span class='valor-dato'>{d['amb']}</span></div>
                        <div class='card-dato'><span class='label-dato'>Dormitorios</span><br><span class='valor-dato'>{d['dor']}</span></div>
                    </div>
                    <a href="https://wa.me/{a['wa']}?text=Hola,%20me%20interesa%20esta%20propiedad" class="btn-wa">CONSULTAR AHORA</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button("⬅️ VOLVER AL PANEL"):
                st.query_params.clear()
                st.rerun()

else:
    # PANEL DE CONTROL (SOLO PARA VOS)
    st.title("🥷 Martínez Prop - Automatizador V3")
    st.markdown("Ingresá la URL de Argenprop para generar la ficha automáticamente.")
    
    ag_nom = st.text_input("Nombre del Agente", "Virginia Lincuiz")
    ag_cel = st.text_input("WhatsApp (ej: 5492213184015)", "5492213184015")
    
    url_input = st.text_input("URL de la propiedad:")
    
    if st.button("🚀 GENERAR FICHA AUTOMÁTICA"):
        with st.spinner("Infiltrando portal y descargando fotos..."):
            resultado = motor_ninja_argenprop(url_input)
            if resultado:
                st.session_state.prop = resultado
                st.session_state.agente = {"nombre": ag_nom, "wa": ag_cel}
                st.query_params["view"] = "ficha"
                st.rerun()
            else:
                st.error("Argenprop bloqueó el acceso. Intentá nuevamente en 5 segundos o usá otra URL.")
