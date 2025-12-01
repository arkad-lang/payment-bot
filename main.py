# main.py (для Railway — polling)
import os
import json
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

# === CONFIG ===
TOKEN = os.getenv("BOT_TOKEN")
# Убираем webhook — используем polling

# === PAYMENTS (взято строго из ваших файлов) ===
PAYMENTS = [
    # Мани Мен #1 (дог. 32715330)
    {"date": "08.12.2025", "sum": 6407.65, "org": "Мани Мен #1", "paid": False},
    {"date": "22.12.2025", "sum": 6407.65, "org": "Мани Мен #1", "paid": False},
    {"date": "05.01.2026", "sum": 6407.66, "org": "Мани Мен #1", "paid": False},
    {"date": "19.01.2026", "sum": 6407.65, "org": "Мани Мен #1", "paid": False},
    {"date": "02.02.2026", "sum": 6407.65, "org": "Мани Мен #1", "paid": False},
    {"date": "16.02.2026", "sum": 6407.65, "org": "Мани Мен #1", "paid": False},
    {"date": "02.03.2026", "sum": 6407.66, "org": "Мани Мен #1", "paid": False},

    # Мани Мен #2 (дог. 32604563) — 1-й платёж погашен
    {"date": "29.11.2025", "sum": 3730.37, "org": "Мани Мен #2", "paid": True},
    {"date": "13.12.2025", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "27.12.2025", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "10.01.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "24.01.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "07.02.2026", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "21.02.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "07.03.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "21.03.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "04.04.2026", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "18.04.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "02.05.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "16.05.2026", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "30.05.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "13.06.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "27.06.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "11.07.2026", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "25.07.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "08.08.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "22.08.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "05.09.2026", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "19.09.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "03.10.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "17.10.2026", "sum": 3730.36, "org": "Мани Мен #2", "paid": False},
    {"date": "31.10.2026", "sum": 3730.37, "org": "Мани Мен #2", "paid": False},
    {"date": "14.11.2026", "sum": 3669.48, "org": "Мани Мен #2", "paid": False},

    # А Деньги (дог. 40748164)
    {"date": "13.12.2025", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "27.12.2025", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "10.01.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "24.01.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "07.02.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "21.02.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "07.03.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "21.03.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "04.04.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "18.04.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "02.05.2026", "sum": 7541.50, "org": "А Деньги", "paid": False},
    {"date": "16.05.2026", "sum": 7541.54, "org": "А Деньги", "paid": False},

    # Микрозайм (дог. 150-25885581)
    {"date": "15.12.2025", "sum": 29760.00, "org": "Микрозайм", "paid": False},
]

def parse_date(s):
    return datetime.strptime(s, "%d.%m.%Y").date()

# === BOT INIT ===
bot = Bot(token=TOKEN)
dp = Dispatcher()

# === COMMANDS ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "✅ Бот запущен.\n\n"
        "Команды:\n"
        "/plan — ближайшие платежи\n"
        "/all — весь график\n"
        "/paid ДД.ММ — отметить как оплачено\n\n"
        "🔔 Напоминания приходят за 3, 1 и в день платежа."
    )

@dp.message(Command("plan"))
async def cmd_plan(message: types.Message):
    today = datetime.now().date()
    upcoming = [p for p in PAYMENTS if not p["paid"] and parse_date(p["date"]) >= today]
    upcoming.sort(key=lambda x: parse_date(x["date"]))
    
    if not upcoming:
        await message.answer("✅ Все платежи оплачены!")
        return

    text = "<b>📅 Ближайшие 5 платежей:</b>\n"
    for p in upcoming[:5]:
        d = parse_date(p["date"])
        days = (d - today).days
        warn = "❗" if days <= 3 else ""
        text += f"\n{warn} <b>{p['date']}</b> — {p['org']} — <b>{p['sum']:,.2f} ₽</b> ({'сегодня' if days == 0 else f'через {days} дн.' if days > 0 else 'просрочка!'})"
    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("all"))
async def cmd_all(message: types.Message):
    text = "<b>📊 Весь график:</b>\n"
    for p in PAYMENTS:
        mark = "✅" if p["paid"] else "⏳"
        text += f"\n{mark} {p['date']} — {p['org']} — {p['sum']:,.2f} ₽"
        if len(text) > 3800:
            await message.answer(text, parse_mode=ParseMode.HTML)
            text = ""
    if text:
        await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("paid"))
async def cmd_paid(message: types.Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            raise ValueError
        date_input = parts[1].strip()

        # Нормализация: ДД.ММ → ДД.ММ.2025/2026
        if len(date_input) == 5 and date_input.count('.') == 1:
            day, month = map(int, date_input.split('.'))
            year = 2025 if (month >= 12 or (month == 11 and day >= 29)) else 2026
            date_input = f"{day:02d}.{month:02d}.{year}"

        found = False
        for p in PAYMENTS:
            if p["date"] == date_input and not p["paid"]:
                p["paid"] = True
                found = True
                d = parse_date(p["date"])
                await message.answer(f"✅ Отмечено: {p['date']} — {p['org']} — {p['sum']:,.2f} ₽")
                break
        if not found:
            await message.answer("❌ Не найден неоплаченный платёж на эту дату.")
    except Exception as e:
        await message.answer("❌ Используйте: /paid ДД.ММ или /paid ДД.ММ.ГГ")

# === NOTIFICATIONS ===
import asyncio

async def send_reminders():
    while True:
        await asyncio.sleep(3600)  # Проверка каждые час
        today = datetime.now().date()
        for p in PAYMENTS:
            if p["paid"]:
                continue
            d = parse_date(p["date"])
            days_left = (d - today).days
            if days_left in [3, 1, 0]:
                warn = "❗❗❗" if days_left == 0 else "❗"
                text = f"{warn} <b>Напоминание:</b>\n📅 {p['date']}\n→ {p['org']}\n→ <b>{p['sum']:,.2f} ₽</b>"
                if days_left == 0:
                    text += "\n\n🔴 <b>Сегодня последний день оплаты!</b>"
                try:
                    # Замените на ваш chat_id (напишите /start боту и получите его)
                    await bot.send_message(chat_id="123456789", text=text, parse_mode=ParseMode.HTML)
                except Exception as e:
                    logging.error(f"Failed to send: {e}")

# === MAIN ===
if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_plan, Command("plan"))
    dp.message.register(cmd_all, Command("all"))
    dp.message.register(cmd_paid, Command("paid"))

    # Запуск напоминаний в фоне
    loop = asyncio.get_event_loop()
    loop.create_task(send_reminders())

    # Запуск бота в режиме polling
    loop.run_until_complete(dp.start_polling(bot))
