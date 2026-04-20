import os
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise Exception("Falta TELEGRAM_TOKEN en Railway")

bot = telebot.TeleBot(TOKEN)

usuarios = {}

def asegurar_usuario(user_id):
    if user_id not in usuarios:
        usuarios[user_id] = {
            "saldo": 0,
            "etapa": "inicio"
        }

def archivo_existe(ruta):
    return os.path.exists(ruta)

# ── MENSAJES EDITABLES ─────────────────────────────────────────────

MENSAJE_BIENVENIDA = (
    "👋 Bienvenido\n\n"
    "Este es un sistema de información con contenido multimedia.\n"
    "Escriba 'hola' para comenzar."
)

MENSAJE_SALUDO = (
    "Hola.\n\n"
    "Aquí puede colocar su conversación inicial.\n"
    "Después, si desea continuar, escriba: si quiero"
)

MENSAJE_CONTINUAR = (
    "Perfecto.\n\n"
    "Ahora escriba /vip para ver los niveles disponibles."
)

MENSAJE_VIP = (
    "💎 NIVELES VIP:\n\n"
    "VIP 1 → 200 Bs\n"
    "VIP 2 → 500 Bs\n"
    "VIP 3 → 800 Bs\n\n"
    "Si desea, también puede escribir: tarea"
)

MENSAJE_TAREA = (
    "📌 TAREA DE EJEMPLO\n\n"
    "Aquí puede escribir la explicación de la tarea.\n"
    "Cuando termine, escriba: listo"
)

MENSAJE_COMPRA = (
    "Aquí puede colocar el mensaje para compra o contacto."
)

MENSAJE_DEFAULT = (
    "No entendí su mensaje.\n\n"
    "Escriba:\n"
    "- hola\n"
    "- si quiero\n"
    "- /vip\n"
    "- tarea\n"
    "- /saldo"
)

MENSAJE_IMAGEN_RECIBIDA = (
    "Recibí su imagen correctamente."
)

MENSAJE_VIDEO_RECIBIDO = (
    "Recibí su video correctamente."
)

MENSAJE_AUDIO_RECIBIDO = (
    "Recibí su audio correctamente."
)

MENSAJE_DOCUMENTO_RECIBIDO = (
    "Recibí su documento correctamente."
)

MENSAJE_STICKER_RECIBIDO = (
    "Recibí su sticker correctamente."
)

# ── RUTAS DE ARCHIVOS ──────────────────────────────────────────────

RUTA_IMAGEN_SALUDO = "imagenes/saludo.jpg"
RUTA_IMAGEN_VIP = "imagenes/vip.jpg"
RUTA_VIDEO_PRESENTACION = "videos/presentacion.mp4"
RUTA_AUDIO_BIENVENIDA = "audios/bienvenida.mp3"
RUTA_DOCUMENTO_INFO = "documentos/info.pdf"

# ── FUNCIONES DE ENVÍO ─────────────────────────────────────────────

def enviar_imagen(chat_id, ruta, caption=None):
    if archivo_existe(ruta):
        with open(ruta, "rb") as foto:
            bot.send_photo(chat_id, foto, caption=caption)
    else:
        bot.send_message(chat_id, f"⚠️ No se encontró la imagen: {ruta}")

def enviar_video(chat_id, ruta, caption=None):
    if archivo_existe(ruta):
        with open(ruta, "rb") as video:
            bot.send_video(chat_id, video, caption=caption)
    else:
        bot.send_message(chat_id, f"⚠️ No se encontró el video: {ruta}")

def enviar_audio(chat_id, ruta, caption=None):
    if archivo_existe(ruta):
        with open(ruta, "rb") as audio:
            bot.send_audio(chat_id, audio, caption=caption)
    else:
        bot.send_message(chat_id, f"⚠️ No se encontró el audio: {ruta}")

def enviar_documento(chat_id, ruta, caption=None):
    if archivo_existe(ruta):
        with open(ruta, "rb") as doc:
            bot.send_document(chat_id, doc, caption=caption)
    else:
        bot.send_message(chat_id, f"⚠️ No se encontró el documento: {ruta}")

