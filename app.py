import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ficha Inmobiliaria | Martínez Prop", layout="wide", initial_sidebar_state="collapsed")

# 2. DISEÑO CSS DARK MODE
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    .main-container { padding: 40px; }
    .titulo-prop { font-size: 36px; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 10px; }
    .precio-prop { font-size: 32px; color: #38bdf8; font-weight: 700; }
    .data-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 20px; margin: 30px 0; }
    .data-card { background: #1e293b; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #334155; }
    .data-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 700; margin-bottom: 5px; display: block; }
    .data-value { font-size: 18px; font-weight: 600; color: #f1f5f9; }
    .section-title { font-size: 22px; font-weight: 700; color: #ffffff; margin-top: 40px; padding-bottom: 10px; border-bottom: 2px solid #334155; margin-bottom: 20px; }
    .description-text { font-size: 17px; line-height: 1.8; color: #cbd5e1; white-space: pre-wrap; }
    .contact-sidebar { background: #1e293b; border: 1px solid #334155; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); position: sticky; top: 40px; }
    .wa-button { background-color: #22c55e; color: white !important; padding: 16px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: 700; font-size: 16px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

def extraer_datos_profesionales(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    try:
        time.sleep(1)
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200: return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        d = {"titulo": "", "precio": "", "desc": "", "fotos": [], "ambientes": "-", "dormitorios": "-", "banos": "-", "m2_totales": "-", "cochera": "-"}
        if "argenprop.com" in url:
            d["titulo"] = soup.find('h1').text.strip() if soup.find('h1') else ""
            d["precio"] = soup.find('p', class_='titlebar__price').text.strip() if soup.find('p', class_='titlebar__price') else ""
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
                if src and 'static.argenprop' in src and src not in d["fotos"]: d["fotos"].append(src)
        return d
    except: return None

# --- LÓGICA DE NAVEGACIÓN ---
if "view" in st.query_params:
    d = st.session_state.get('p_data')
    a = st.session_state.get('a_data')
    
    col_content, _, col_sidebar = st.columns([2.3, 0.1, 1])
    with col_content:
        st.markdown(f"<div class='header-prop'><h1 class='titulo-prop'>{d['titulo']}</h1><p class='precio-prop'>{d['precio']}</p></div>", unsafe_allow_html=True)
        if d['fotos']:
            st.image(d['fotos'][0], use_container_width=True)
            if len(d['fotos']) > 1:
                cols = st.columns(min(len(d['fotos'])-1, 3))
                for i, furl in enumerate(d['fotos'][1:4]):
                    cols[i].image(furl, use_container_width=True)
        st.markdown(f"<div class='data-grid'><div class='data-card'><span class='data-label'>Sup. Total</span><span class='data-value'>{d['m2_totales']}</span></div><div class='data-card'><span class='data-label'>Ambientes</span><span class='data-value'>{d['ambientes']}</span></div><div class='data-card'><span class='data-label'>Dormitorios</span><span class='data-value'>{d['dormitorios']}</span></div><div class='data-card'><span class='data-label'>Baños</span><span class='data-value'>{d['banos']}</span></div><div class='data-card'><span class='data-label'>Cochera</span><span class='data-value'>{d['cochera']}</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Descripción</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='description-text'>{d['desc']}</div>", unsafe_allow_html=True)
    with col_sidebar:
        st.markdown(f"<div class='contact-sidebar'><p style='color:#38bdf8; font-weight:800; font-size:12px; text-transform:uppercase;'>Contacto Agente</p><h3 style='color:white;'>{a['nombre']}</h3><p style='color:#94a3b8; font-size:14px;'>Martínez Propiedades</p><hr style='border:0; border-top:1px solid #334155; margin:20px 0;'><a href='https://wa.me/{a['wa']}?text=Consulta%20por%20{d['titulo']}' class='wa-button'>WHATSAPP</a></div>", unsafe_allow_html=True)
        if st.button("⬅️ Volver"):
            st.query_params.clear()
            st.rerun()
else:
    st.title("🏠 Martínez Prop | Panel")
    nom = st.text_input("Tu Nombre", "Virginia Lincuiz")
    cel = st.text_input("Tu WhatsApp", "5492213184015")
    
    tab1, tab2 = st.tabs(["🚀 Automático", "📝 Manual (Recomendado si falla)"])
    
    with tab1:
        url = st.text_input("Link de Argenprop:")
        if st.button("GENERAR AUTOMÁTICO"):
            res = extraer_datos_profesionales(url)
            if res:
                st.session_state.p_data, st.session_state.a_data = res, {"nombre": nom, "wa": cel}
                st.query_params["view"] = "ficha"; st.rerun()
            else: st.error("Portal bloqueado. Usá la pestaña 'Manual' aquí al lado ➔")
            
    with tab2:
        st.info("Copiá y pegá los datos del aviso original.")
        t_m = st.text_input("Título")
        p_m = st.text_input("Precio")
        f_m = st.text_input("Link de la Foto (Clic derecho en la foto > Copiar dirección de imagen)")
        desc_m = st.text_area("Descripción")
        c1, c2, c3 = st.columns(3)
        m2_m = c1.text_input("m2 Totales")
        amb_m = c2.text_input("Ambientes")
        dor_m = c3.text_input("Dormitorios")
        if st.button("GENERAR FICHA PROFESIONAL"):
            st.session_state.p_data = {"titulo": t_m, "precio": p_m, "desc": desc_m, "fotos": [f_m] if f_m else [], "m2_totales": m2_m, "ambientes": amb_m, "dormitorios": dor_m, "banos": "-", "cochera": "-"}
            st.session_state.a_data = {"nombre": nom, "wa": cel}
            st.query_params["view"] = "ficha"; st.rerun()
