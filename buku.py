import telebot
from telebot import types

api = '7488501557:AAHO4e3OaYRQcwx0tao3Atz6m1DTHruZT5E'
bot = telebot.TeleBot(api)

# ID admin yang terdaftar (admin utama adalah admin pertama)
admin_ids = {7065804264}
main_admin_id = 7065804264  # Admin utama

# Simpan buku dalam genre
books = {
    'School': [],
    'Novel': [],
    'History': []
}

# Simpan permintaan buku
book_requests = []

# Simpan data pengguna
user_data = {main_admin_id: {'name': 'Admin', 'blocked': False, 'motivation_enabled': False}}

# Fungsi untuk membuat tombol menu
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('📚 Choice Book')
    btn2 = types.KeyboardButton('⚙️ Settings')
    btn3 = types.KeyboardButton('❓ Help')
    btn4 = types.KeyboardButton('📝 Book Request')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def create_genre_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('🏫 School')
    btn2 = types.KeyboardButton('📖 Novel')
    btn3 = types.KeyboardButton('📜 History')
    btn4 = types.KeyboardButton('🔙 Back to Main Menu')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def create_settings_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('➕ Add Book')
    btn2 = types.KeyboardButton('➖ Remove Book')
    btn3 = types.KeyboardButton('📋 Book Requests')
    btn4 = types.KeyboardButton('👥 User Data')
    btn5 = types.KeyboardButton('📋 Manage Admins')
    btn6 = types.KeyboardButton('💡 Manage Motivation')
    btn7 = types.KeyboardButton('🔙 Back to Main Menu')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

def create_user_data_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('🔒 Block User')
    btn2 = types.KeyboardButton('🔓 Unblock User')
    btn3 = types.KeyboardButton('🔙 Back to Settings Menu')
    markup.add(btn1, btn2, btn3)
    return markup

def create_manage_admins_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('➕ Add Admin')
    btn2 = types.KeyboardButton('➖ Remove Admin')
    btn3 = types.KeyboardButton('📋 List Admins')
    btn4 = types.KeyboardButton('🔙 Back to Settings Menu')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def create_manage_motivation_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('🔔 Enable Motivation')
    btn2 = types.KeyboardButton('🔕 Disable Motivation')
    btn3 = types.KeyboardButton('📤 Send Motivation')
    btn4 = types.KeyboardButton('📤 Send Motivation Sticker')
    btn5 = types.KeyboardButton('🔙 Back to Settings Menu')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

# Fungsi untuk menangani /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(user_id, "Welcome to BearBooks! Please register to use the bot. Send your name:")
        bot.register_next_step_handler(message, register_user)
    elif user_data[user_id].get('blocked'):
        bot.send_message(user_id, "You have been blocked from using this bot.")
    else:
        welcome_message = (
            "Welcome back to BearBooks! 📚\n\n"
            "We are delighted to have you here in our community of book lovers. "
            "Feel free to explore, discuss, and share your favorite books with us. "
            "Happy reading! 📖"
        )
        bot.send_message(user_id, welcome_message, reply_markup=create_main_menu())

def register_user(message):
    user_id = message.from_user.id
    user_name = message.text.strip()
    user_data[user_id] = {'name': user_name, 'blocked': False, 'motivation_enabled': False}
    bot.send_message(user_id, f"Thank you for registering, {user_name}! You can now use the bot.", reply_markup=create_main_menu())

