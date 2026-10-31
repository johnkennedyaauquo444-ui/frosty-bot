import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import random

BOT_TOKEN = "9004000347:AAHNX05Z50jT59tjTMpLxGrQLFKj3QcMvHw"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Play Frosty Fortune", callback_data="play")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance"), InlineKeyboardButton("📊 Stats", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "❄️ *Frosty Fortune Bot Activated!* ❄️\n\nWelcome! Tap Play to start winning!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "play":
        win = random.choice(["🎉 You won 100 coins!", "😢 Try again!", "💎 JACKPOT! 1000 coins!"])
        await query.edit_message_text(text=f"{win}\n\nTap /start to play again")
    else:
        await query.edit_message_text(text=f"You clicked {query.data} - Coming soon!")

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Frosty Bot polling started...")
    app.run_polling()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Frosty Bot is Running!")
    def log_message(self, format, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    run_bot()
