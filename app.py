import os
import csv
import hmac
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "products.csv"

st.set_page_config(
    page_title="Kali Makeup & Beauty",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Configuración y datos
# ----------------------------
def get_secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
        return str(value) if value is not None else default
    except Exception:
        return os.getenv(name, default)


def load_products() -> pd.DataFrame:
    columns = ["id", "name", "brand", "category", "price", "stock", "description", "image_url", "active"]
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=columns)
    try:
        df = pd.read_csv(DATA_FILE, keep_default_na=False)
    except Exception:
        return pd.DataFrame(columns=columns)
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)
    df["active"] = df["active"].astype(str).str.lower().isin(["true", "1", "sí", "si", "yes"])
    return df[columns]


def save_products(df: pd.DataFrame) -> None:
    df = df.copy()
    df["active"] = df["active"].astype(bool)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


if "products" not in st.session_state:
    st.session_state.products = load_products()
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

# ----------------------------
# Estilo visual
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root { --lilac: #eee5f8; --lavender: #c6a8e8; --purple: #65417d; --deep: #241a2d; --ink: #29212f; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(180deg, #faf7fd 0%, #f3ebfa 100%); color: var(--ink); }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: var(--deep); }
[data-testid="stSidebar"] { background: #eee5f8; border-right: 1px solid #ddcbea; }
div.stButton > button, div.stDownloadButton > button { background: #65417d; color: white; border: 0; border-radius: 999px; padding: .55rem 1rem; }
div.stButton > button:hover { background: #4f3264; color: white; border: 0; }
.kali-kicker { letter-spacing: .25em; text-transform: uppercase; font-size: .75rem; color: #76578d; font-weight: 700; }
.kali-hero { padding: 2rem 2.2rem; border-radius: 22px; background: linear-gradient(120deg, #e6d6f4, #f8f1fc 58%, #c9a8e4); border: 1px solid #dfcde9; }
.kali-hero h1 { font-size: clamp(2rem, 5vw, 3.4rem); margin: .2rem 0; }
.kali-muted { color: #695d70; }
.product-card { background: rgba(255,255,255,.82); border: 1px solid #e4d6ee; border-radius: 18px; padding: 12px; height: 100%; }
.price { font-size: 1.15rem; color: #56336c; font-weight: 700; }
.pill { display:inline-block; padding: 4px 10px; border-radius: 999px; background:#eee4f8; color:#65417d; font-size:.75rem; }
hr { border-color: #e4d6ee; }
</style>
""", unsafe_allow_html=True)

def money(value) -> str:
    return f"${float(value):,.2f} MXN"


def whatsapp_link(phone: str, message: str) -> str:
    phone = "".join(ch for ch in phone if ch.isdigit())
    return f"https://wa.me/{phone}?text={quote(message)}"


def cart_count() -> int:
    return sum(int(qty) for qty in st.session_state.cart.values())


def active_products() -> pd.DataFrame:
    df = st.session_state.products.copy()
    return df[(df["active"] == True) & (df["stock"] > 0)].copy()


# ----------------------------
# Navegación
# ----------------------------
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:.6rem 0 1rem'><div style='font-family:Playfair Display,serif;font-size:2.2rem;letter-spacing:.12em;color:#241a2d'>KALI</div><div style='font-size:.7rem;letter-spacing:.28em;color:#65417d'>MAKEUP & BEAUTY</div><div style='color:#76578d;margin-top:.5rem'>Tu belleza, nuestra prioridad ♡</div></div>", unsafe_allow_html=True)
    page = st.radio("MENÚ", ["Inicio", "Catálogo", f"Mi carrito ({cart_count()})", "Cómo comprar", "Administración"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("Maquillaje de tus marcas favoritas 💜")
    st.caption("Pedidos por WhatsApp · Entrega presencial")
    st.markdown("[Instagram](https://www.instagram.com/) · [WhatsApp](https://www.whatsapp.com/)")

phone = get_secret("whatsapp_number", "")
store_location = get_secret("store_location", "CDMX · Consulta zonas de entrega")
currency_note = "Precios en MXN. Disponibilidad sujeta a confirmación."

# ----------------------------
# Inicio
# ----------------------------
if page == "Inicio":
    st.markdown("""
    <div class="kali-hero">
      <div class="kali-kicker">Makeup · Beauty · Self-love</div>
      <h1>Kali Makeup & Beauty</h1>
      <p style="font-size:1.08rem;color:#4d3b58;max-width:650px">Maquillaje y favoritos de belleza para resaltar tu esencia. Encuentra tus productos, arma tu carrito y envíanos tu pedido por WhatsApp.</p>
      <span class="pill">♡ Tu belleza, a tu manera</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns(3)
    col1.metric("Marcas", "Multimarca", help="Vendemos productos de marcas existentes.")
    col2.metric("Pedidos", "Por WhatsApp")
    col3.metric("Entrega", "Presencial")
    st.markdown("## Favoritos de Kali")
    products = active_products().head(4)
    if products.empty:
        st.info("Todavía no hay productos activos. Entra a Administración para agregar los primeros productos.")
    else:
        cols = st.columns(4)
        for i, (_, p) in enumerate(products.iterrows()):
            with cols[i]:
                if p["image_url"]:
                    st.image(p["image_url"], use_container_width=True)
                else:
                    st.markdown("<div style='height:130px;display:flex;align-items:center;justify-content:center;background:#eee5f8;border-radius:14px;font-size:3rem'>💄</div>", unsafe_allow_html=True)
                st.markdown(f"**{p['name']}**")
                st.caption(f"{p['brand']} · {p['category']}")
                st.markdown(f"<div class='price'>{money(p['price'])}</div>", unsafe_allow_html=True)
                if st.button("Agregar al carrito", key=f"home_add_{p['id']}", use_container_width=True):
                    st.session_state.cart[str(p["id"])] = st.session_state.cart.get(str(p["id"]), 0) + 1
                    st.rerun()
    st.markdown("---")
    st.caption(f"{store_location} · {currency_note}")

# ----------------------------
# Catálogo
# ----------------------------
elif page == "Catálogo":
    st.title("Catálogo")
    st.write("Explora tus favoritos y agrega al carrito los productos que te interesen.")
    df = active_products()
    if df.empty:
        st.info("Pronto encontrarás productos aquí. Estamos preparando el catálogo.")
    else:
        f1, f2, f3 = st.columns([2, 1, 1])
        search = f1.text_input("Buscar", placeholder="Producto, marca o palabra clave…")
        brands = ["Todas"] + sorted([x for x in df["brand"].astype(str).unique() if x])
        categories = ["Todas"] + sorted([x for x in df["category"].astype(str).unique() if x])
        brand = f2.selectbox("Marca", brands)
        category = f3.selectbox("Categoría", categories)
        if search:
            mask = (
                df["name"].astype(str).str.contains(search, case=False, na=False)
                | df["brand"].astype(str).str.contains(search, case=False, na=False)
                | df["description"].astype(str).str.contains(search, case=False, na=False)
            )
            df = df[mask]
        if brand != "Todas":
            df = df[df["brand"] == brand]
        if category != "Todas":
            df = df[df["category"] == category]
        if df.empty:
            st.warning("No encontramos productos con esos filtros.")
        else:
            cols = st.columns(3)
            for i, (_, p) in enumerate(df.iterrows()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if p["image_url"]:
                            st.image(p["image_url"], use_container_width=True)
                        else:
                            st.markdown("<div style='height:170px;display:flex;align-items:center;justify-content:center;background:#eee5f8;border-radius:14px;font-size:3.2rem'>💜</div>", unsafe_allow_html=True)
                        st.markdown(f"### {p['name']}")
                        st.caption(f"{p['brand']} · {p['category']}")
                        st.markdown(f"<div class='price'>{money(p['price'])}</div>", unsafe_allow_html=True)
                        st.write(p["description"] or "Un favorito para tu rutina de belleza.")
                        st.caption(f"Disponibles: {int(p['stock'])}")
                        qty_key = f"qty_{p['id']}"
                        qty = st.number_input("Cantidad", min_value=1, max_value=max(1, int(p["stock"])), value=1, step=1, key=qty_key)
                        if st.button("Agregar al carrito ♡", key=f"add_{p['id']}", use_container_width=True):
                            pid = str(p["id"])
                            current = int(st.session_state.cart.get(pid, 0))
                            st.session_state.cart[pid] = min(current + int(qty), int(p["stock"]))
                            st.success("Agregado al carrito.")
                            st.rerun()
    st.caption(currency_note)

# ----------------------------
# Carrito y WhatsApp
# ----------------------------
elif page.startswith("Mi carrito"):
    st.title("Tu carrito ♡")
    products = st.session_state.products
    cart = st.session_state.cart
    if not cart:
        st.info("Tu carrito está vacío. Ve al Catálogo para elegir tus favoritos.")
    else:
        total = 0.0
        items_for_message = []
        for pid in list(cart.keys()):
            match = products[products["id"].astype(str) == str(pid)]
            if match.empty:
                del st.session_state.cart[pid]
                continue
            p = match.iloc[0]
            qty = int(cart[pid])
            subtotal = float(p["price"]) * qty
            total += subtotal
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            c1.write(f"**{p['name']}**")
            c1.caption(f"{p['brand']} · {money(p['price'])} c/u")
            new_qty = c2.number_input("Cant.", min_value=0, max_value=max(0, int(p["stock"])), value=min(qty, int(p["stock"])), step=1, key=f"cart_qty_{pid}")
            c3.write(f"**{money(subtotal)}**")
            if c4.button("Quitar", key=f"remove_{pid}"):
                st.session_state.cart.pop(pid, None)
                st.rerun()
            if new_qty == 0:
                st.session_state.cart.pop(pid, None)
            else:
                st.session_state.cart[pid] = int(new_qty)
            items_for_message.append(f"• {p['name']} ({p['brand']}) x{new_qty} — {money(float(p['price']) * new_qty)}")
        st.markdown("---")
        st.markdown(f"## Total estimado: {money(total)}")
        st.caption("El total no incluye posibles cargos de entrega. Confirma disponibilidad y total final por WhatsApp.")
        customer_name = st.text_input("Tu nombre (opcional)")
        notes = st.text_area("Notas para tu pedido (opcional)", placeholder="Por ejemplo: ¿Qué tonos hay disponibles?")
        if not phone:
            st.warning("Falta configurar el número de WhatsApp de Kali. Agrégalo en Secrets antes de publicar.")
        else:
            message = "Hola, Kali Makeup & Beauty 💜 Quiero consultar este pedido:\n\n" + "\n".join(items_for_message) + f"\n\nTotal estimado: {money(total)}"
            if customer_name.strip():
                message += f"\nNombre: {customer_name.strip()}"
            if notes.strip():
                message += f"\nNotas: {notes.strip()}"
            message += "\n\n¿Me confirmas disponibilidad y cómo coordinamos la entrega?"
            st.link_button("Enviar pedido por WhatsApp", whatsapp_link(phone, message), use_container_width=True)
        if st.button("Vaciar carrito"):
            st.session_state.cart = {}
            st.rerun()

# ----------------------------
# Cómo comprar
# ----------------------------
elif page == "Cómo comprar":
    st.title("¿Cómo comprar?")
    steps = [
        ("01 · Elige tus favoritos", "Explora el catálogo, revisa precios y agrega productos al carrito."),
        ("02 · Envía tu pedido", "Presiona el botón de WhatsApp para enviarnos tu lista."),
        ("03 · Confirma disponibilidad", "Te confirmaremos existencias, total final y opciones de pago."),
        ("04 · Coordina tu entrega", "La entrega es presencial; consulta por WhatsApp las zonas y horarios disponibles."),
    ]
    for heading, body in steps:
        with st.container(border=True):
            st.subheader(heading)
            st.write(body)
    st.info("Importante: el pedido no queda confirmado hasta que Kali te responda por WhatsApp.")
    if phone:
        st.link_button("Consultar por WhatsApp", whatsapp_link(phone, "Hola, Kali Makeup & Beauty 💜 Tengo una duda sobre cómo comprar."))

# ----------------------------
# Administración
# ----------------------------
elif page == "Administración":
    st.title("Panel de administración")
    st.write("Gestiona productos, precios, existencias y visibilidad del catálogo.")
    admin_password = get_secret("admin_password", "")
    if not admin_password:
        st.error("Por seguridad, configura `admin_password` en los Secrets de Streamlit antes de usar el panel.")
        st.code('admin_password = "pon-aqui-una-clave-larga-y-unica"\nwhatsapp_number = "521XXXXXXXXXX"\nstore_location = "CDMX · Consulta zonas de entrega"', language="toml")
    else:
        if not st.session_state.admin_ok:
            with st.form("admin_login"):
                password = st.text_input("Contraseña de administración", type="password")
                submitted = st.form_submit_button("Entrar")
            if submitted:
                if hmac.compare_digest(password, admin_password):
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")
        else:
            top1, top2 = st.columns([3, 1])
            top1.success("Sesión de administración activa en esta sesión.")
            if top2.button("Cerrar sesión"):
                st.session_state.admin_ok = False
                st.rerun()

            st.markdown("### Agregar producto")
            with st.form("new_product", clear_on_submit=True):
                a1, a2 = st.columns(2)
                name = a1.text_input("Nombre del producto *")
                brand = a2.text_input("Marca *")
                a3, a4, a5 = st.columns(3)
                category = a3.selectbox("Categoría", ["Labios", "Ojos", "Rostro", "Brochas", "Skincare", "Sets / Kits", "Accesorios", "Otro"])
                price = a4.number_input("Precio (MXN) *", min_value=0.0, value=99.0, step=1.0)
                stock = a5.number_input("Existencias *", min_value=0, value=1, step=1)
                description = st.text_area("Descripción")
                image_url = st.text_input("URL pública de imagen (opcional)")
                active = st.checkbox("Mostrar en el catálogo", value=True)
                add_submitted = st.form_submit_button("Guardar producto")
            if add_submitted:
                if not name.strip() or not brand.strip():
                    st.error("Completa el nombre y la marca.")
                else:
                    current = st.session_state.products.copy()
                    next_id = 1
                    if not current.empty:
                        numeric_ids = pd.to_numeric(current["id"], errors="coerce").dropna()
                        next_id = int(numeric_ids.max()) + 1 if not numeric_ids.empty else len(current) + 1
                    row = {
                        "id": str(next_id), "name": name.strip(), "brand": brand.strip(),
                        "category": category, "price": float(price), "stock": int(stock),
                        "description": description.strip(), "image_url": image_url.strip(), "active": bool(active)
                    }
                    current = pd.concat([current, pd.DataFrame([row])], ignore_index=True)
                    save_products(current)
                    st.session_state.products = load_products()
                    st.success("Producto guardado.")
                    st.rerun()

            st.markdown("### Editar productos existentes")
            current = st.session_state.products.copy()
            if current.empty:
                st.info("Aún no hay productos. Puedes agregar el primero arriba.")
            else:
                edited = st.data_editor(
                    current,
                    use_container_width=True,
                    num_rows="dynamic",
                    column_config={
                        "id": st.column_config.TextColumn("ID", disabled=True),
                        "name": st.column_config.TextColumn("Producto", required=True),
                        "brand": st.column_config.TextColumn("Marca", required=True),
                        "category": st.column_config.TextColumn("Categoría"),
                        "price": st.column_config.NumberColumn("Precio MXN", min_value=0, step=1, format="$%.2f"),
                        "stock": st.column_config.NumberColumn("Existencias", min_value=0, step=1),
                        "description": st.column_config.TextColumn("Descripción", width="large"),
                        "image_url": st.column_config.TextColumn("URL de imagen", width="large"),
                        "active": st.column_config.CheckboxColumn("Visible"),
                    },
                    key="products_editor",
                )
                csave, cdownload = st.columns(2)
                if csave.button("Guardar cambios", use_container_width=True):
                    edited = edited.copy()
                    edited["price"] = pd.to_numeric(edited["price"], errors="coerce").fillna(0.0)
                    edited["stock"] = pd.to_numeric(edited["stock"], errors="coerce").fillna(0).astype(int)
                    edited["active"] = edited["active"].astype(bool)
                    save_products(edited)
                    st.session_state.products = load_products()
                    st.success("Cambios guardados en el archivo de productos.")
                    st.rerun()
                cdownload.download_button(
                    "Descargar copia CSV",
                    data=edited.to_csv(index=False).encode("utf-8-sig"),
                    file_name="kali_products_backup.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            st.warning("Nota de alojamiento: en servicios gratuitos, los cambios guardados en archivos locales pueden perderse cuando la app se reinicia o se vuelve a desplegar. Descarga copias CSV y conserva el archivo products.csv actualizado en tu proyecto. Para una tienda con muchos productos, conviene migrar los datos a una base de datos.")
