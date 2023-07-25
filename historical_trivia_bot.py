import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Your Telegram Bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Historical trivia questions and answers
questions = [
    {"question": "In which year did Christopher Columbus reach the Americas?", "answer": "1492"},
    {"question": "Who was the first President of the United States?", "answer": "George Washington"},
    # Add more historical trivia questions and answers here
]

def start(update: Update, context: CallbackContext) -> None:
    """Handler for the /start command."""
    update.message.reply_text("Welcome to the Historical Trivia Game Bot! "
                              "Test your knowledge of history by answering trivia questions from different time periods and cultures. "
                              "Choose an option below to begin playing!")
    show_menu(update)

def show_menu(update: Update) -> None:
    """Display the main menu with quiz options."""
    keyboard = [[InlineKeyboardButton("Play Historical Trivia", callback_data='play')],
                [InlineKeyboardButton("About", callback_data='about')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select an option:", reply_markup=reply_markup)

def start_quiz(update: Update, context: CallbackContext) -> None:
    """Start the historical trivia quiz."""
    random_question = random.choice(questions)
    context.user_data['current_question'] = random_question
    update.message.reply_text(random_question["question"])

def check_answer(update: Update, context: CallbackContext) -> None:
    """Check the user's answer to the current question."""
    user_answer = update.message.text
    current_question = context.user_data['current_question']
    if user_answer.strip().lower() == current_question["answer"].lower():
        update.message.reply_text("Correct answer! Well done!")
    else:
        update.message.reply_text("Incorrect answer. Try again!")

def about(update: Update) -> None:
    """Display information about the bot."""
    update.message.reply_text("The Historical Trivia Game Bot is a Telegram bot that quizzes you on historical events, figures, and facts from different time periods and cultures. Have fun and test your historical knowledge!")

def main() -> None:
    """Main function to start the bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(start_quiz, pattern='^play$'))
    dispatcher.add_handler(CallbackQueryHandler(about, pattern='^about$'))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
