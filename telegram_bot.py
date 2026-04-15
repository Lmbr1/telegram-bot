import os
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TOKEN)

usuarios = {}

# ── START ──
@bot.message_handler(commands=["start"])
def start(message):
    usuarios[message.chat.id] = {"saldo": 0}

    bot.send_message(message.chat.id,
    "👋 Bienvenido al sistema de tareas\n\n"
    "💰 Gana dinero realizando tareas simples\n"
    "📊 Ganancias: 5 - 50 Bs por tarea\n\n"
    "📌 Comandos:\n"
    "/tarea - Ver tareas\n"
    "/vip - Ver niveles VIP\n"
    "/saldo - Ver saldo")

# ── TAREA ──
@bot.message_handler(commands=["tarea"])
def tarea(message):
    bot.send_message(message.chat.id,
    "📺 TAREA DISPONIBLE\n\n"
    "1. Ve a YouTube\n"
    "2. Busca: 'viajes Noruega'\n"
    "3. Dale 👍 y suscríbete\n"
    "4. Envía 'listo'\n\n"
    "💰 Pago: 10 Bs")

# ── SALDO ──
@bot.message_handler(commands=["saldo"])
def saldo(message):
    saldo = usuarios.get(message.chat.id, {}).get("saldo", 0)
    bot.send_message(message.chat.id, f"💰 Tu saldo: {saldo} Bs")

# ── VIP ──
@bot.message_handler(commands=["vip"])
def vip(message):
    bot.send_message(message.chat.id,
    "💎 NIVELES VIP:\n\n"
    "VIP 1 → 200 Bs → gana 260 Bs\n"
    "VIP 2 → 500 Bs → gana 650 Bs\n"
    "VIP 3 → 800 Bs → gana 1040 Bs\n\n"
    "📩 Escribe: comprar vip")

# ── RESPUESTAS ──
@bot.message_handler(func=lambda msg: True)
def mensajes(message):
    texto = message.text.lower()
    user_id = message.chat.id

   if user_id not in usuarios:
    usuarios[user_id] = {"saldo": 0}

if texto == "listo":
    usuarios[user_id]["saldo"] += 10
        bot.send_message(user_id, "✅ Tarea completada\n💰 +10 Bs agregados")

    elif "comprar vip" in texto:
        bot.send_message(user_id,
        "💳 Para comprar VIP envía comprobante\n"
        "📩 Contacta al admin")

    elif "hola" in texto:
        bot.send_message(user_id, "Hola 👋 usa /tarea para empezar")

    else:
        bot.send_message(user_id, "❓ Usa /tarea para comenzar")

print("Bot activo...")
bot.infinity_polling()
