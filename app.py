import streamlit as st
import pandas as pd
from pathlib import Path
from urllib.parse import quote
import os
import hmac

# ==========================================
# KALI MAKEUP & BEAUTY
# Catálogo web con carrito y WhatsApp
# ==========================================

st.set_page_config(
    page_title="Kali Makeup & Beauty",
    page_icon="💜",
    layout="wide"
)

# CONFIGURACIÓN
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "products.csv"

def secret(nombre, default=""):
    try:
        return str(st.secrets.get(nombre, default))
    except Exception:
        return os.getenv(nombre, default)

WHATSAPP = secret("whatsapp_number", "5538237880")
ADMIN_PASSWORD = secret("admin_password", "Karlita2116")
UBICACION = secret("store_location", "CDMX · Consulta zonas de entrega")

# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background: linear-gradient(180deg, #fcf9ff, #f0e5fa);
    color: #5B2126;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] * {
    color: #6B21A8 !important;
}

div.stMarkdown p, label, div[class*="st-write"] {
    color: #6B21A8 !important;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #7C3AED !important;
}

[data-testid="stSidebar"] {
    background: #eadcf7;
}

div.stButton > button,
div.stLinkButton > a {
    background: #65417d;
    color: white !important;
    border: none;
    border-radius: 30px;
    font-weight: 600;
}

div.stButton > button:hover,
div.stLinkButton > a:hover {
    background: #442653;
    color: white !important;
}

