import requests
import time
import telebot

# 🔹 Configuración de tu bot de Telegram
TELEGRAM_BOT_TOKEN = "TU_TOKEN_DEL_BOT"
TELEGRAM_CHAT_ID = "TU_CHAT_ID"

# 🔹 API de CryptoPanic para noticias cripto
CRYPTOPANIC_API_KEY = "TU_API_KEY_DE_CRYPTOPANIC"
CRYPTOPANIC_URL = "https://cryptopanic.com/api/v1/posts/?auth_token=" + CRYPTOPANIC_API_KEY + "&filter=important"

# 🔹 API de Binance para precios de criptos
BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

# 🔹 Lista de criptos a monitorear
MONEDAS = ["BTC", "ETH", "XRP", "PEPE", "PENGU", "TRUMP", "QDT"]

# 🔹 Inicializa el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def obtener_noticias():
    """Obtiene noticias importantes de CryptoPanic"""
    try:
        response = requests.get(CRYPTOPANIC_URL)
        data = response.json()
        noticias = data.get("results", [])

        mensajes = []
        for noticia in noticias[:5]:  # Solo las 5 más recientes
            titulo = noticia["title"]
            enlace = noticia["url"]
            mensajes.append(f"📰 {titulo}\n🔗 {enlace}")

        return mensajes
    except Exception as e:
        print("Error obteniendo noticias:", e)
        return []

def obtener_precios():
    """Obtiene precios de criptos desde Binance"""
    try:
        response = requests.get(BINANCE_URL)
        precios = response.json()
        precios_filtrados = [f"{p['symbol']}: {p['price']}" for p in precios if p['symbol'][:-4] in MONEDAS]
        return precios_filtrados
    except Exception as e:
        print("Error obteniendo precios:", e)
        return []

def enviar_alertas():
    """Envía alertas a Telegram con noticias y precios"""
    while True:
        # Obtener noticias y precios
        noticias = obtener_noticias()
        precios = obtener_precios()

        # Enviar noticias
        for noticia in noticias:
            bot.send_message(TELEGRAM_CHAT_ID, noticia)
            time.sleep(2)

        # Enviar precios
        mensaje_precios = "💰 **Precios de Criptos**:\n" + "\n".join(precios)
        bot.send_message(TELEGRAM_CHAT_ID, mensaje_precios)

        # Esperar 30 minutos antes de la siguiente alerta
        time.sleep(1800)

if __name__ == "__main__":
    bot.send_message(TELEGRAM_CHAT_ID, "🤖 Bot de Alertas Cripto Iniciado 🚀")
    enviar_alertas()
