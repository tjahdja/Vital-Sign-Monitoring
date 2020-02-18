from telegram.ext import Updater, CommandHandler
import requests

class PyBot:
    def __init__(self):
        super().__init__()

    def init(self):
        self.token ='1071924346:AAEEzY1BokxY-6lONZMC5VVNm661R24Cg2A'
        self.bot_id = '913685701'
        self.updater = Updater(self.token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('hello',self.hello))
        self.updater.dispatcher.add_handler(CommandHandler('check',self.check))
        self.updater.start_polling()

    def hello (self, update, context):
        update.message.reply_text("selamat datang di Vital Sign Bot")

    def check (self, update, context):
        update.message.reply_text(f"detak jantung: {self.beat}, kadar oksigen: {self.spo}, status: {self.stat}")

    def warning(self):
        pesan = 'Pasien dalam keadaan kritis'
        send_text ='https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.bot_id + '&parse_mode=Markdown&text=' + pesan
        response = requests.get(send_text)
        return response.json()

    def get_val(self, dtk, oxy, status):
        self.beat = dtk
        self.spo = oxy
        self.stat = status