.kali-hero {
    background: linear-gradient(120deg, #e4d1f4, #faf5ff, #c8a9e5);
    padding: 35px;
    border-radius: 24px;
    border: 1px solid #dfcbea;
}

.kali-logo {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    letter-spacing: 9px;
    color: #35223f;
    text-align: center;
}

.kali-subtitle {
    letter-spacing: 5px;
    text-align: center;
    font-size: 12px;
    color: #65417d;
}

.price {
    font-size: 22px;
    font-weight: bold;
    color: #65417d;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.75);
    border-color: #e1d0ee;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# BASE DE DATOS CSV
# ==========================================

COLUMNAS = [
    "id", "name", "brand", "category", "price",
    "stock", "description", "image_url", "active"
]

EJEMPLOS = [
    {
        "id": 1,
        "name": "Gloss labial",
        "brand": "Pink Up",
        "category": "Labios",
        "price": 95,
        "stock": 5,
        "description": "Gloss para complementar tu maquillaje.",
        "image_url": "",
        "active": True
    },
    {
        "id": 2,
        "name": "Rubor en polvo",
        "brand": "L.A. Colors",
        "category": "Rostro",
        "price": 85,
        "stock": 4,
        "description": "Dale un toque de color a tu look.",
        "image_url": "",
        "active": True
    },
    {
        "id": 3,
        "name": "Máscara de pestañas",
        "brand": "e.l.f.",
        "category": "Ojos",
        "price": 120,
        "stock": 3,
        "description": "Un básico para tu rutina de maquillaje.",
        "image_url": "",
        "active": True
    },
    {
        "id": 4,
        "name": "Paleta de sombras",
        "brand": "Beauty Creations",
        "category": "Ojos",
        "price": 180,
        "stock": 2,
        "description": "Colores para crear distintos looks.",
        "image_url": "",
        "active": True
    },
    {
        "id": 5,
        "name": "Set de brochas",
        "brand": "Pink Up",
        "category": "Brochas",
        "price": 250,
        "stock": 2,
        "description": "Brochas para aplicar y difuminar.",
        "image_url": "",
        "active": True
    }
]

def cargar_productos():
    if not DATA_FILE.exists():
        df = pd.DataFrame(EJEMPLOS, columns=COLUMNAS)
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        return df

    try:
        df = pd.read_csv(DATA_FILE, keep_default_na=False)

        for col in COLUMNAS:
            if col not in df.columns:
                df[col] = ""

        df["price"] = pd.to_numeric(
            df["price"], errors="coerce"
        ).fillna(0)

        df["stock"] = pd.to_numeric(
            df["stock"], errors="coerce"
        ).fillna(0).astype(int)

        df["active"] = df["active"].astype(str).str.lower().isin(
            ["true", "1", "si", "sí", "yes"]
        )

        return df[COLUMNAS]

    except Exception:
        return pd.DataFrame(EJEMPLOS, columns=COLUMNAS)


def guardar_productos(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


if "productos" not in st.session_state:
    st.session_state.productos = cargar_productos()

if "carrito" not in st.session_state:
    st.session_state.carrito = {}

if "admin" not in st.session_state:
    st.session_state.admin = False


def dinero(cantidad):
    return f"${float(cantidad):,.2f} MXN"


def enlace_whatsapp(mensaje):
    telefono = "".join(c for c in WHATSAPP if c.isdigit())
    return f"https://wa.me/{telefono}?text={quote(mensaje)}"


def productos_disponibles():
    df = st.session_state.productos.copy()
    return df[(df["active"] == True) & (df["stock"] > 0)]


# ==========================================
# MENÚ LATERAL
# ==========================================

with st.sidebar:
    st.markdown(
        '<div class="kali-logo">KALI</div>'
        '<div class="kali-subtitle">MAKEUP & BEAUTY</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.caption("♡ Tu belleza, nuestra prioridad")

    pagina = st.radio(
        "MENÚ PRINCIPAL",
        [
            "Inicio",
            "Catálogo",
            "Mi carrito",
            "Cómo comprar",
            "Administración"
        ]
    )

    st.divider()
    st.write("💄 Maquillaje y belleza")
    st.write("💌 Pedidos por WhatsApp")
    st.write("📍 " + UBICACION)


# ==========================================
# INICIO
# ==========================================

if pagina == "Inicio":

    st.markdown("""
    <div class="kali-hero">
        <p style="letter-spacing:4px;color:#65417d">
            MAKEUP · BEAUTY · SELF LOVE
        </p>
        <h1 style="font-size:48px">
            Kali Makeup & Beauty ♡
        </h1>
        <p style="font-size:18px;color:#594564">
            Maquillaje y favoritos de belleza para
            resaltar tu esencia.
        </p>
        <p>Descubre tus productos favoritos en un solo lugar.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("## ✨ Favoritos de Kali")

    df = productos_disponibles().head(4)

    if df.empty:
        st.info("Próximamente tendremos productos disponibles.")
    else:
        columnas = st.columns(4)

        for i, (_, p) in enumerate(df.iterrows()):
            with columnas[i]:
                with st.container(border=True):

                    if p["image_url"]:
                        st.image(p["image_url"], use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='text-align:center;font-size:60px;"
                            "padding:20px;background:#eee3f8;border-radius:12px'>"
                            "💄</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown(f"**{p['name']}**")
                    st.caption(p["brand"])
                    st.markdown(
                        f"<div class='price'>{dinero(p['price'])}</div>",
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Agregar ♡",
                        key=f"inicio_{p['id']}",
                        use_container_width=True
                    ):
                        pid = str(p["id"])
                        actual = st.session_state.carrito.get(pid, 0)

                        if actual < int(p["stock"]):
                            st.session_state.carrito[pid] = actual + 1
                            st.rerun()
                        else:
                            st.warning("Ya agregaste todas las existencias.")

    st.write("")
    st.info(
        "♡ Venta presencial. Consulta disponibilidad y zonas de entrega."
    )


# ==========================================
# CATÁLOGO
# ==========================================

elif pagina == "Catálogo":

    st.title("Nuestro catálogo ♡")
    st.write("Encuentra tus nuevos favoritos de belleza.")

    df = productos_disponibles()

    if df.empty:
        st.info("No hay productos disponibles actualmente.")
    else:
        c1, c2, c3 = st.columns([2, 1, 1])

        busqueda = c1.text_input(
            "Buscar producto",
            placeholder="Nombre, marca..."
        )

        marcas = ["Todas"] + sorted(df["brand"].unique().tolist())
        categorias = ["Todas"] + sorted(df["category"].unique().tolist())

        marca = c2.selectbox("Marca", marcas)
        categoria = c3.selectbox("Categoría", categorias)

        if busqueda:
            mascara = (
                df["name"].str.contains(busqueda, case=False, na=False)
                | df["brand"].str.contains(busqueda, case=False, na=False)
                | df["description"].str.contains(busqueda, case=False, na=False)
            )
            df = df[mascara]

        if marca != "Todas":
            df = df[df["brand"] == marca]

        if categoria != "Todas":
            df = df[df["category"] == categoria]

        if df.empty:
            st.warning("No encontramos productos con esos filtros.")
        else:
            columnas = st.columns(3)

            for i, (_, p) in enumerate(df.iterrows()):
                with columnas[i % 3]:
                    with st.container(border=True):

                        if p["image_url"]:
                            st.image(p["image_url"], use_container_width=True)
                        else:
                            st.markdown(
                                "<div style='text-align:center;font-size:65px;"
                                "padding:25px;background:#eee3f8;border-radius:12px'>"
                                "💜</div>",
                                unsafe_allow_html=True
                            )

                        st.subheader(p["name"])
                        st.caption(f"{p['brand']} · {p['category']}")

                        st.markdown(
                            f"<div class='price'>{dinero(p['price'])}</div>",
                            unsafe_allow_html=True
                        )

                        st.write(p["description"])
                        st.caption(f"Disponibles: {int(p['stock'])}")

                        cantidad = st.number_input(
                            "Cantidad",
                            min_value=1,
                            max_value=int(p["stock"]),
                            value=1,
                            key=f"cantidad_{p['id']}"
                        )

                        if st.button(
                            "Agregar al carrito ♡",
                            key=f"catalogo_{p['id']}",
                            use_container_width=True
                        ):
                            pid = str(p["id"])
                            actual = st.session_state.carrito.get(pid, 0)
                            nuevo = min(
                                actual + int(cantidad),
                                int(p["stock"])
                            )
                            st.session_state.carrito[pid] = nuevo
                            st.success("Producto agregado.")
                            st.rerun()


# ==========================================
# CARRITO Y PEDIDO POR WHATSAPP
# ==========================================

elif pagina == "Mi carrito":

    st.title("Mi carrito ♡")

    carrito = st.session_state.carrito
    productos = st.session_state.productos

    if not carrito:
        st.info("Tu carrito está vacío. ¡Explora el catálogo! 💜")

    else:
        total = 0
        mensaje_productos = []

        for pid in list(carrito.keys()):

            coincidencia = productos[
                productos["id"].astype(str) == str(pid)
            ]

            if coincidencia.empty:
                st.session_state.carrito.pop(pid, None)
                continue

            p = coincidencia.iloc[0]
            cantidad_actual = int(carrito[pid])

            cantidad = st.number_input(
                p["name"],
                min_value=0,
                max_value=max(0, int(p["stock"])),
                value=min(cantidad_actual, int(p["stock"])),
                key=f"carrito_{pid}"
            )

            if cantidad == 0:
                st.session_state.carrito.pop(pid, None)
                st.rerun()

            st.caption(
                f"{dinero(p['price'])} por unidad · "
                f"Subtotal: {dinero(float(p['price']) * cantidad)}"
            )

            total += float(p["price"]) * cantidad

            mensaje_productos.append(
                f"• {p['name']} ({p['brand']}) x{cantidad} "
                f"= {dinero(float(p['price']) * cantidad)}"
            )

            st.session_state.carrito[pid] = int(cantidad)

        st.divider()
        st.subheader(f"Total estimado: {dinero(total)}")
        st.caption("El costo de entrega, si aplica, se confirma por WhatsApp.")

        nombre = st.text_input("Tu nombre (opcional)")
        notas = st.text_area("Notas de tu pedido (opcional)")

        if not WHATSAPP:
            st.warning(
                "La tienda aún no tiene configurado su WhatsApp."
            )
        else:
            mensaje = (
                "Hola, Kali Makeup & Beauty 💜\n"
                "Quiero consultar este pedido:\n\n"
                + "\n".join(mensaje_productos)
                + f"\n\nTotal estimado: {dinero(total)}"
            )

            if nombre.strip():
                mensaje += f"\nNombre: {nombre.strip()}"

            if notas.strip():
                mensaje += f"\nNotas: {notas.strip()}"

            mensaje += (
                "\n\n¿Me confirmas la disponibilidad y cómo coordinamos "
                "la entrega?"
            )

            st.link_button(
                "Enviar pedido por WhatsApp 💌",
                enlace_whatsapp(mensaje),
                use_container_width=True
            )

        if st.button("Vaciar carrito"):
            st.session_state.carrito = {}
            st.rerun()


# ==========================================
# CÓMO COMPRAR
# ==========================================

elif pagina == "Cómo comprar":

    st.title("¿Cómo comprar? ♡")

    pasos = [
        ("01 · Elige tus favoritos",
         "Explora el catálogo y agrega productos a tu carrito."),
        ("02 · Envía tu pedido",
         "Abre WhatsApp desde el botón de tu carrito."),
        ("03 · Confirma tu compra",
         "Te confirmaremos disponibilidad, total y forma de pago."),
        ("04 · Coordina la entrega",
         "Consulta las zonas y horarios para entrega presencial.")
    ]

    for titulo, descripcion in pasos:
        with st.container(border=True):
            st.subheader(titulo)
            st.write(descripcion)

    st.info(
        "Tu pedido queda confirmado cuando Kali te responda por WhatsApp."
    )

    if WHATSAPP:
        st.link_button(
            "Preguntar por WhatsApp",
            enlace_whatsapp(
                "Hola, Kali Makeup & Beauty 💜 Tengo una duda."
            )
        )


# ==========================================
# PANEL DE ADMINISTRACIÓN
# ==========================================

elif pagina == "Administración":

    st.title("Administración ♡")
    st.write("Agrega productos, actualiza precios y controla existencias.")

    if not ADMIN_PASSWORD:
        st.error(
            "Configura admin_password en los Secrets de Streamlit "
            "para habilitar el acceso."
        )

        st.code(
            'admin_password = "tu-clave-segura"\n'
            'whatsapp_number = "521XXXXXXXXXX"\n'
            'store_location = "CDMX · Consulta zonas de entrega"',
            language="toml"
        )

    else:
        if not st.session_state.admin:

            with st.form("login"):
                password = st.text_input(
                    "Contraseña de administración",
                    type="password"
                )
                entrar = st.form_submit_button("Entrar")

            if entrar:
                if hmac.compare_digest(password, ADMIN_PASSWORD):
                    st.session_state.admin = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")

        else:
            if st.button("Cerrar sesión"):
                st.session_state.admin = False
                st.rerun()

            st.subheader("Agregar nuevo producto")

            with st.form("nuevo_producto", clear_on_submit=True):

                c1, c2 = st.columns(2)
                nombre = c1.text_input("Nombre del producto")
                marca = c2.text_input("Marca")

                c3, c4, c5 = st.columns(3)

                categoria = c3.selectbox(
                    "Categoría",
                    [
                        "Labios", "Ojos", "Rostro", "Brochas",
                        "Skincare", "Sets / Kits", "Accesorios", "Otro"
                    ]
                )

                precio = c4.number_input(
                    "Precio en MXN",
                    min_value=0.0,
                    value=99.0,
                    step=1.0
                )

                stock = c5.number_input(
                    "Existencias",
                    min_value=0,
                    value=1,
                    step=1
                )

                descripcion = st.text_area("Descripción")
                imagen = st.text_input("URL pública de imagen")
                activo = st.checkbox(
                    "Mostrar en catálogo",
                    value=True
                )

                guardar = st.form_submit_button("Guardar producto")

            if guardar:
                if not nombre.strip() or not marca.strip():
                    st.error("Escribe el nombre y la marca.")
                else:
                    df = st.session_state.productos.copy()

                    ids = pd.to_numeric(df["id"], errors="coerce").dropna()
                    nuevo_id = int(ids.max()) + 1 if not ids.empty else 1

                    nuevo = pd.DataFrame([{
                        "id": nuevo_id,
                        "name": nombre.strip(),
                        "brand": marca.strip(),
                        "category": categoria,
                        "price": precio,
                        "stock": stock,
                        "description": descripcion.strip(),
                        "image_url": imagen.strip(),
                        "active": activo
                    }])

                    df = pd.concat([df, nuevo], ignore_index=True)
                    guardar_productos(df)

                    st.session_state.productos = cargar_productos()
                    st.success("Producto guardado.")
                    st.rerun()

            st.subheader("Editar productos existentes")

            df_editado = st.data_editor(
                st.session_state.productos,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "id": st.column_config.NumberColumn(
                        "ID", disabled=True
                    ),
                    "name": st.column_config.TextColumn("Producto"),
                    "brand": st.column_config.TextColumn("Marca"),
                    "category": st.column_config.TextColumn("Categoría"),
                    "price": st.column_config.NumberColumn(
                        "Precio MXN", min_value=0
                    ),
                    "stock": st.column_config.NumberColumn(
                        "Existencias", min_value=0, step=1
                    ),
                    "description": st.column_config.TextColumn("Descripción"),
                    "image_url": st.column_config.TextColumn("URL de imagen"),
                    "active": st.column_config.CheckboxColumn("Visible")
                }
            )

            if st.button("Guardar cambios"):
                df_editado["price"] = pd.to_numeric(
                    df_editado["price"], errors="coerce"
                ).fillna(0)

                df_editado["stock"] = pd.to_numeric(
                    df_editado["stock"], errors="coerce"
                ).fillna(0).astype(int)

                df_editado["active"] = df_editado["active"].astype(bool)

                guardar_productos(df_editado)
                st.session_state.productos = cargar_productos()

                st.success("Cambios guardados.")
                st.rerun()

            st.download_button(
                "Descargar respaldo de productos",
                data=st.session_state.productos.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="kali_products_backup.csv",
                mime="text/csv"
            )

            st.warning(
                "Haz respaldos frecuentes. En alojamiento gratuito, "
                "los cambios guardados en archivos locales pueden perderse "
                "al reiniciar o volver a publicar la aplicación."
            )

# ==========================================
# PIE DE PÁGINA
# ==========================================

st.divider()

st.markdown(
    "<div style='text-align:center;color:#65417d'>"
    "♡ KALI MAKEUP & BEAUTY ♡<br>"
    "<small>Maquillaje que resalta lo mejor de ti.</small>"
    "</div>",
    unsafe_allow_html=True
)