# ── START ──────────────────────────────────────────────────────────

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)

    usuarios[user_id]["etapa"] = "inicio"

    bot.send_message(user_id, MENSAJE_BIENVENIDA)

# ── SALDO ──────────────────────────────────────────────────────────

@bot.message_handler(commands=["saldo"])
def saldo(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)

    bot.send_message(user_id, f"💰 Saldo: {usuarios[user_id]['saldo']} Bs")

# ── VIP ────────────────────────────────────────────────────────────

@bot.message_handler(commands=["vip"])
def vip(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)

    if usuarios[user_id]["etapa"] == "vip":
        bot.send_message(user_id, MENSAJE_VIP)

        # Imagen VIP
        enviar_imagen(user_id, RUTA_IMAGEN_VIP, "Imagen informativa VIP")

        # Audio VIP o bienvenida
        enviar_audio(user_id, RUTA_AUDIO_BIENVENIDA, "Audio informativo")

        # Documento PDF
        enviar_documento(user_id, RUTA_DOCUMENTO_INFO, "Documento informativo")
    else:
        bot.send_message(
            user_id,
            "Primero escriba 'hola' y luego 'si quiero' para continuar."
        )

# ── TEXTO ──────────────────────────────────────────────────────────

@bot.message_handler(content_types=["text"])
def mensajes(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)

    texto = (message.text or "").lower().strip()

    if texto in ["hola", "buen dia", "buen día", "buenos dias", "buenos días", "buenas tardes", "buenas noches"]:
        usuarios[user_id]["etapa"] = "oferta"

        bot.send_message(user_id, MENSAJE_SALUDO)

        # Imagen de saludo
        enviar_imagen(user_id, RUTA_IMAGEN_SALUDO, "Imagen de saludo")

        # Video de presentación
        enviar_video(user_id, RUTA_VIDEO_PRESENTACION, "Video de presentación")

    elif texto in ["si", "si quiero", "ok", "dale"]:
        if usuarios[user_id]["etapa"] == "oferta":
            usuarios[user_id]["etapa"] = "vip"
            bot.send_message(user_id, MENSAJE_CONTINUAR)
        else:
            bot.send_message(user_id, "Primero escriba 'hola' para iniciar.")

    elif texto == "tarea":
        usuarios[user_id]["etapa"] = "tarea"
        bot.send_message(user_id, MENSAJE_TAREA)

    elif texto == "listo":
        usuarios[user_id]["saldo"] += 5
        bot.send_message(
            user_id,
            f"✅ Registro completado.\n💰 +5 Bs\nSaldo actual: {usuarios[user_id]['saldo']} Bs"
        )

    elif "comprar vip" in texto:
        bot.send_message(user_id, MENSAJE_COMPRA)

    else:
        bot.send_message(user_id, MENSAJE_DEFAULT)

# ── ARCHIVOS RECIBIDOS DEL USUARIO ─────────────────────────────────

@bot.message_handler(content_types=["photo"])
def recibir_imagen(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)
    bot.send_message(user_id, MENSAJE_IMAGEN_RECIBIDA)

@bot.message_handler(content_types=["video"])
def recibir_video(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)
    bot.send_message(user_id, MENSAJE_VIDEO_RECIBIDO)

@bot.message_handler(content_types=["audio", "voice"])
def recibir_audio(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)
    bot.send_message(user_id, MENSAJE_AUDIO_RECIBIDO)

@bot.message_handler(content_types=["document"])
def recibir_documento_usuario(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)
    bot.send_message(user_id, MENSAJE_DOCUMENTO_RECIBIDO)

@bot.message_handler(content_types=["sticker"])
def recibir_sticker(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)
    bot.send_message(user_id, MENSAJE_STICKER_RECIBIDO)

print("✅ Bot activo...")
bot.infinity_polling(timeout=30, long_polling_timeout=30)
