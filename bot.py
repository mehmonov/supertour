import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Telegram bot token
BOT_TOKEN = "7389653878:AAHO23jlUn-qDJlHnMmfydXX1oqzkMYLogQ"

bot = telebot.TeleBot(BOT_TOKEN)

def get_db_connection():
    return sqlite3.connect('db.sqlite3')

# Start command
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Salom! Bu tur paketlarini izlash va band qilish botidir. \n\n" +
        "Quyidagi komandalarni ishlating:\n" +
        "/destinations - Manzillar ro'yxatini ko'rish\n" +
        "/search - Tur paketlarini qidirish\n" +
        "/book - Tur paketini band qilish"
    )

# Show destinations
@bot.message_handler(commands=['destinations'])
def list_destinations(message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM home_destination")
    destinations = cursor.fetchall()
    conn.close()

    if destinations:
        response = "Manzillar ro'yxati:\n"
        for dest in destinations:
            response += f"\n{dest[0]}: {dest[1]}"
    else:
        response = "Hech qanday manzil topilmadi."
    bot.send_message(message.chat.id, response)

# Search tour packages
@bot.message_handler(commands=['search'])
def search_tour_packages(message):
    msg = bot.send_message(message.chat.id, "Qaysi manzilni izlayapsiz?")
    bot.register_next_step_handler(msg, show_tours_by_destination)

def show_tours_by_destination(message):
    query = message.text
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT home_tourpackage.id, home_tourpackage.name, home_tourpackage.description, home_tourpackage.price, home_tourpackage.start_date, home_tourpackage.end_date 
        FROM home_tourpackage 
        INNER JOIN home_destination ON home_tourpackage.destination_id = home_destination.id 
        WHERE home_destination.name LIKE ?
    """, (f"%{query}%",))
    tours = cursor.fetchall()
    conn.close()

    if tours:
        for tour in tours:
            markup = InlineKeyboardMarkup()
            button = InlineKeyboardButton("Band qilish", callback_data=f"book_{tour[0]}")
            markup.add(button)

            response = (
                f"{tour[1]}: {tour[2]}\n" +
                f"Narxi: {tour[3]} so'm\n" +
                f"Boshlanish: {tour[4]}, Tugash: {tour[5]}"
            )
            bot.send_message(message.chat.id, response, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Tur paketlari topilmadi.")

# Callback handler for booking
def handle_booking(call):
    tour_id = call.data.split('_')[1]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM home_tourpackage WHERE id = ?", (tour_id,))
    tour = cursor.fetchone()
    conn.close()

    if tour:
        msg = bot.send_message(call.message.chat.id, "Ismingizni kiriting:")
        bot.register_next_step_handler(msg, lambda m: save_booking(m, tour_id, tour[0]))

@bot.callback_query_handler(func=lambda call: call.data.startswith('book_'))
def callback_query(call):
    handle_booking(call)

def save_booking(message, tour_id, tour_name):
    first_name = message.text
    msg = bot.send_message(message.chat.id, "Telefon raqamingizni kiriting:")
    bot.register_next_step_handler(msg, lambda m: finalize_booking(m, tour_id, tour_name, first_name))

def finalize_booking(message, tour_id, tour_name, first_name):
    phone_number = message.text
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO home_booking (tour_package_id, first_name, phone_number, status, active, booking_date) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
        (tour_id, first_name, phone_number, 'PENDING', 1)
    )
    conn.commit()
    conn.close()

    bot.send_message(
        message.chat.id,
        f"Rahmat! Sizning bandlovingiz qabul qilindi. \nBandlangan tur: {tour_name}."
    )

# Run bot
if __name__ == "__main__":
    print("Bot ishga tushdi")
    bot.polling(none_stop=True)
