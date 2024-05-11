import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import markdown

import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import telegram

from html import escape

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    escaped_name = escape(user.first_name)
    await update.message.reply_html(
        rf"Hi <a href='tg://user?id={user.id}'>{escaped_name}</a>!",
        reply_to_message_id=update.message.message_id,
    )
    #await update.message.reply_text(f"/start for start \n /help for help")


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message when the command /help is issued."""
#     await update.message.reply_text("Help!")
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
def to_html(text):
    html = markdown.markdown(text)
    return html
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    response = model.generate_content(update.message.text)
    #html_text = to_html(to_markdown(response.text).data)
    # await update.message.sender_chat()
    await update.message.reply_text(rf"{response.text}",parse_mode='Markdown')
genai.configure(api_key="api-key-here")
model = genai.GenerativeModel('gemini-pro')



def get_input(update, context):
    user_text = update.message.text
    update.message.reply_text(f"You said: {user_text}")
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("token?").build()
    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
