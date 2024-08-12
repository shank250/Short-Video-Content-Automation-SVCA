from telegram.ext import Updater, CommandHandler
ALLOWED_USERS = [6004512427]
def telegrambot():
    # Create an Updater object
    updater = Updater(token="6098266248:AAGekqHABpFijxlxyU4Tv7RYP_WSRtQSqNo", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Define command handlers
    def start(update, context):
        user_id = update.effective_user.id
        print(user_id)
        if user_id in ALLOWED_USERS :
            context.bot.send_message(chat_id=update.effective_chat.id, text="yep it started working@!")
            pass
        # else :
        #     context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized to use this bot.")
        #     program_execution()


    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

# if __name__ == '__main__':
while True :
    telegrambot()
