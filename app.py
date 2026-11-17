import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Delicia Reposteria", layout="wide")
st.title("Delicia Reposteria - Inventario")
st.markdown("Control de productos, stock y ventas de la reposteria")

# Funcion para calcular el estado automaticamente segun el stock
def calcular_estado(stock_producto):
    if stock_producto == 0:
        return "Agotado"
    elif stock_producto < 15:
        return "Bajo"
    else:
        return "En Stock"

# 1. session_state - se inicializa una sola vez
if "inventario" not in st.session_state:
    st.session_state.inventario = [
        {"Producto": "Croissant", "Precio": 4500, "Stock": 24, "Estado": calcular_estado(24)},
        {"Producto": "Donut Rosa", "Precio": 3800, "Stock": 12, "Estado": calcular_estado(12)},
        {"Producto": "Cupcake Vainilla", "Precio": 5000, "Stock": 30, "Estado": calcular_estado(30)},
    ]

# 2. Consumo de API - Extra / Bonus
st.subheader("Inspiracion de la API")
try:
    respuesta = requests.get("https://fakestoreapi.com/products?limit=3", timeout=5)
    if respuesta.status_code == 200:
        productos_api = respuesta.json()
        for producto_api in productos_api:
            st.write(f"- {producto_api['title']} - Precio referencia: ${producto_api['price']}")
    else:
        st.info("No se pudo cargar la API en este momento.")
except Exception:
    st.info("Sin conexion a la API en este momento. Se muestra el inventario local.")

# 3. Resumen superior
inventario_actual = st.session_state.inventario
total_stock = sum(item["Stock"] for item in inventario_actual)
productos_bajos = sum(1 for item in inventario_actual if item["Estado"] == "Bajo")

col1, col2, col3 = st.columns(3)
col1.metric("Total en Stock", total_stock)
col2.metric("Productos con Stock Bajo", productos_bajos)
col3.metric("Total de Productos", len(inventario_actual))

# 4. Buscador y Filtro
st.subheader("Buscar y Filtrar")
col_buscar, col_filtro = st.columns(2)
with col_buscar:
    texto_busqueda = st.text_input("Buscar producto por nombre", "")
with col_filtro:
    filtro_estado = st.selectbox("Filtrar por Estado", ["Todos", "En Stock", "Bajo", "Agotado"])

df_inventario = pd.DataFrame(inventario_actual)
if texto_busqueda:
    df_inventario = df_inventario[df_inventario["Producto"].str.contains(texto_busqueda, case=False, na=False)]
if filtro_estado != "Todos":
    df_inventario = df_inventario[df_inventario["Estado"] == filtro_estado]

# 5. LEER - Mostrar inventario
st.subheader("Tu Inventario Actual")
st.dataframe(df_inventario, use_container_width=True)

if not df_inventario.empty:
    st.bar_chart(df_inventario.set_index("Producto")["Stock"])

for item in inventario_actual:
    if item["Estado"] == "Bajo":
        st.warning(f"Alerta: {item['Producto']} tiene stock bajo ({item['Stock']} unidades).")
    if item["Estado"] == "Agotado":
        st.error(f"Alerta: {item['Producto']} esta agotado.")

# 6. CREAR - Agregar producto con validaciones
st.subheader("Agregar Nuevo Producto")
with st.form("formulario_crear"):
    nombre_producto = st.text_input("Nombre del producto")
    precio_producto = st.number_input("Precio", min_value=0, step=100)
    stock_producto = st.number_input("Stock / Cantidad", min_value=0, step=1)
    boton_guardar = st.form_submit_button("Guardar Producto")

    if boton_guardar:
        nombres_existentes = [item["Producto"].lower() for item in inventario_actual]
        if nombre_producto.strip() == "":
            st.error("Error: El nombre del producto no puede estar vacio.")
        elif precio_producto <= 0:
            st.error("Error: El precio debe ser mayor a 0.")
        elif stock_producto < 0:
            st.error("Error: El stock no puede ser negativo.")
        elif nombre_producto.strip().lower() in nombres_existentes:
            st.error("Error: Ese producto ya existe en el inventario.")
        else:
            estado_automatico = calcular_estado(stock_producto)
            nuevo_producto = {
                "Producto": nombre_producto.strip(),
                "Precio": precio_producto,
                "Stock": stock_producto,
                "Estado": estado_automatico
            }
            st.session_state.inventario.append(nuevo_producto)
            st.success(f"Producto {nombre_producto} agregado con estado: {estado_automatico}")
            st.rerun()

# 7. ACTUALIZAR - Editar producto
st.subheader("Editar Producto")
if inventario_actual:
    lista_nombres = [item["Producto"] for item in inventario_actual]
    producto_seleccionado = st.selectbox("Elige el producto a editar", lista_nombres)
    producto_encontrado = next(item for item in inventario_actual if item["Producto"] == producto_seleccionado)

    with st.form("formulario_editar"):
        nuevo_precio = st.number_input("Nuevo precio", min_value=0, value=int(producto_encontrado["Precio"]), step=100)
        nuevo_stock = st.number_input("Nuevo stock", min_value=0, value=int(producto_encontrado["Stock"]), step=1)
        boton_actualizar = st.form_submit_button("Actualizar Producto")

        if boton_actualizar:
            if nuevo_precio <= 0:
                st.error("Error: El precio debe ser mayor a 0.")
            else:
                producto_encontrado["Precio"] = nuevo_precio
                producto_encontrado["Stock"] = nuevo_stock
                producto_encontrado["Estado"] = calcular_estado(nuevo_stock)
                st.success(f"Producto {producto_seleccionado} actualizado. Nuevo estado: {producto_encontrado['Estado']}")
                st.rerun()

# 8. ELIMINAR - Boton especifico
st.subheader("Eliminar Producto")
if inventario_actual:
    producto_a_eliminar = st.selectbox("Elige el producto a eliminar", lista_nombres, key="eliminar")
    boton_eliminar = st.button("Eliminar Producto Seleccionado")
    if boton_eliminar:
        st.session_state.inventario = [item for item in inventario_actual if item["Producto"] != producto_a_eliminar]
        st.success(f"Producto {producto_a_eliminar} eliminado correctamente.")
        st.rerun()
