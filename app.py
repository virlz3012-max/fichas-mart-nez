import streamlit as st
import requests
from bs4 import BeautifulSoup

# CONFIGURACIÓN
st.set_page_config(page_title="Martínez Prop - Ficha", layout="wide")

# ESTILO DARK (Para no quemar los ojos)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    .stApp { background-color: #0b0f1a; color: #e2e8f0; }
    .titulo-ficha { font-size: 40px; font-weight: 800; color: white; margin-bottom: 0px; }
    .precio-ficha { font-size: 32px; color: #38bdf8; font-weight: 700; margin-bottom: 20px; }
    .grid-datos { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 15px; margin: 20px 0; }
    .caja-dato { background: #161d2f; padding: 15px; border-radius: 10px; border: 1px solid #2d3748; text-align: center; }
    .dato-label { font-size: 10px; color: #94a3b8; text-transform: uppercase; }
    .dato-valor { font-size: 16px; font-weight: 600; color: white; }
    .btn-whatsapp { background-color: #22c55e; color: white !important; padding: 18px; border-radius: 12px; display: block; text-align: center; font-weight: 700; text-decoration: none; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# LÓGICA DE EXTRACCIÓN
def extraer_datos(url):
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'}
    try:
        r = requests.get(url, headers=h, timeout=10)
        if r.status_code != 200: return None
        s = BeautifulSoup(r.text, 'html.parser')
        d = {"t": "", "p": "", "desc": "", "imgs": [], "m2": "-", "amb": "-", "dor": "-"}
        
        if "argenprop.com" in url:
            d["t"] = s.find('h1').text.strip() if s.find('h1') else "Propiedad"
            d["p"] = s.find('p', class_='titlebar__price').text.strip() if s.find('p', class_='titlebar__price') else ""
            d["desc"] = s.find('div', class_='section-description__text').get_text(separator="\n").strip() if s.find('div', class_='section-description__text') else ""
            for img in s.find_all('img'):
                src = img.get('data-flickity-lazyload') or img.get('src')
                if src and 'static.argenprop' in src and src not in d["imgs"]: d["imgs"].append(src)
        return d
    except: return None

# --- VISTAS ---
if "ficha" in st.session_state:
    # ESTA ES LA PÁGINA QUE VE EL CLIENTE
    f = st.session_state.ficha
    a = st.session_state.agente
    
    c_izq, _, c_der = st.columns([2, 0.1, 1])
    
    with c_izq:
        st.markdown(f"<h1 class='titulo-ficha'>{f['t']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='precio-ficha'>{f['p']}</p>", unsafe_allow_html=True)
        
        if f['imgs']:
            st.image(f['imgs'][0], use_container_width=True) # Foto Principal
            if len(f['imgs']) > 1:
                cols = st.columns(3) # Grilla de fotos restantes
                for i, img_url in enumerate(f['imgs'][1:10]):
                    cols[i % 3].image(img_url, use_container_width=True)
        
        st.markdown("### Descripción")
        st.write(f['desc'])

    with c_der:
        st.markdown(f"""
            <div style='background:#161d2f; padding:25px; border-radius:15px; border:1px solid #2d3748;'>
                <h2 style='color:white; margin-top:0;'>{a['n']}</h2>
                <p style='color:#94a3b8;'>Martínez Propiedades</p>
                <hr style='border:0; border-top:1px solid #2d3748;'>
                <div class='grid-datos'>
                    <div class='caja-dato'><span class='dato-label'>m2</span><br><span class='dato-valor'>{f['m2']}</span></div>
                    <div class='caja-dato'><span class='dato-label'>Amb.</span><br><span class='dato-valor'>{f['amb']}</span></div>
                    <div class='caja-dato'><span class='dato-label'>Dorm.</span><br><span class='dato-valor'>{f['dor']}</span></div>
                </div>
                <a href="https://wa.me/{a['w']}?text=Consulta%20por%20{f['t']}" class="btn-whatsapp">WHATSAPP</a>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Volver al Panel"):
            del st.session_state["ficha"]
            st.rerun()

else:
    # PANEL DE CONTROL
    st.title("🥷 Martínez Prop - Panel")
    nombre = st.text_input("Tu Nombre", "Virginia Lincuiz")
    whatsapp = st.text_input("WhatsApp", "5492213184015")
    
    st.divider()
    
    url = st.text_input("Pegá el link de Argenprop:")
    if st.button("🚀 GENERAR FICHA"):
        with st.spinner("Buscando propiedad..."):
            datos = extraer_datos(url)
            if datos:
                st.session_state.ficha = datos
                st.session_state.agente = {"n": nombre, "w": whatsapp}
                st.rerun()
            else:
                st.error("Argenprop nos bloqueó. Los servidores de Streamlit están marcados.")
