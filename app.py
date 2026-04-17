import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Ficha Inmobiliaria | Martínez Prop", layout="wide", initial_sidebar_state="collapsed")

# 2. DISEÑO DARK MODE (Ojos descansados)
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    .titulo-prop { font-size: 36px; font-weight: 800; color: #ffffff; margin-bottom: 10px; }
    .precio-prop { font-size: 32px; color: #38bdf8; font-weight: 700; }
    .data-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; margin: 25px 0; }
    .data-card { background: #1e293b; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #334155; }
    .data-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 700; }
    .data-value { font-size: 18px; font-weight: 600; color: #f1f5f9; }
    .description-text { font-size: 17px; line-height: 1.8; color: #cbd5e1; white-space: pre-wrap; }
    .contact-sidebar { background: #1e293b; border: 1px solid #334155; padding: 25px; border-radius: 16px; position: sticky; top: 20px; }
    .wa-button { background-color: #22c55e; color: white !important; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: 700; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if "view" in st.query_params:
    d = st.session_state.get('p_data')
    a = st.session_state.get('a_data')
    
    col_content, _, col_sidebar = st.columns([2.3, 0.1, 1])
    with col_content:
        st.markdown(f"<h1 class='titulo-prop'>{d['titulo']}</h1><p class='precio-prop'>{d['precio']}</p>", unsafe_allow_html=True)
        if d['foto']:
            st.image(d['foto'], use_container_width=True)
        
        st.markdown(f"""
            <div class='data-grid'>
                <div class='data-card'><span class='data-label'>Sup. Total</span><br><span class='data-value'>{d['m2']}</span></div>
                <div class='data-card'><span class='data-label'>Ambientes</span><br><span class='data-value'>{d['amb']}</span></div>
                <div class='data-card'><span class='data-label'>Dormitorios</span><br><span class='data-value'>{d['dor']}</span></div>
                <div class='data-card'><span class='data-label'>Baños</span><br><span class='data-value'>{d['ban']}</span></div>
                <div class='data-card'><span class='data-label'>Cochera</span><br><span class='data-value'>{d['coch']}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color:white;'>Descripción</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='description-text'>{d['desc']}</div>", unsafe_allow_html=True)
    
    with col_sidebar:
        st.markdown(f"""
            <div class='contact-sidebar'>
                <p style='color:#38bdf8; font-weight:800; font-size:12px;'>AGENTE</p>
                <h3 style='color:white; margin:0;'>{a['nombre']}</h3>
                <p style='color:#94a3b8;'>Martínez Propiedades</p>
                <hr style='border-top: 1px solid #334155;'>
                <a href='https://wa.me/{a['wa']}?text=Consulta%20por%20{d['titulo']}' class='wa-button'>ENVIAR WHATSAPP</a>
            </div>
        """, unsafe_allow_html=True)
        if st.button("⬅️ Crear Otra"):
            st.query_params.clear()
            st.rerun()

else:
    st.title("🏠 Martínez Prop | Crear Ficha")
    st.info("Copiá los datos del portal (Zonaprop/Argenprop) y pegalos aquí.")
    
    nom = st.text_input("Tu Nombre", "Virginia Lincuiz")
    cel = st.text_input("Tu WhatsApp", "5492213184015")
    
    with st.container():
        t = st.text_input("Título del aviso")
        p = st.text_input("Precio (ej: USD 150.000)")
        img = st.text_input("Link de la Foto (Clic derecho en foto > Copiar dirección de imagen)")
        des = st.text_area("Descripción de la propiedad", height=150)
        
        c1, c2, c3, c4, c5 = st.columns(5)
        m2 = c1.text_input("m2")
        amb = c2.text_input("Amb.")
        dor = c3.text_input("Dorm.")
        ban = c4.text_input("Baños")
        coch = c5.text_input("Cochera")
        
        if st.button("✨ GENERAR FICHA PROFESIONAL"):
            st.session_state.p_data = {"titulo": t, "precio": p, "desc": des, "foto": img, "m2": m2, "amb": amb, "dor": dor, "ban": ban, "coch": coch}
            st.session_state.a_data = {"nombre": nom, "wa": cel}
            st.query_params["view"] = "ficha"
            st.rerun()
