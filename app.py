import streamlit as st
import pandas as pd

st.set_page_config(page_title="Delicia Reposteria Rosmery", page_icon="🧁", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #ffe6f0; background-image: radial-gradient(#ffffff 4px, transparent 4px); background-size: 28px 28px; }
h1, h2, h3 { color: #e91e63 !important; font-family: 'Comic Sans MS', cursive !important; }
.header {
    background: #ff9ec5; border: 4px solid #5c1a2e; border-radius: 22px;
    padding: 18px 25px; text-align: center;
}
.card {
    background: white; border: 3px solid #5c1a2e; border-radius: 20px;
    padding: 18px; text-align: center;
}
.num { font-size: 55px; font-weight: bold; color: #e91e63; line-height: 1; }
.banner {
    background: #ff1a75; color: white; border: 3px dashed white;
    border-radius: 20px; padding: 14px; text-align: center;
    font-size: 24px; font-weight: bold; outline: 4px solid #5c1a2e;
}
div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div { background: white !important; border-radius: 12px !important; }
.stButton > button { background: #ff1a75 !important; color: white !important; border: 3px solid #5c1a2e !important; border-radius: 15px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1 style="margin:0; font-size:42px;">🧁 Delicia Reposteria Rosmery ✨</h1></div>', unsafe_allow_html=True)
st.write("")

if "inventario_v2" not in st.session_state:
    st.session_state.inventario_v2 = pd.DataFrame({
        "Producto": ["Croissant", "Donut Rosa", "Cupcake Vainilla"],
        "Precio": [4500, 3800, 5000],
        "Stock": [24, 12, 30],
        "Estado": ["En Stock", "Bajo", "En Stock"]
    })

df = st.session_state.inventario_v2
df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce").fillna(0)
df["Precio"] = pd.to_numeric(df["Precio"], errors="coerce").fillna(0)
total_stock = int(df["Stock"].sum())
bajo = int((df["Estado"] == "Bajo").sum())

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="card">✨📦 Total en Stock<div class="num">{total_stock}</div><div>¡Vamos bien! ⭐</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="card">⚠️ Productos con Stock Bajo<div class="num">{bajo}</div><div>¡Reabastecer pronto! ♡</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="card">🧁 Total de Productos<div class="num">{len(df)}</div><div>Delicias rosadas</div></div>', unsafe_allow_html=True)

st.write("")
st.markdown("### 🔍 Buscar y Filtrar 💖")
col_b, col_f = st.columns(2)
with col_b: buscar = st.text_input("Buscar producto por nombre", placeholder="Ej: Croissant...")
with col_f: filtro = st.selectbox("Filtrar por Estado", ["Todos", "En Stock", "Bajo"])

df_f = df.copy()
if buscar:
    df_f = df_f[df_f["Producto"].astype(str).str.contains(buscar, case=False, na=False)]
if filtro != "Todos":
    df_f = df_f[df_f["Estado"] == filtro]

st.markdown("### 📋 Tu Inventario Actual")
editado = st.data_editor(df_f, use_container_width=True, hide_index=True, num_rows="dynamic", key="tabla")

if st.button("💾 Guardar Cambios ✨", use_container_width=True):
    st.session_state.inventario_v2 = editado
    st.balloons()
    st.success("¡Guardado Rosmery!")

st.write("")
st.markdown('<div class="banner">✨ ¡Todo listo para hornear hoy! ✨<br><span style="font-size:15px;">Prepara tu horno • Ventas activas • Nuevas recetas disponibles</span></div>', unsafe_allow_html=True)
