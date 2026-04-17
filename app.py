import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ficha Inmobiliaria | Martínez Prop", layout="wide", initial_sidebar_state="collapsed")

# 2. DISEÑO CSS PROFESIONAL (ESTILO PROPIO FICHAS)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    body { background-color: #f7fafc; }
    .stApp { max-width: 1200px; margin: 0 auto; background-color: white; }
    
    /* Contenedor Ficha */
    .main-container { padding: 40px; }
    .header-prop { margin-bottom: 30px; }
    .titulo-prop { font-size: 36px; font-weight: 800; color: #1a202c; line-height: 1.1; margin-bottom: 10px; }
    .precio-prop { font-size: 32px; color: #2b6cb0; font-weight: 700; }
    
    /* Grilla de Datos */
    .data-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 20px; margin: 30px 0; }
    .data-card { background: #f1f5f9; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0; }
    .data-label { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700; margin-bottom: 5px; display: block; }
    .data-value { font-size: 18px; font-weight: 600; color: #1e293b; }

    /* Descripción */
    .section-title { font-size: 22px; font-weight: 700; color: #1e293b; margin-top: 40px; padding-bottom: 10px; border-bottom: 2px solid #edf2f7; margin-bottom: 20px; }
    .description-text { font-size: 17px; line-height: 1.8; color: #4a5568; white-space: pre-wrap; }

    /* Card de Contacto Lateral */
    .contact-sidebar { background: white; border: 1px solid #e2e8f0; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); position: sticky; top: 40px; }
    .wa-button { background-color: #25d366; color: white !important; padding: 16px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: 700; font-size: 16px; margin-top: 20px; transition: 0.3s; }
    .wa-button:hover { background-color: #128c7e; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

def extraer_datos_profesionales(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'es-AR,es;q=0.9'
    }
    try:
        time.sleep(random.uniform(1, 2))
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200: return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        d = {"titulo": "", "precio": "Consultar", "desc": "", "fotos": [], "ambientes": "-", "dormitorios": "-", "banos": "-", "m2_totales": "-", "cochera": "No"}

        if "argenprop.com" in url:
            d["titulo"] = soup.find('h1', class_='titlebar__title').text.strip() if soup.find('h1') else "Propiedad Martínez Prop"
            d["precio"] = soup.find('p', class_='titlebar__price').text.strip() if soup.find('p', class_='titlebar__price') else "Consultar"
            
            # Características técnicas
            for item in soup.find_all('li', class_='property-main-features-item'):
                val = item.find('strong').text.strip()
                lbl = item.find('p').text.lower()
                if "totales" in lbl: d["m2_totales"] = val
                if "ambientes" in lbl: d["ambientes"] = val
                if "dormitorios" in lbl: d["dormitorios"] = val
                if "baños" in lbl: d["banos"] = val
                if "cocheras" in lbl: d["cochera"] = val

            desc_div = soup.find('div', class_='section-description__text')
            d["desc"] = desc_div.get_text(separator="\n").strip() if desc_div else ""
            
            for img in soup.find_all('img'):
                src = img.get('data-flickity-lazyload') or img.get('src')
                if src and 'static.argenprop' in src and src not in d["fotos"]:
                    d["fotos"].append(src)
        return d
    except:
        return None

# --- NAVEGACIÓN ---
params = st.query_params
if "view" in params:
    # VISTA CLIENTE
    d = st.session_state.get('p_data', {})
    a = st.session_state.get('a_data', {"nombre": "Virginia Lincuiz", "wa": "5492213184015"})
    
    col_content, col_spacer, col_sidebar = st.columns([2.3, 0.1, 1])
    
    with col_content:
        st.markdown(f"<div class='header-prop'><h1 class='titulo-prop'>{d['titulo']}</h1><p class='precio-prop'>{d['precio']}</p></div>", unsafe_allow_html=True)
        if d['fotos']:
            st.image(d['fotos'][0], use_container_width=True)
            if len(d['fotos']) > 1:
                fcols = st.columns(3)
                for i, furl in enumerate(d['fotos'][1:4]):
                    fcols[i].image(furl, use_container_width=True)
        
        st.markdown(f"""
            <div class='data-grid'>
                <div class='data-card'><span class='data-label'>Sup. Total</span><span class='data-value'>{d['m2_totales']}</span></div>
                <div class='data-card'><span class='data-label'>Ambientes</span><span class='data-value'>{d['ambientes']}</span></div>
                <div class='data-card'><span class='data-label'>Dormitorios</span><span class='data-value'>{d['dormitorios']}</span></div>
                <div class='data-card'><span class='data-label'>Baños</span><span class='data-value'>{d['banos']}</span></div>
                <div class='data-card'><span class='data-label'>Cochera</span><span class='data-value'>{d['cochera']}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>Descripción</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='description-text'>{d['desc']}</div>", unsafe_allow_html=True)

    with col_sidebar:
        st.markdown(f"""
            <div class='contact-sidebar'>
                <p style='color:#2b6cb0; font-weight:800; font-size:12px; text-transform:uppercase;'>Contacto Agente</p>
                <h3 style='margin-bottom:5px;'>{a['nombre']}</h3>
                <p style='color:#718096; font-size:14px;'>Martínez Propiedades</p>
                <hr style='border:0; border-top:1px solid #edf2f7; margin:20px 0;'>
                <p style='font-size:15px;'>Hacé clic para coordinar una visita o recibir más información de esta unidad.</p>
                <a href="https://wa.me/{a['wa']}?text=Hola%20{a['nombre']},%20consulto%20por:%20{d['titulo']}" class="wa-button">SOLICITAR INFORMACIÓN</a>
            </div>
        """, unsafe_allow_html=True)
        if st.button("⬅️ Crear otra ficha"):
            st.query_params.clear()
            st.rerun()
else:
    # PANEL CONTROL
    st.title("🏠 Generador Martínez Prop")
    nom = st.text_input("Tu Nombre", "Virginia Lincuiz")
    cel = st.text_input("Tu WhatsApp", "5492213184015")
    url = st.text_input("Link de Argenprop:")
    if st.button("🚀 GENERAR FICHA PROFESIONAL"):
        with st.spinner("Infiltrando portal..."):
            res = extraer_datos_profesionales(url)
            if res:
                st.session_state.p_data = res
                st.session_state.a_data = {"nombre": nom, "wa": cel}
                st.query_params["view"] = "ficha"
                st.rerun()
            else:
                st.error("Bloqueo de seguridad detectado. Subí la app a internet para solucionar esto.")
