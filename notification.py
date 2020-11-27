import requests 
import shelve
from configs import config 
from internal import methods, buttons, database, const

url = "https://api.telegram.org/bot{0}/sendMessage".format(config.TOKEN)

# def message_user(message_text, chat_id):
#     """Функция для отправки сообщения пользователю"""
#     message_data = {
#     'chat_id': chat_id,
#     'text': message_text,
#     'parse_mode': 'HTML'
#     }
#     requests.post(url, data=message_data)
# def send_message(user_id, task, loc_time):
#     """Функция создания сообщения"""
#     if database.Database().get_past_notification(user_id, task.id_task):
#         message = task.getTask()
#         message = "⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️⚜️\n{}\n🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰🔰".format(message)
#         message_user(message, user_id)
#         database.Database().add_past_notification(user_id, task.id_task, loc_time)
#         if task.type_task == "Праздничная":
#             database.Database().update_date(user_id, task.id_task)
#         return 0


# def main():
#     while True:
#         tables = database.Database().alert_tables()
#         if(len(tables)):
#             for user_id in tables:
#                 timezone = database.Database().get_timezone(user_id)
#                 loc_date = methods.now_date(timezone)
#                 loc_time = methods.now_local_time(timezone)
#                 database.Database().delete_past_notification(loc_time)
#                 database.Database().delete_past_basic_task(user_id, loc_date)
#                 now_tasks = database.Database().get_now_rows(user_id, loc_date, loc_time)
#                 now_evetyday_task = database.Database().get_everyday_rows(user_id, loc_time)
#                 if len(now_tasks):
#                     for task in now_tasks:
#                         send_message(user_id, task, loc_time)
#                 if len(now_evetyday_task):
#                     for task in now_evetyday_task:
#                         send_message(user_id, task, loc_time)

def main():
    # notif = shelve.open("past_notification")
    # notif["111"] = "10:00"
    # for i in notif.values():
    #     print(i, end="\n")
    mx = 0
    for i in const.priorities:
        mx = max(len(i), mx)

    print(mx)
     
    

if __name__=="__main__":
    main()