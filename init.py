import os
import telebot
import requests
from dotenv import load_dotenv
config = load_dotenv(".env")

#Asignamos las variables de entorno
telegram_token = os.getenv('TELEGRAM_TOKEN')
metar_token = os.getenv('METAR_TOKEN')

#Instanciamos el bot
bot = telebot.TeleBot(telegram_token)

#Comando start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(message, "Welcome to METARInfo Bot, use /help to obtain commands info")

#Comando ayuda
@bot.message_handler(commands=["help"])
def cmd_start(message):
    #Texto en formato markdown
    texto = 'This is the bot help menu, you can use the **/metar** command or the **/taf** command followed by the ICAO to get the information' + '\n'
    texto += '\n'
    texto += 'If you have problems reading a METAR or a TAF you can check the AEMET guide at the following link' + '\n'
    texto += '\n'
    texto += '[Guia meteorologica ES](https://www.aemet.es/documentos/es/conocermas/aeronautica/AU-GUI-0102.pdf)' + '\n'
    texto += '[Weather guide EN](https://www.aemet.es/documentos/es/conocermas/aeronautica/AU-GUI-0102_en.pdf)' + '\n'

    bot.send_message(message.chat.id, texto, parse_mode='MarkdownV2', disable_web_page_preview=True)

#Respuesta a metar
@bot.message_handler(commands=["metar"])
def cmd_metar(message):
    slice_object = slice(7,11)
    icao = message.text[slice_object]
    r = requests.get(f"https://avwx.rest/api/metar/{icao}?format=json&onfail=cache", headers={ 'Authorization': 'TOKEN '+metar_token })
    respuesta = r.json()
    bot.send_message(message.chat.id, "Metar: "+respuesta['sanitized'])

#Respuesta a taf
@bot.message_handler(commands=["taf"])
def cmd_metar(message):
    slice_object = slice(5,9)
    icao = message.text[slice_object]
    r = requests.get(f"https://avwx.rest/api/taf/{icao}?format=json&onfail=cache", headers={ 'Authorization': 'TOKEN '+metar_token })
    respuesta = r.json()
    bot.send_message(message.chat.id, "Taf: "+respuesta['sanitized'])


#MAIN
if __name__ == '__main__':
    print('Bot starting')
    bot.infinity_polling()