# Fungsi untuk menangani pesan
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(user_id, "Please register to use the bot. Send your name:")
        bot.register_next_step_handler(message, register_user)
        return
    elif user_data[user_id].get('blocked'):
        bot.send_message(user_id, "You have been blocked from using this bot.")
        return

    if message.text == '📚 Choice Book':
        bot.send_message(message.chat.id, "Select a genre:", reply_markup=create_genre_menu())
    elif message.text == '⚙️ Settings':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Settings Menu:", reply_markup=create_settings_menu())
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can access the settings.")
    elif message.text == '❓ Help':
        help_message = (
            "Here is how you can use BearBooks bot:\n\n"
            "- **📚 Choice Book**: Choose a book genre.\n"
            "- **⚙️ Settings**: Admin settings.\n"
            "- **❓ Help**: Display this help message.\n"
            "- **📝 Book Request**: Request information about a book.\n\n"
            "Feel free to explore the options and enjoy your reading journey!"
        )
        bot.send_message(message.chat.id, help_message, reply_markup=create_main_menu())
    elif message.text == '📝 Book Request':
        bot.send_message(message.chat.id, "Please provide the book title you are interested in:")
        bot.register_next_step_handler(message, handle_book_request)
    elif message.text in ['🏫 School', '📖 Novel', '📜 History']:
        genre_map = {'🏫 School': 'School', '📖 Novel': 'Novel', '📜 History': 'History'}
        current_genre = genre_map[message.text]
        books_list = books[current_genre]
        book_list_message = '\n'.join([f"{i+1}. {book['title']} - {book['link']}" for i, book in enumerate(books_list)])
        if book_list_message:
            bot.send_message(message.chat.id, f"Books in {current_genre} genre:\n\n{book_list_message}")
        else:
            bot.send_message(message.chat.id, f"No books available in {current_genre} genre.")
    elif message.text == '➕ Add Book':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the book details in the format:\nGenre: [genre]\nTitle: [title]\nLink: [link]")
            bot.register_next_step_handler(message, add_book)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can add books.")
    elif message.text == '➖ Remove Book':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the book details in the format:\nGenre: [genre]\nNumber: [number]")
            bot.register_next_step_handler(message, remove_book)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can remove books.")
    elif message.text == '📋 Book Requests':
        if user_id in admin_ids:
            requests_list = '\n'.join([f"{i+1}. {req['title']} (User ID: {req['user_id']})" for i, req in enumerate(book_requests)])
            if requests_list:
                bot.send_message(message.chat.id, f"Book Requests:\n\n{requests_list}")
            else:
                bot.send_message(message.chat.id, "No book requests available.")
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can view book requests.")
    elif message.text == '👥 User Data':
        if user_id in admin_ids:
            user_data_message = '\n'.join([f"User ID: {id}, Name: {data['name']}" for id, data in user_data.items()])
            bot.send_message(message.chat.id, f"User Data:\n{user_data_message}", reply_markup=create_user_data_menu())
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can view user data.")
    elif message.text == '📋 Manage Admins':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Manage Admins Menu:", reply_markup=create_manage_admins_menu())
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can manage admins.")
    elif message.text == '💡 Manage Motivation':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Manage Motivation Menu:", reply_markup=create_manage_motivation_menu())
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can manage motivation.")
    elif message.text == '🔒 Block User':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the User ID to block:")
            bot.register_next_step_handler(message, block_user)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can block users.")
    elif message.text == '🔓 Unblock User':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the User ID to unblock:")
            bot.register_next_step_handler(message, unblock_user)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can unblock users.")
    elif message.text == '➕ Add Admin':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the User ID to add as admin:")
            bot.register_next_step_handler(message, add_admin)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can add new admins.")
    elif message.text == '➖ Remove Admin':
        if user_id == main_admin_id:
            bot.send_message(message.chat.id, "Please provide the User ID to remove from admin:")
            bot.register_next_step_handler(message, remove_admin)
        else:
            bot.send_message(message.chat.id, "Sorry, only the main admin can remove other admins.")
    elif message.text == '📋 List Admins':
        if user_id in admin_ids:
            admin_list_message = '\n'.join([f"Admin ID: {admin_id}" for admin_id in admin_ids])
            bot.send_message(message.chat.id, f"Admins List:\n{admin_list_message}")
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can view the list of admins.")
    elif message.text == '🔔 Enable Motivation':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the User ID to enable motivation for:")
            bot.register_next_step_handler(message, enable_motivation)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can enable motivation.")
    elif message.text == '🔕 Disable Motivation':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the User ID to disable motivation for:")
            bot.register_next_step_handler(message, disable_motivation)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can disable motivation.")
    elif message.text == '📤 Send Motivation':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the motivation message to send:")
            bot.register_next_step_handler(message, send_motivation_message)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can send motivation messages.")
    elif message.text == '📤 Send Motivation Sticker':
        if user_id in admin_ids:
            bot.send_message(message.chat.id, "Please provide the motivation sticker ID to send:")
            bot.register_next_step_handler(message, send_motivation_sticker)
        else:
            bot.send_message(message.chat.id, "Sorry, only admins can send motivation stickers.")
    elif message.text == '🔙 Back to Main Menu':
        bot.send_message(message.chat.id, "Main Menu:", reply_markup=create_main_menu())
    elif message.text == '🔙 Back to Settings Menu':
        bot.send_message(message.chat.id, "Settings Menu:", reply_markup=create_settings_menu())

# Fungsi untuk menangani permintaan buku
def handle_book_request(message):
    user_id = message.from_user.id
    if message.content_type == 'text':
        book_title = message.text.strip()
        book_requests.append({'user_id': user_id, 'title': book_title})
        bot.send_message(message.chat.id, "Thank you! Your request has been noted.")
    else:
        bot.send_message(message.chat.id, "Please send only text for the book title.")

