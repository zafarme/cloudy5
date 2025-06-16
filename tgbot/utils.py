from django.conf import settings
import telebot


bot = telebot.TeleBot(settings.BOT_TOKEN)

def send_message_to_user(tg_id, message):
    try:
        bot.send_message(tg_id, message)
    except Exception as e:
        print(f"Хабар юборишда хатолик: {e}")

def notify_group_creation(group):
    for student in group.student_set.all():
        send_message_to_user(student.tg_id, f"{group.name} гуруҳига қўшилдингиз.")

teacher = Teacher.objects.get(id=1)


send_message_to_user(teacher.tg_id, "Иванов номли ўқувчи дарсга келмади.")