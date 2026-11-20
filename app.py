import streamlit as st
import pandas as pd

st.set_page_config(page_title="Delicia Reposteria Rosmery", page_icon="🧁", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #ffe6f0; background-image: radial-gradient(#ffffff 4px, transparent 4px); background-size: 28px 28px; }
h1, h2, h3 { color: #e91e63 !important; font-family: 'Comic Sans MS', cursive !important; }
.header { background: #ff9ec5; border: 4px solid #5c1a2e; border-radius: 22px; padding: 18px 25px; text-align: center; }
.card { background: white; border: 3px solid #5c1a2e; border-radius: 20px; padding: 18px; text-align: center; }
.num { font-size: 55px; font-weight: bold; color: #e91e63; line-height: 1; }
.banner { background: #ff1a75; color: white; border: 3px dashed white; border-radius: 20px; padding: 14px; text-align: center; font-size: 24px; font-weight: bold; outline: 4px solid #5c1a2e; }
div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] div { background: white !important; border-radius: 12px !important; }
.stButton > button { background: #ff1a75 !important; color: white !important; border: 3px solid #5c1a2e !important; border-radius: 15px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1 style="margin:0; font-size:42px;">🧁 Delicia Reposteria Rosmery ✨</h1></div>', unsafe_allow_html=True)
st.write("")

def poner_estado(stock):
    if stock == 0:
        return "Agotado"
    elif stock < 15:
        return "Bajo"
    else:
        return "En Stock"

if "inventario_v5" not in st.session_state:
    st.session_state.inventario_v5 = pd.DataFrame({
        "Producto": ["Croissant", "Donut Rosa", "Cupcake Vainilla"],
        "Precio": [4500, 3800, 5000],
        "Stock": [24, 12, 30],
    })

df_base = st.session_state.inventario_v5.copy()
df_base["Stock"] = pd.to_numeric(df_base["Stock"], errors="coerce").fillna(0).astype(int)
df_base["Precio"] = pd.to_numeric(df_base["Precio"], errors="coerce").fillna(0).astype(int)
df = df_base.copy()
df["Estado"] = df["Stock"].apply(poner_estado)

total_stock = int(df["Stock"].sum())
bajo = int((df["Estado"] == "Bajo").sum())

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="card">✨📦 Total en Stock<div class="num">{total_stock}</div><div>¡Vamos bien! ⭐</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="card">⚠️ Productos con Stock Bajo<div class="num">{bajo}</div><div>¡Reabastecer pronto! ♡</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="card">🧁 Total de Productos<div class="num">{len(df)}</div><div>Delicias rosadas</div></div>', unsafe_allow_html=True)

st.write("")
# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["➕ Agregar Nuevo", "✏️ Editar", "🗑️ Eliminar"])

# 1. AGREGAR NUEVO - SOLO PARA PRODUCTOS NUEVOS
with tab1:
    st.markdown("### ➕ Agregar Producto Nuevo 💖")
    st.caption("Aquí solo se agregan productos nuevos, no se editan los viejos.")
    with st.form("agregar", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1: nuevo_prod = st.text_input("Nombre del producto nuevo")
        with col2: nuevo_precio = st.number_input("Precio", min_value=0, step=100)
        with col3: nuevo_stock = st.number_input("Stock", min_value=0, step=1)
        if st.form_submit_button("💖 Agregar Producto Nuevo ✨", use_container_width=True):
            if nuevo_prod.strip() == "":
                st.warning("Escribe el nombre del producto")
            elif nuevo_prod in df["Producto"].tolist():
                st.warning("Ese producto ya existe, mejor edítalo en la pestaña Editar")
            else:
                nuevo = pd.DataFrame([{"Producto": nuevo_prod, "Precio": nuevo_precio, "Stock": nuevo_stock}])
                st.session_state.inventario_v5 = pd.concat([st.session_state.inventario_v5, nuevo], ignore_index=True)
                st.success(f"¡{nuevo_prod} agregado! Estado automático: {poner_estado(nuevo_stock)} 💖")
                st.rerun()

# 2. EDITAR
with tab2:
    st.markdown("### ✏️ Editar Producto")
    if len(df) > 0:
        prod_editar = st.selectbox("Elige producto para editar", df["Producto"].tolist(), key="sel_editar")
        fila = df[df["Producto"] == prod_editar].iloc[0]
        with st.form("editar"):
            edit_nombre = st.text_input("Nombre", value=str(fila["Producto"]))
            edit_precio = st.number_input("Precio", min_value=0, step=100, value=int(fila["Precio"]))
            edit_stock = st.number_input("Stock", min_value=0, step=1, value=int(fila["Stock"]))
            st.caption(f"Estado automático será: {poner_estado(edit_stock)}")
            if st.form_submit_button("💾 Guardar Cambios ✨", use_container_width=True):
                idx = df_base[df_base["Producto"] == prod_editar].index[0]
                st.session_state.inventario_v5.loc[idx, "Producto"] = edit_nombre
                st.session_state.inventario_v5.loc[idx, "Precio"] = edit_precio
                st.session_state.inventario_v5.loc[idx, "Stock"] = edit_stock
                st.success("¡Editado! El Estado se actualizó solo 💖")
                st.rerun()
    else:
        st.info("No hay productos todavía.")

# 3. ELIMINAR
with tab3:
    st.markdown("### 🗑️ Eliminar Producto")
    if len(df) > 0:
        prod_eliminar = st.selectbox("Elige producto para eliminar", df["Producto"].tolist(), key="sel_eliminar")
        st.write(f"Vas a eliminar: **{prod_eliminar}**")
        if st.button("🗑️ Eliminar Producto", use_container_width=True):
            st.session_state.inventario_v5 = st.session_state.inventario_v5[st.session_state.inventario_v5["Producto"] != prod_eliminar].reset_index(drop=True)
            st.success(f"¡{prod_eliminar} eliminado!")
            st.rerun()
    else:
        st.info("No hay productos para eliminar.")

st.write("")
st.markdown("### 🔍 Buscar y Filtrar 💖")
col_b, col_f = st.columns(2)
with col_b: buscar = st.text_input("Buscar producto por nombre", placeholder="Ej: Croissant...")
with col_f: filtro = st.selectbox("Filtrar por Estado", ["Todos", "En Stock", "Bajo", "Agotado"])

df_f = df.copy()
if buscar:
    df_f = df_f[df_f["Producto"].astype(str).str.contains(buscar, case=False, na=False)]
if filtro != "Todos":
    df_f = df_f[df_f["Estado"] == filtro]

st.markdown("### 📋 Tu Inventario Actual")
st.dataframe(df_f, use_container_width=True, hide_index=True)

st.write("")
st.markdown('<div class="banner">✨ ¡Todo listo para hornear hoy! ✨<br><span style="font-size:15px;">Prepara tu horno • Ventas activas • Nuevas recetas disponibles</span></div>', unsafe_allow_html=True)
