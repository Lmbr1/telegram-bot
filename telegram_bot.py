import os
import telebot

# 🔑 Obtener token desde Railway
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise Exception("Falta TELEGRAM_TOKEN en Railway")

bot = telebot.TeleBot(TOKEN)

usuarios = {}

# ── START ──
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    usuarios[user_id] = {"saldo": 0}

    bot.send_message(user_id,
    "👋 Bienvenido al sistema de tareas\n\n"
    "💰 Gana dinero realizando tareas simples\n"
    "📊 Ganancias: 5 - 50 Bs por tarea\n\n"
    "📌 Comandos:\n"
    "/vip - Ver niveles VIP\n"
    "/saldo - Ver saldo")

# ── SALDO ──
@bot.message_handler(commands=["saldo"])
def saldo(message):
    user_id = message.chat.id

    if user_id not in usuarios:
        usuarios[user_id] = {"saldo": 0}

    saldo = usuarios[user_id]["saldo"]
    bot.send_message(user_id, f"💰 Tu saldo: {saldo} Bs")

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

    # 🔧 evitar crash si no existe usuario
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
        bot.send_message(user_id, "Hola 👋 usa /vip para ver los niveles")

    else:
        bot.send_message(user_id, "❓ Usa /vip para ver los niveles disponibles")

print("✅ Bot activo...")
bot.infinity_polling()
