import sys
import os
import django
import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


os.environ["DJANGO_SETTINGS_MODULE"] = "Cloudy.settings"


django.setup()

bot = telebot.TeleBot("7343417017:AAEpZmgL34oOamR6A9oUy6DdVFj2ilOBD2I")






from tgbot.models import Student, Teacher, Group


ADMIN_ID = 5119685180



conn = sqlite3.connect('cloud.db', check_same_thread=False)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tg_id INTEGER UNIQUE
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    tg_id INTEGER UNIQUE,
    group_name TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
    name TEXT PRIMARY KEY,
    teacher_id INTEGER
)''')
conn.commit()

grading_data = {}
attendance_data = {}


def admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Guruh qo'shish", "👨‍🏫 O'qituvchi qo'shish")
    markup.add("🧑‍🎓 O'quvchi qo'shish", "📋 Guruhlar ro'yxati")
    return markup

def teacher_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("📝 Ball qo'yish", "📆 Davomat")
    markup.add("📋 Bosh menyu")
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    tg_id = message.from_user.id
    if tg_id == ADMIN_ID:
        bot.send_message(tg_id, "Assalomu alaykum, Admin!", reply_markup=admin_menu())
    else:
        cursor.execute("SELECT * FROM teachers WHERE tg_id = ?", (tg_id,))
        teacher = cursor.fetchone()
        if teacher:
            bot.send_message(tg_id, f"Xush kelibsiz, {teacher[1]}!", reply_markup=teacher_menu())
        else:
            bot.send_message(tg_id, "❌ Siz tizimga kiritilmagansiz.")

# --- ADMIN FUNKSIYALAR ---
@bot.message_handler(func=lambda m: m.text == "👨‍🏫 O'qituvchi qo'shish")
def add_teacher(message):
    bot.send_message(message.chat.id, "O'qituvchining ismini kiriting:")
    bot.register_next_step_handler(message, get_teacher_name)

def get_teacher_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Telegram ID sini kiriting:")
    bot.register_next_step_handler(message, lambda m: save_teacher(m, name))

def save_teacher(message, name):
    try:
        tg_id = int(message.text)
        cursor.execute("INSERT OR IGNORE INTO teachers (name, tg_id) VALUES (?, ?)", (name, tg_id))
        conn.commit()
        bot.send_message(message.chat.id, "✅ O'qituvchi qo‘shildi.")
    except:
        bot.send_message(message.chat.id, "❌ Xatolik yuz berdi.")

@bot.message_handler(func=lambda m: m.text == "➕ Guruh qo'shish")
def add_group(message):
    bot.send_message(message.chat.id, "Guruh nomini kiriting:")
    bot.register_next_step_handler(message, get_group_name)

def get_group_name(message):
    name = message.text
    bot.send_message(message.chat.id, "O'qituvchining Telegram ID sini kiriting:")
    bot.register_next_step_handler(message, lambda m: save_group(m, name))

def save_group(message, name):
    try:
        teacher_id = int(message.text)
        cursor.execute("SELECT * FROM teachers WHERE tg_id = ?", (teacher_id,))
        if cursor.fetchone():
            cursor.execute("INSERT INTO groups (name, teacher_id) VALUES (?, ?)", (name, teacher_id))
            conn.commit()
            bot.send_message(message.chat.id, "✅ Guruh qo‘shildi.")
        else:
            bot.send_message(message.chat.id, "❌ O'qituvchi topilmadi.")
    except:
        bot.send_message(message.chat.id, "❌ Xatolik yuz berdi.")

@bot.message_handler(func=lambda m: m.text == "🧑‍🎓 O'quvchi qo'shish")
def add_student(message):
    bot.send_message(message.chat.id, "O'quvchining ismini kiriting:")
    bot.register_next_step_handler(message, get_student_name)

def get_student_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Telegram ID sini kiriting:")
    bot.register_next_step_handler(message, lambda m: get_student_id(m, name))


def get_student_id(message, name):
    try:
        tg_id = int(message.text)
        bot.send_message(message.chat.id, "Guruh nomini kiriting:")
        bot.register_next_step_handler(message, lambda m: save_student(m, name, tg_id))
    except:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri ID.")

def save_student(message, name, tg_id):
    group = message.text
    cursor.execute("SELECT * FROM groups WHERE name = ?", (group,))
    if cursor.fetchone():
        cursor.execute("INSERT OR IGNORE INTO students (name, tg_id, group_name) VALUES (?, ?, ?)", (name, tg_id, group))
        conn.commit()
        bot.send_message(message.chat.id, "✅ O'quvchi qo‘shildi.")
    else:
        bot.send_message(message.chat.id, "❌ Guruh topilmadi.")

@bot.message_handler(func=lambda m: m.text == "📋 Guruhlar ro'yxati")
def show_groups(message):
    cursor.execute("SELECT name FROM groups")
    groups = cursor.fetchall()
    if groups:
        text = "\n".join([g[0] for g in groups])
        bot.send_message(message.chat.id, "📋 Guruhlar:\n" + text)
    else:
        bot.send_message(message.chat.id, "❌ Guruh yo‘q.")

# --- O'QITUVCHI: Ball qo'yish ---
@bot.message_handler(func=lambda m: m.text == "📝 Ball qo'yish")
def assign_grade(message):
    tg_id = message.from_user.id
    cursor.execute("SELECT name FROM groups WHERE teacher_id = ?", (tg_id,))
    groups = cursor.fetchall()
    if not groups:
        return bot.send_message(message.chat.id, "❌ Sizga guruh biriktirilmagan.")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for g in groups:
        markup.add(g[0])
    markup.add("📋 Bosh menyu")
    bot.send_message(message.chat.id, "📋 Guruhni tanlang:", reply_markup=markup)
    bot.register_next_step_handler(message, select_group_for_grading)

def select_group_for_grading(message):
    group = message.text
    if group == "📋 Bosh menyu":
        return bot.send_message(message.chat.id, "📋 Asosiy menyu", reply_markup=teacher_menu())
    cursor.execute("SELECT name, tg_id FROM students WHERE group_name = ?", (group,))
    students = cursor.fetchall()
    if not students:
        return bot.send_message(message.chat.id, "❌ Bu guruhda o‘quvchilar yo‘q.", reply_markup=teacher_menu())
    grading_data[message.chat.id] = {'group': group, 'students': {}, 'index': 0, 'list': students}
    ask_grading(message.chat.id)

def ask_grading(chat_id):
    data = grading_data[chat_id]
    if data['index'] >= len(data['list']):
        result = f"📝 Ballar: {data['group']}\n"
        for name, grade in data['students'].items():
            result += f"• {name}: {grade} ball\n"
        bot.send_message(chat_id, "✅ Ball qo‘yish yakunlandi.", reply_markup=teacher_menu())
        bot.send_message(ADMIN_ID, result)
        return
    student_name, student_id = data['list'][data['index']]
    markup = InlineKeyboardMarkup()
    for i in range(0, 11):
        markup.add(InlineKeyboardButton(f"{i}", callback_data=f"grade_{i}_{student_name}"))
    bot.send_message(chat_id, f"🧑 {student_name} uchun ball tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("grade_"))
def handle_grade(call):
    chat_id = call.message.chat.id
    data = grading_data.get(chat_id)
    if not data:
        return
    grade = int(call.data.split("_")[1])
    student_name = call.data.split("_")[2]
    data['students'][student_name] = grade
    data['index'] += 1
    ask_grading(chat_id)


@bot.message_handler(func=lambda m: m.text == "📆 Davomat")
def take_attendance(message):
    tg_id = message.from_user.id
    cursor.execute("SELECT name FROM groups WHERE teacher_id = ?", (tg_id,))
    groups = cursor.fetchall()
    if not groups:
        return bot.send_message(message.chat.id, "❌ Sizga guruh biriktirilmagan.")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for g in groups:
        markup.add(g[0])
    markup.add("📋 Bosh menyu")
    bot.send_message(message.chat.id, "📋 Guruhni tanlang:", reply_markup=markup)
    bot.register_next_step_handler(message, select_group_for_attendance)


def select_group_for_attendance(message):
    group = message.text
    if group == "📋 Bosh menyu":
        return bot.send_message(message.chat.id, "📋 Asosiy menyu", reply_markup=teacher_menu())
    cursor.execute("SELECT name, tg_id FROM students WHERE group_name = ?", (group,))
    students = cursor.fetchall()
    if not students:
        return bot.send_message(message.chat.id, "❌ Bu guruhda o‘quvchilar yo‘q.", reply_markup=teacher_menu())
    attendance_data[message.chat.id] = {'group': group, 'students': {}, 'index': 0, 'list': students}
    ask_attendance(message.chat.id)

def ask_attendance(chat_id):
    data = attendance_data[chat_id]
    if data['index'] >= len(data['list']):
        result = f"📆 Davomat: {data['group']}\n"
        for name, status in data['students'].items():
            result += f"• {name}: {status}\n"
        bot.send_message(chat_id, "✅ Davomat yakunlandi.", reply_markup=teacher_menu())
        bot.send_message(ADMIN_ID, result)
        return
    student_name, student_id = data['list'][data['index']]
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Keldi", callback_data="attended"),
               InlineKeyboardButton("❌ Kelmadi", callback_data="absent"))
    bot.send_message(chat_id, f"🧑 {student_name} holati:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["attended", "absent"])
def handle_attendance(call):
    chat_id = call.message.chat.id
    data = attendance_data.get(chat_id)
    if not data:
        return
    student_name, _ = data['list'][data['index']]
    data['students'][student_name] = "✅ Keldi" if call.data == "attended" else "❌ Kelmadi"
    data['index'] += 1
    ask_attendance(chat_id)
cursor.execute("""
DELETE FROM groups WHERE name = "👨‍🏫 O'qituvchi qo'shish";               
""")





def run_bot():
    bot.polling(none_stop=True)



