import telebot

API_TOKEN = '7854776613:AAGu2iztlE9NEXTWjdpansUw8-jgWVr_GJ8'
bot = telebot.TeleBot(API_TOKEN)

ARQUIVO_EMAILS = 'autorizados.txt'
LINK_SUPORTE = 'https://bit.ly/3k0xhxK'

def carregar_emails():
    try:
        with open(ARQUIVO_EMAILS, 'r') as f:
            return [linha.strip().lower() for linha in f.readlines()]
    except FileNotFoundError:
        return []

def salvar_emails(emails):
    with open(ARQUIVO_EMAILS, 'w') as f:
        for email in emails:
            f.write(email + '\n')

@bot.message_handler(commands=['add'])
def add_email(message):
    email = message.text.replace('/add', '').strip().lower()
    if not email:
        bot.reply_to(message, "⚠️ Digite um e-mail após o comando. Ex: /add email@teste.com")
        return
    emails = carregar_emails()
    if email not in emails:
        emails.append(email)
        salvar_emails(emails)
    bot.reply_to(message, f"Adicionei o email:\n{email}")

@bot.message_handler(commands=['remover'])
def remover_email(message):
    email = message.text.replace('/remover', '').strip().lower()
    emails = carregar_emails()
    if email in emails:
        emails.remove(email)
        salvar_emails(emails)
        bot.reply_to(message, f"O cliente foi removido: {email}")
        bot.send_message(message.chat.id, f"Removi o pagamento de {email}")
    else:
        bot.reply_to(message, f"Não foi possível remover o PAGAMENTO de {email}, verifique se o email está certo!")

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    botao = telebot.types.KeyboardButton("Iniciar Atendimento")
    markup.add(botao)
    bot.send_message(message.chat.id,
        "Utilize o comando /start ou clique no botão iniciar o atendimento",
        reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def tratar_mensagem(message):
    texto = message.text.strip().lower()

    if '@' in texto:
        emails = carregar_emails()
        if texto in emails:
            bot.reply_to(message,
                "Olá! Add pelo bot seu cadastro já consta como ativo no nosso grupo!\n\nSe algo estiver errado, entre em contato com o suporte digitando /suporte.")
        else:
            bot.reply_to(message,
                f"Sua assinatura não está ativa no sistema!!!\n\nFale com a gente através do link {LINK_SUPORTE}")
    else:
        bot.reply_to(message,
            "Não entendo isso\n\nUtilize o comando /start ou clique no botão iniciar o atendimento")

@bot.message_handler(commands=['suporte'])
def suporte(message):
    bot.reply_to(message, f"Fale com nosso time pelo WhatsApp:\n{LINK_SUPORTE}")

print("BOT rodando igual ao dos prints com mensagens completas ✅")
bot.polling()