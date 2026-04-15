import os
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise Exception("Falta TELEGRAM_TOKEN en Railway")

bot = telebot.TeleBot(TOKEN)

usuarios = {}

SALUDOS = [
    "hola", "buen dia", "buenos dias", "buen día",
    "buenas tardes", "buenas noches", "hey", "hi"
]

def asegurar_usuario(user_id):
    if user_id not in usuarios:
        usuarios[user_id] = {
            "saldo": 0,
            "etapa": "inicio"
        }

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)

    usuarios[user_id]["etapa"] = "inicio"

    bot.send_message(
        user_id,
        "👋 Hola\n\n"
        "¿Quieres saber mas sobre mi trabajo?\n"
        "El trabajo consiste en darle like a videos de youtube, no te tomara mucho tiempo y podras hacerlo en tus tiempos libres, por cada like que
        des se acumulan 5 Bs, y aparte hay tareas vip a las que podras ingrsar, te interesa?.\n\n"
        "Escriba 'hola' para comenzar o use /vip para ver los niveles."
    )

@bot.message_handler(commands=["saldo"])
def saldo(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)
    bot.send_message(user_id, f"💰 Su saldo registrado es: {usuarios[user_id]['saldo']} Bs")

@bot.message_handler(commands=["vip"])
def vip(message):
    user_id = message.chat.id
    asegurar_usuario(user_id)

    bot.send_message(
        user_id,
        "💎 NIVELES VIP DISPONIBLES:\n\n"
        "VIP 1 → 200 Bs → retorno referencial 260 Bs\n"
        "VIP 2 → 500 Bs → retorno referencial 650 Bs\n"
        "VIP 3 → 800 Bs → retorno referencial 1040 Bs\n\n"
        "📩 Escriba: comprar vip\n"
        "📌 También puede escribir: tarea"
    )

@bot.message_handler(func=lambda msg: True, content_types=["text"])
def mensajes(message):
    user_id = message.chat.id
    texto = message.text.strip().lower()

    asegurar_usuario(user_id)

    if texto in SALUDOS:
        usuarios[user_id]["etapa"] = "oferta"
        bot.send_message(
            user_id,
            "Hola, ¿le gustaría ganar dinero?\n\n"
            "Es muy facil solo te tomara unos minutos realizar, las tareas.\n\n"
            "Si desea continuar, responda: si quiero"
        )

    elif texto == "si quiero":
        if usuarios[user_id]["etapa"] == "oferta":
            usuarios[user_id]["etapa"] = "continuar"
            bot.send_message(
                user_id,
                "Perfecto.\n\n"
                "Para continuar, escriba /vip y revise los niveles disponibles.\n"
                "Luego podrá escribir 'tarea' para ver una actividad de ejemplo."
            )
        else:
            bot.send_message(user_id, "Primero escriba 'hola' para iniciar.")

    elif texto == "tarea":
        usuarios[user_id]["etapa"] = "tarea"
        bot.send_message(
            user_id,
            "📺 TAREA DE EJEMPLO\n\n"
            "1. Abra YouTube\n"
            "2. Busque un video promocional\n"
            "3. Interactúe con el contenido\n"
            "4. Escriba: listo\n\n"
            "💰 Bonificación demostrativa: 5 Bs"
        )

    elif texto == "listo":
        usuarios[user_id]["saldo"] += 5
        bot.send_message(
            user_id,
            f"✅ Registro completado.\n💰 Se añadieron 5 Bs.\nSaldo actual: {usuarios[user_id]['saldo']} Bs"
        )

    elif "comprar vip" in texto:
        bot.send_message(
            user_id,
            "💳 Para información sobre membresías VIP, envíe su comprobante o contacte al administrador."
        )

    else:
        bot.send_message(
            user_id,
            "Escriba 'hola' para comenzar, /vip para ver niveles, 'tarea' para una actividad o /saldo para ver su saldo."
        )

print("✅ Bot activo...")
bot.infinity_polling()
