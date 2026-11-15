import streamlit as st
import pandas as pd

# CONFIGURACIÓN
st.set_page_config(
    page_title="Delicia Repostería Rosmery",
    page_icon="🧁",
    layout="wide"
)

# COLORES BONITOS ROSADOS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700&display=swap');

.stApp {
    background-color: #ffe6f0;
    background-image: radial-gradient(#ffffff 3px, transparent 3px);
    background-size: 25px 25px;
}
h1, h2, h3 { font-family: 'Fredoka One', cursive !important; color: #e91e63 !important; }

.header-rosado {
    background: #ff9ec5;
    border: 4px solid #5c1a2e;
    border-radius: 20px;
    padding: 15px 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.card-amarilla {
    background: #fff2a8;
    border: 3px solid #5c1a2e;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
}
.card-rosada {
    background: #ffccd9;
    border: 3px solid #5c1a2e;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
}
.numero-grande {
    font-family: 'Fredoka One';
    font-size: 70px;
    color: #e91e63;
    line-height: 1;
    margin: 0;
    -webkit-text-stroke: 2px white;
}
.banner-abajo {
    background: #ff1a75;
    color: white;
    border: 3px dashed white;
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    font-family: 'Fredoka One';
    font-size: 28px;
    outline: 4px solid #5c1a2e;
}
.muñeca-box {
    text-align: center;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header-rosado">
    <div style="display:flex; align-items:center; gap:15px;">
        <div style="background:#fff2a8; border-radius:50%; width:70px; height:70px; display:flex; align-items:center; justify-content:center; font-size:40px; border:3px solid #5c1a2e;">🧁</div>
        <div>
            <h1 style="margin:0; font-size:38px; line-height:1;">Delicia Repostería<br>Rosmery ✨</h1>
            <div style="background:#fff2a8; border-radius:10px; padding:2px 10px; font-weight:bold; display:inline-block; border:2px solid #5c1a2e; font-size:12px;">PANADERÍA KAWAI</div>
        </div>
    </div>
    <div style="display:flex; gap:10px;">
        <div style="background:#fff2a8; width:55px; height:55px; border-radius:15px; display:flex; align-items:center; justify-content:center; font-size:28px; border:3px solid #5c1a2e;">🏠</div>
        <div style="background:#ffccd9; width:55px; height:55px; border-radius:15px; display:flex; align-items:center; justify-content:center; font-size:28px; border:3px solid #5c1a2e;">🔔</div>
        <div style="background:#fff2a8; width:55px; height:55px; border-radius:15px; display:flex; align-items:center; justify-content:center; font-size:28px; border:3px solid #5c1a2e;">⚙️</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# COLUMNAS PRINCIPALES
col_izq, col_der = st.columns([2.2, 1])

with col_izq:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="card-amarilla">
            <div style="font-weight:bold; color:#c2185b;">✨📦 Total Items</div>
            <div class="numero-grande">104</div>
            <div style="color:#ad1457; font-weight:bold;">+12 esta semana ↗️ ⭐</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class="card-rosada" style="background:#ffc2d6; border-style: dotted;">
            <div style="font-weight:bold; color:#c2185b;">✨ Hoy Producido</div>
            <div class="numero-grande">50</div>
            <div style="color:#ad1457; font-weight:bold;">Croissants • Donuts • Cupcakes</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card-rosada">
            <div style="font-weight:bold; color:#c2185b;">⚠️ Bajo Stock</div>
            <div class="numero-grande">3</div>
            <div style="color:#ad1457; font-weight:bold;">¡Reabastecer pronto! ♡</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class="card-amarilla">
            <div style="font-weight:bold; color:#c2185b; font-size:22px;">Inventario Actual</div>
            <div style="text-align:left; background:#fff0f5; border-radius:12px; padding:10px; margin-top:10px; font-weight:bold; color:#5c1a2e;">
                • Croissant — 24 ✅<br>
                • Donut Rosa — 12 ⚠️ Bajo<br>
                • Cupcake — 30 ✅
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="banner-abajo">✨ ¡Todo listo para hornear hoy! ✨<br><span style="font-size:16px; font-family:Nunito;">Prepara tu horno • Ventas activas • Nuevas recetas disponibles</span></div>', unsafe_allow_html=True)

    st.write("")
    # TABLA EDITABLE REAL
    st.markdown("### 📋 Tu Inventario Mágico")
    
    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame({
            "Producto": ["Croissant", "Donut Rosa", "Cupcake Vainilla", "Pan de Bono"],
            "Stock": [24, 12, 30, 8],
            "Estado": ["✅ En Stock", "⚠️ Bajo", "✅ En Stock", "⚠️ Bajo"]
        })
    
    edited = st.data_editor(st.session_state.inventario, use_container_width=True, hide_index=True, num_rows="dynamic")
    
    if st.button("💾 Guardar Cambios ✨", use_container_width=True):
        st.session_state.inventario = edited
        st.balloons()
        st.success("¡Guardado Rosmery!")

with col_der:
    st.markdown("""
    <div class="muñeca-box">
        <div style="font-size:40px;">🎈🎈</div>
        <div style="font-size:130px; line-height:1;">👧🏻</div>
        <div style="background:white; border:3px solid #5c1a2e; border-radius:15px; padding:8px; display:inline-block; font-size:60px; margin-top:-30px;">🍩🍩<br><span style="font-size:14px; font-weight:bold;">Donas Rosadas</span></div>
        <div style="margin-top:10px; font-size:25px;">💖🧁⭐🍓🍪💫</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("✨ ¡Hornear Hoy! 🍩", use_container_width=True):
        st.balloons()
        st.success("¡Vamos a hornear Rosmery!")
    
    st.info("💡 Tip: ¡Edita tu tabla a la izquierda y dale a Guardar!")