# Fungsi untuk menambahkan buku
def add_book(message):
    try:
        parts = message.text.split('\n')
        genre = parts[0].split(': ')[1]
        title = parts[1].split(': ')[1]
        link = parts[2].split(': ')[1]
        books[genre].append({'title': title, 'link': link})
        bot.send_message(message.chat.id, f"The book '{title}' has been added to the {genre} genre.")
    except (IndexError, KeyError):
        bot.send_message(message.chat.id, "Invalid format. Please provide the book details in the format:\nGenre: [genre]\nTitle: [title]\nLink: [link]")

# Fungsi untuk menghapus buku
def remove_book(message):
    try:
        parts = message.text.split('\n')
        genre = parts[0].split(': ')[1]
        number = int(parts[1].split(': ')[1])
        removed_book = books[genre].pop(number - 1)
        bot.send_message(message.chat.id, f"The book '{removed_book['title']}' has been removed from the {genre} genre.")
    except (IndexError, KeyError, ValueError):
        bot.send_message(message.chat.id, "Invalid format or number. Please provide the book details in the format:\nGenre: [genre]\nNumber: [number]")

# Fungsi untuk memblokir pengguna
def block_user(message):
    try:
        user_id_to_block = int(message.text.strip())
        if user_id_to_block in user_data:
            user_data[user_id_to_block]['blocked'] = True
            bot.send_message(message.chat.id, f"User ID {user_id_to_block} has been blocked.")
        else:
            bot.send_message(message.chat.id, "User ID not found.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid User ID.")

# Fungsi untuk membuka blokir pengguna
def unblock_user(message):
    try:
        user_id_to_unblock = int(message.text.strip())
        if user_id_to_unblock in user_data:
            user_data[user_id_to_unblock]['blocked'] = False
            bot.send_message(message.chat.id, f"User ID {user_id_to_unblock} has been unblocked.")
        else:
            bot.send_message(message.chat.id, "User ID not found.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid User ID.")

# Fungsi untuk menambahkan admin
def add_admin(message):
    try:
        user_id_to_add = int(message.text.strip())
        if user_id_to_add in user_data:
            admin_ids.add(user_id_to_add)
            bot.send_message(message.chat.id, f"User ID {user_id_to_add} has been added as an admin.")
        else:
            bot.send_message(message.chat.id, "User ID not found.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid User ID.")

# Fungsi untuk menghapus admin
def remove_admin(message):
    try:
        user_id_to_remove = int(message.text.strip())
        if user_id_to_remove in admin_ids and user_id_to_remove != main_admin_id:
            admin_ids.remove(user_id_to_remove)
            bot.send_message(message.chat.id, f"User ID {user_id_to_remove} has been removed from admins.")
        else:
            bot.send_message(message.chat.id, "User ID not found or is the main admin.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid User ID.")

# Fungsi untuk mengaktifkan motivasi
def enable_motivation(message):
    try:
        user_id_to_enable = int(message.text.strip())
        if user_id_to_enable in user_data:
            user_data[user_id_to_enable]['motivation_enabled'] = True
            bot.send_message(message.chat.id, f"Motivation has been enabled for User ID {user_id_to_enable}.")
        else:
            bot.send_message(message.chat.id, "User ID not found.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid User ID.")

# Fungsi untuk menonaktifkan motivasi
def disable_motivation(message):
    try:
        user_id_to_disable = int(message.text.strip())
        if user_id_to_disable in user_data:
            user_data[user_id_to_disable]['motivation_enabled'] = False
            bot.send_message(message.chat.id, f"Motivation has been disabled for User ID {user_id_to_disable}.")
        else:
            bot.send_message(message.chat.id, "User ID not found.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid User ID.")

# Fungsi untuk mengirim pesan motivasi
def send_motivation_message(message):
    motivation_message = message.text.strip()
    for user_id, data in user_data.items():
        if data['motivation_enabled']:
            bot.send_message(user_id, motivation_message)
    bot.send_message(message.chat.id, "Motivation message sent to all users with motivation enabled.")

# Fungsi untuk mengirim stiker motivasi
def send_motivation_sticker(message):
    sticker_id = message.text.strip()
    for user_id, data in user_data.items():
        if data['motivation_enabled']:
            bot.send_sticker(user_id, sticker_id)
    bot.send_message(message.chat.id, "Motivation sticker sent to all users with motivation enabled.")

bot.polling()