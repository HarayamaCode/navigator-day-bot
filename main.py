import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from replit import db  # Подключаем память

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет, Стефания! Я твой планировщик. Можешь использовать /add, /list, /done, /help."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/help - список команд\n"
        "/add [текст] - добавить задачу\n"
        "/list - показать все задачи\n"
        "/done [номер] - отметить задачу выполненной"
    )

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = ' '.join(context.args)
    if not task_text:
        await update.message.reply_text("Пожалуйста, укажи текст задачи после команды /add")
        return
    tasks = db.get("tasks", [])
    tasks.append(task_text)
    db["tasks"] = tasks
    await update.message.reply_text(f"Задача добавлена: {task_text}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = db.get("tasks", [])
    if not tasks:
        await update.message.reply_text("У тебя пока нет задач.")
        return
    response = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
    await update.message.reply_text(f"Твои задачи:\n{response}")

async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Укажи номер задачи после команды /done")
        return
    index = int(context.args[0]) - 1
    tasks = db.get("tasks", [])
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        db["tasks"] = tasks
        await update.message.reply_text(f"Задача выполнена и удалена: {removed}")
    else:
        await update.message.reply_text("Неверный номер задачи.")

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        logger.error("BOT_TOKEN не задан в переменных окружения")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done_task))

    app.run_polling()

if __name__ == "__main__":
    main()
