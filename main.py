import telebot
from configs import config
from internal import const, buttons, database, methods, task

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def send_wellcome(message):
    if database.Database().if_user_exists(message.chat.id):
        bot.send_message(
            chat_id = message.chat.id, 
            text = "Здравствуйте! Рад снова видеть вас!",
            reply_markup=buttons.start_button(),
            disable_notification = 'true'
        )
    else:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "{}{}{}".format(
                "**Здравствуйте! Добро пожаловать!**\nВыберите способ ввода часового пояса.\n",
                "**ВНИМАНИЕ**! Если вы используете Desktop версию Telegram, ",
                "то используйте ручной ввод!"
            ),
            parse_mode = "Markdown",
            reply_markup = buttons.input_tz(),
            disable_notification = 'true'
        )

@bot.callback_query_handler(lambda  call: call.data in {"use_gps", "input_timezone"})
def send_timezone(call):
    if call.data == "use_gps":
        bot.send_message(
            chat_id = call.message.chat.id, 
            text = "Местоположение:",
            reply_markup=buttons.send_geo(),
            disable_notification = 'true'
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, add_gps_location)
    elif call.data == "input_timezone":
        bot.send_message(
            chat_id = call.message.chat.id, 
            text = 'Введите ваш часовой пояс в ручную.\n**Пример: Москва - "+3", Иркутск - "+8"**',
            parse_mode = "Markdown",
            disable_notification = 'true'
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, add_location)
    else:
        bot.send_message(
            chat_id = call.message.chat.id, 
            text = 'Страшно! Вырубай!',
            parse_mode = "Markdown",
            disable_notification = 'true'
        )

def add_gps_location(message):
    if message.location:
        tz = methods.check_timezone_gps(message.location)
        loc_time = methods.loc_time(tz)
        loc_time = loc_time.strftime("%H:%M")
        bot.send_message(
            chat_id = message.chat.id,
            text = "Ваше время **{}**, верно?".format(loc_time),
            parse_mode = "Markdown",
            reply_markup = buttons.yes_or_not(),
            disable_notification = 'true'
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, timezone_validation, tz)
    else:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "**Часовой пояс по gps не получен! Попробуйте снова.",
            parse_mode = "Markdown",
            reply_markup = buttons.input_tz(),
            disable_notification = 'true'
        )

def add_location(message):
    tz = methods.check_timezone(message.text)
    loc_time = methods.loc_time(tz)
    loc_time = loc_time.strftime("%H:%M")
    if loc_time:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "Ваше время **{}**, верно?".format(loc_time),
            parse_mode = "Markdown",
            reply_markup = buttons.yes_or_not(),
            disable_notification = 'true'
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, timezone_validation, tz)
    else:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "{}\n{}".format(
                "**Часовой пояс введен не корректно! Попробуйте снова!**",
                'Пример: Москва - "+3", Иркутск - "+8"'
            ),
            parse_mode = "Markdown",
            disable_notification = 'true'
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, add_location)

def timezone_validation(message, tz):
    tz = methods.loc_time(tz)
    tz = str(tz.strftime("%Z"))
    if message.text == "Да":
        if database.Database().add_new_user(message.chat.id, tz):
            bot.send_message(
                chat_id = message.chat.id, 
                text = "**Регистрация прошла успешно!**",
                parse_mode = "Markdown",
                reply_markup = buttons.start_button(),
                disable_notification = 'true'
            )
        else:
            bot.send_message(
                chat_id = message.chat.id, 
                text = "**Ошибка регистрации! Введите /start, чтобы начать сначала!**",
                parse_mode = "Markdown",
                disable_notification = 'true'
            )
    else:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "**Попробуйте снова.**\nВыберите способ ввода часового пояса:",
            parse_mode = "Markdown",
            reply_markup = buttons.input_tz(),
            disable_notification = 'true'
        )

@bot.callback_query_handler(lambda  call: call.data == "delete_my_account")
def send_delete_account(call):
    bot.edit_message_text(
        text = "{}\n{}".format(
            "Если вы действительно хотите удалить свой аккаунт, введите, без ковычек:",
            '"Да, я действительно хочу удалить свой аккаунт!"\nОтменить /cancel.'
        ), 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
    )
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, delete_account)

def delete_account(message):
    if message.text == "Да, я действительно хочу удалить свой аккаунт!":
        database.Database().delete_user_account(message.chat.id)
        bot.send_message(
            chat_id = message.chat.id, 
            text = "**Аккаунт удален!**",
            parse_mode = "Markdown"
        )
    else:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "**Удаление аккаунта отменено!**",
            parse_mode = "Markdown",
            reply_markup = buttons.start_button()
        )

@bot.message_handler(commands=['help'])
def send_help(message):
    pass

@bot.message_handler(commands=['info'])
def send_info(message):
    pass

