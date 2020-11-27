from telebot import types

def start_button():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text='📖 Mеню', callback_data='menu')
    button2 = types.InlineKeyboardButton(text='⚙️ Настройки', callback_data='setting')
    markup.add(button1, button2)
    return markup

def menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='📝 Новая задача', callback_data='newtask')
    button2 = types.InlineKeyboardButton(text='🗑 Удалить задачу', callback_data='deletetask')
    button3 = types.InlineKeyboardButton(text='🧾 Задачи на сегодня', callback_data='today')
    button4 = types.InlineKeyboardButton(text='📜 Личные задачи', callback_data='mytasks')
    button5 = types.InlineKeyboardButton(text='📆 Групповые задачи', callback_data='mygrouptasks')
    button6 = types.InlineKeyboardButton(text='🥳 Группы', callback_data='groups')
    button7 = types.InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_start_buttons')
    markup.row(button1, button2)
    markup.add(button3, button4, button5)
    markup.row(button6, button7)
    return markup

def setting():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='🕑 Часовой пояс', callback_data='change_tz')
    button2 = types.InlineKeyboardButton(text='🕑 Формат времени', callback_data='change_format_time')
    button3 = types.InlineKeyboardButton(text='🕑 Язык', callback_data='change_lang')
    button4 = types.InlineKeyboardButton(text='‼️ Удалить аккаунт', callback_data='delete_my_account')
    button5 = types.InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_start_buttons')
    markup.row(button1, button3)
    markup.add(button2, button4, button5)
    return markup

def type_task(namefunc):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(
        text='Обычная', 
        callback_data='common_from_{}'.format(namefunc)
    )
    button2 = types.InlineKeyboardButton(
        text='Повседневная', 
        callback_data='everyday_from_{}'.format(namefunc)
    )
    button3 = types.InlineKeyboardButton(
        text='Праздничная', 
        callback_data='holiday_from_{}'.format(namefunc)
    )
    button4 = types.InlineKeyboardButton(text='Отменить', callback_data='cancel')
    markup.add(button1, button2, button3, button4)
    return markup

def groups():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Мои группы', callback_data='mygroups')
    button2 = types.InlineKeyboardButton(text='Создать группу', callback_data='create_group')
    button3 = types.InlineKeyboardButton(text='Удалить группу', callback_data='delete_group')
    button4 = types.InlineKeyboardButton(text='🔙 Назад', callback_data='menu')
    markup.add(button1, button2, button3, button4)
    return markup

def input_tz():
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Ввести в ручную', callback_data='input_timezone')
    button2 = types.InlineKeyboardButton(text='Использовать GPS', callback_data='use_gps')
    markup.add(button1, button2)
    return markup

def send_geo():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton(text="Отправить своё местоположение", request_location = True)
    markup.add(button1)
    return markup

def priority_task():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton(text="Важно и срочно")
    button2 = types.KeyboardButton(text="Важно, но неcрочно")
    button3 = types.KeyboardButton(text="Не важно, но срочно")
    button4 = types.KeyboardButton(text="Не важно и несрочно")
    markup.add(button1, button2, button3, button4)
    return markup

def yes_or_not():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton(text='Да')
    button2 = types.KeyboardButton(text='Нет')
    markup.add(button1, button2)
    return markup