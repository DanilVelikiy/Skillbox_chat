from datetime import datetime
from flask import Flask, request, render_template
import json

app = Flask(__name__)

#messages_list = [
#    {
#        "text": "Всем приветы в этом чате",
#        "sender": "Василий",
#        "date": "31.01.2022 21:00",
#    },
#    {
#        "text": " йо йо",
#        "sender": "Мишаня",
#        "date": "31.01.2022 22:00",
#    },
#]

# messages_list = []

db_file = "./data/db.json" # путь к файлу
json_db = open(db_file, "rb") # открываем файл
data = json.load(json_db) # загружаем данные из файла
messages_list = data["message_list"]

# Функция сохранения сообщений в файл
def save_messages():
    # создам структуру
    data = {
        "message_list": messages_list,
    }

    # открываем файл на запись
    json_db = open(db_file, "w")
    json.dump(data, json_db) #


def print_message(message):
    print(f"[{message['sender']}] - {message['text']} / {message['date']}")
    print("-" * 60)


# функиця добавления нового сообщения
def add_message(name, txt):
    message = {
        "text": txt,
        "sender": name,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }
    messages_list.append(message)


#add_message("Сергей", "Расскажите про глобальные и локальные переменные")
#add_message("Ксения", "А что и как и когда")


# for m in messages_list:
#    print_message(m)

# print_message(chat_message_1)
# print_message(chat_message_2)

# главная страница
@app.route("/")
def index_page():
    return "Hello! Welcome to The SkillBox Chat"

# рааздел со списком сообщений
@app.route("/get_messages")
def get_messages():
    return {"messages": messages_list}

# раздел для отправки сообщения
@app.route("/send_message")
def send_message():
    # как получить данные из браузера ?
    name = request.args["name"]
    # валидация имени по длине и вывод соответствуещего сообщения
    if (len(name) < 3)or(len(name) > 100):
        name = "Error Name"
        text = "Имя должно быть от 3 до 100 символов"
        add_message(name, text)
        save_messages()
        return "Error"
    text = request.args["text"]

    # валидация текста по длине и вывод соответствуещего сообщения
    if (len(text) < 1)or(len(text)>3000):
        text = "Error. Текст должен быть от 1 до 3000 символов"
        add_message(name, text)
        save_messages()
        return "Error"
    add_message(name, text)
    save_messages()
    return "ok"

# раздел с визуальным интерфейсом
@app.route("/form")
def form():
    return render_template("form.html")

app.run()