@bot.callback_query_handler(lambda  call: call.data == "newtask")
def send_newtask(call):
    bot.edit_message_text(
        text = "Выберите тип задачи:", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.type_task("send_newtask")
    )



@bot.callback_query_handler(lambda  call: call.data == "deletetask")
def send_delete_task(call):
    bot.edit_message_text(
        text = "Выберите тип удаляемой задачи:", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.type_task("send_delete_task")
    )

@bot.callback_query_handler(lambda  call: call.data == "mytasks")
def send_mytasks(call):
    bot.edit_message_text(
        text = "Выберите тип задачи:", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.type_task("send_mytasks")
    )

@bot.callback_query_handler(lambda  call: call.data == "groups")
def send_groups(call):
    bot.edit_message_text(
        text = "Выберите действие", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.groups()
    )

@bot.callback_query_handler(lambda  call: call.data == "cancel")
def cancel(call):
    bot.edit_message_text(
        text = "Действие отменено!", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.start_button()
    )

@bot.callback_query_handler(lambda  call: call.data in {
    'common_from_send_newtask'    , 'everyday_from_send_newtask'    , 'holiday_from_send_newtask',
    'common_from_send_delete_task', 'everyday_from_send_delete_task', 'holiday_from_send_delete_task',
    'common_from_send_mytasks'    , 'everyday_from_send_mytasks'    , 'holiday_from_send_mytasks'
})
def add_type_task(call):
    if call.data in {'common_from_send_newtask', 
                     'everyday_from_send_newtask', 
                     'holiday_from_send_newtask'}:
        tsk = task.Task()
        type_task = str(call.data).split("_")
        type_task = type_task[0]
        tsk.type_task = type_task
        bot.edit_message_text(
            text = "Введите суть задачи, о которой нужно напомнить.\n_Отменить_ - /cancel", 
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            parse_mode = "Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, add_text_task, tsk)

def add_text_task(message, tsk):
    tsk.text = message.text
    if tsk.type_task in ("common", "holiday"):
        bot.send_message(
            text = 'Введите дату в формате "ДД-ММ-ГГГГ".\n_Отменить_ - /cancel', 
            chat_id = message.chat.id,
            parse_mode = "Markdown"
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, add_date_task, tsk)
    elif tsk.type_task in "everyday":
        bot.send_message(
            text = "{}\n{}".format(
                'Введите номера дней недели, через запятую, в которые нужно вас оповещать.',
                '_Отменить_ - /cancel', 
            ),
            chat_id = message.chat.id,
            parse_mode = "Markdown"
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, add_weekday_task, tsk)

def add_date_task(message, tsk):
    date = message.text
    if methods.date_is_correct(date.split("-")):
        tsk.date = date
        bot.send_message(
            text = 'Введите время. В формате "ЧЧ:ММ"\n_Отменить_ - /cancel',
            chat_id = message.chat.id,
            parse_mode = "Markdown"
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, add_time_task, tsk)
    else:
        bot.send_message(
            text = "{}\n{}".format(
                '**Дата введена не верно!**.', 
                'Введите дату в формате "ДД-ММ-ГГГГ".\n_Отменить_ - /cancel'
            ),
            chat_id = message.chat.id,
            parse_mode = "Markdown"
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, add_date_task, tsk)

def add_weekday_task(message, tsk):
    weekday = message.text
    if methods.weekday_is_correct(weekday.split(",")):
        pass
    else:
        pass

def add_time_task(message, tsk):
    pass

def add_priority_task(message, tsk):
    pass

@bot.callback_query_handler(lambda  call: call.data == "back_to_start_buttons")
def send_start_buttons(call):
    bot.edit_message_text(
        text = "Выберите действие:", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.start_button()
    )

@bot.callback_query_handler(lambda  call: call.data == "menu")
def send_menu(call):
    bot.edit_message_text(
        text = "Выберите действие:", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.menu()
    )

@bot.callback_query_handler(lambda  call: call.data == "setting")
def send_setting(call):
    bot.edit_message_text(
        text = "Выберите действие:", 
        chat_id = call.message.chat.id,
        message_id = call.message.message_id,
        reply_markup = buttons.setting()
    )

@bot.message_handler(func=lambda m: True)
def error_message(message):
    if database.Database().if_user_exists(message.chat.id):
        bot.send_message(
            chat_id = message.chat.id, 
            text = "Я не понимаю этой команды!", 
            reply_markup = buttons.start_button(),
            disable_notification = 'true'
        )
    else:
        bot.send_message(
            chat_id = message.chat.id, 
            text = "**Ваш аккаунт не зарегистрирован!",
            parse_mode = "Markdown",
            disable_notification = 'true'
        )
        bot.send_message(
            chat_id = message.chat.id, 
            text = "**Для регистрации выберите способ ввода часового пояса:",
            parse_mode = "Markdown",
            reply_markup = buttons.input_tz(),
            disable_notification = 'true'
        )


if __name__ == "__main__":
    bot.polling(none_stop = True)
