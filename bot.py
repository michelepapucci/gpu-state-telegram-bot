import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from pynvml import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

nvmlInit()


async def gpu_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    device_count = nvmlDeviceGetCount()
    for i in range(device_count):
        logging.info(f"Received /gpu_state from: {update.effective_chat.id}")
        handle = nvmlDeviceGetHandleByIndex(i)
        info = nvmlDeviceGetMemoryInfo(handle)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Device: {nvmlDeviceGetName(handle)}\n"
                                            f"Used Memory {info.used}/{info.total} - Remaining: {info.free}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start from: {update.effective_chat.id}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ciao! ti tormenterò d'ora in poi!")


if __name__ == '__main__':
    token_key = os.environ.get('TELEGRAM_BOT_TOKEN')
    application = ApplicationBuilder().token(token_key).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    gpu_handler = CommandHandler('gpu_state', gpu_state)
    application.add_handler(gpu_handler)

    application.run_polling()
