import random
import telebot
from telebot import types


bot = telebot.TeleBot('token')


list_j = [
    "Мой друг, счастье не откладывай ни на час. Счастье надо пить свежим. А неприятность может и подождать. Р.Роллан",
    "Настроение, как у Карлсона: хочу сладкого и пошалить.",
    "Тепло тому, кто излучает свет. Светло тому, кто носит в себе солнце.",
    "Заболел хорошим настроением… Больничный брать не буду! Пускай люди заражаются…",
    "Чтобы жить и радоваться, нужно всего две вещи: во-первых ― жить, во-вторых ― радоваться…"
]

list_s = [
    "Никогда не говори: «Я ошибся», лучше скажи: «Надо же, как интересно получилось! «Ледниковый период»",
    "Случайности не случайны. «Кунг-фу панда»",
    "Тебе плохо? Ты знаешь, просто скажи «акуна-матата». И всё, никаких проблем! «Король лев»",
    "Вчера больной, сегодня больной… Не надоело? «Маша и медведь.»",
    "Повод для грусти всегда найдётся. Нужно уметь радоваться."
]

list_m = [
    "Жизнь измеряется не числом вдохов-выдохов, а моментами, когда захватывает дух! Д.Карлин",
    "Важно не то, сбили ли тебя с ног, — важно то, поднялся ли ты снова. В.Ломбарди",
    "Не ошибается тот, кто ничего не делает! Не бойтесь ошибаться – бойтесь повторять ошибки! Т.Рузвельт",
    "Путь в тысячу ли начинается с одного единственного маленького шага. Лао Цзы",
    "У всех у нас есть страхи. Но у тех, кто смотрит им в лицо, есть ещё и мужество. Э.Хемингуэй"
]


# Получаем сообщения и обрабатываем их
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Если написали «Привет» или /start
    if message.text.lower() == "привет" or message.text.lower() == "/start":
        # Пишем приветствие ввиде смайлика
        bot.send_message(message.from_user.id, "\U0001F44B")
        # Спрашиваем имя и переходим к get_name
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)

    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def get_name(message):  # получаем имя
    global name
    name = message.text
    # Пишем приветствие с именем
    bot.send_message(message.from_user.id, 'Привет, ' + name + '!')
    bot.send_message(message.from_user.id, 'Меня зовут Маруся, вот моё фото')
    # Добавляем фото (выбирается случайным методом)
    bot.send_photo(message.chat.id, open('photoes/' + str(random.randint(1, 6)) + '.jpg', 'rb'))

    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст для кнопки и обработчик для каждой
    key_joy = types.InlineKeyboardButton(text='\U0001F604 Радостно', callback_data='citation_joy')
    # И добавляем кнопку на экран
    keyboard.add(key_joy)
    key_sad = types.InlineKeyboardButton(text='\U0001F614 Грустно', callback_data='citation_sad')
    keyboard.add(key_sad)
    key_motivation = types.InlineKeyboardButton(text='\U0001F680 Нужна мотивация', callback_data='citation_motivation')
    keyboard.add(key_motivation)

    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.from_user.id, text=name + ', выбери какое у тебя настроение', reply_markup=keyboard)


# Обрабатываем значения кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 3 кнопок — выводим цитату
    if call.data == "citation_joy":
        # Формируем случайным методом цитату
        msg_joy = random.choice(list_j)
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg_joy)

    elif call.data == "citation_sad":
        msg_sad = random.choice(list_s)
        bot.send_message(call.message.chat.id, msg_sad)

    elif call.data == "citation_motivation":
        msg_motivation = random.choice(list_m)
        bot.send_message(call.message.chat.id, msg_motivation)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
