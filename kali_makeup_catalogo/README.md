# Kali Makeup & Beauty — Catálogo en Python + Streamlit

Catálogo web de estilo lila/morado con buscador, filtros, carrito, envío del pedido por WhatsApp y panel privado para administrar productos.

## Incluye

- Inicio con productos destacados.
- Catálogo con búsqueda por nombre/marca y filtros por marca/categoría.
- Carrito con cantidades y total estimado.
- Botón para enviar el pedido preparado a WhatsApp.
- Página “Cómo comprar”.
- Panel de administración protegido por contraseña para agregar y editar productos.
- CSV de ejemplo para empezar rápidamente.

## 1. Requisitos

- Python 3.10 o posterior.
- Una cuenta de Streamlit Community Cloud para publicar gratis.
- Un repositorio de GitHub para desplegar desde Streamlit Community Cloud.

## 2. Ejecutar en tu computadora

Abre una terminal dentro de esta carpeta y ejecuta:

```bash
python -m venv .venv
```

Activa el entorno:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

Crea el archivo `.streamlit/secrets.toml` copiando `secrets.toml.example` y cambia los valores por los tuyos. No compartas ni subas ese archivo a GitHub.

Ejecuta:

```bash
streamlit run app.py
```

La aplicación se abrirá en el navegador. Si no configuras `admin_password`, el panel de administración no permitirá entrar.

## 3. Configurar WhatsApp

En `.streamlit/secrets.toml`, pon el número de WhatsApp de la tienda en formato internacional, solo dígitos, sin `+`, espacios ni guiones. Verifica el formato con tu propia línea antes de publicar.

Ejemplo de estructura (no uses este número ficticio):
```toml
whatsapp_number = "521XXXXXXXXXX"
```

El carrito arma un mensaje con productos, cantidades y total estimado. La clienta revisa y envía el mensaje desde WhatsApp; no se envía automáticamente sin su acción.

## 4. Publicar gratis y obtener un enlace

1. Crea una cuenta en GitHub y un repositorio nuevo, por ejemplo `kali-makeup-catalogo`.
2. Sube `app.py`, `products.csv`, `requirements.txt` y `.gitignore`. Puedes incluir este README.
3. **No subas** `.streamlit/secrets.toml`; el `.gitignore` ya lo excluye.
4. Entra a Streamlit Community Cloud: https://share.streamlit.io/
5. Conecta GitHub y selecciona tu repositorio.
6. Indica `app.py` como archivo principal y despliega la aplicación.
7. Abre la configuración de la app en Streamlit Community Cloud y agrega en **Secrets** los valores de `secrets.toml.example`, sustituyendo la contraseña y el teléfono por los reales.
8. Reinicia/reinicia el despliegue si hace falta.
9. Copia la URL pública que Streamlit te asigna y pégala en la biografía de Instagram de Kali.

Los nombres exactos de los menús pueden cambiar. Consulta la documentación oficial si la interfaz es distinta:
- Despliegue: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
- Secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management

## 5. Administrar productos

Entra en **Administración** desde el menú lateral e inicia sesión con `admin_password`. Puedes agregar productos con nombre, marca, categoría, precio, existencias, descripción y URL pública de imagen; también puedes editar la tabla y descargar una copia CSV.

Los productos de `products.csv` son ejemplos, no afirmaciones de disponibilidad real. Antes de compartir el catálogo, reemplaza nombres, precios, marcas, existencias y descripciones por los productos que realmente tengas.

### Fotos

Puedes poner una URL pública directa de imagen en `image_url`. Usa fotos propias o imágenes que tengas permiso de usar y comprueba que la URL abra la imagen sin iniciar sesión. Para una primera versión, puedes dejar ese campo vacío; la app mostrará un icono de maquillaje.

## Importante sobre datos y alojamiento gratuito

Esta versión guarda productos en `products.csv`, dentro del proyecto. En un alojamiento gratuito como Streamlit Community Cloud, los cambios hechos en el archivo local desde el panel **no deben considerarse almacenamiento permanente**: podrían perderse al reiniciar o volver a desplegar. Descarga copias CSV y conserva una copia de seguridad. Para uso comercial continuo, el siguiente paso sería conectar una base de datos persistente.

El panel de administración usa una contraseña compartida configurada en Secrets; es una protección inicial, no un sistema completo de cuentas/roles. No guardes datos sensibles de clientas. El carrito es temporal por sesión y el pedido solo se confirma cuando tú respondes por WhatsApp.

## Antes de lanzar

- [ ] Cambiar contraseña de administración.
- [ ] Configurar el WhatsApp correcto.
- [ ] Reemplazar los productos de ejemplo por el inventario real.
- [ ] Verificar precios y existencias.
- [ ] Probar un pedido desde el celular.
- [ ] Probar el enlace público en modo incógnito.
- [ ] Poner el enlace en Instagram.
