class Task:
    def __init__(self, type_task='', text='', date='', time='', priority='', weekday='', timezone=''):
        self.type_task = type_task
        self.text = text
        self.date = date
        self.time = time
        self.priority = priority
        self.weekday = weekday
        self.timezone = timezone
    def getTask(self):
        if self.type_task == "Повседневная":
            temp = "{}{}{}{}{}{}{}{}{}{}{}".format(
                "📜 <b>Задача: </b>", self.text, "\n",
                "⌛️ <b>Время: </b>", str(self.time), "\n",
                "🗓 <b>Дни недели: </b>", str(self.weekday), "\n",
                "🔥 <b>Приоритет: </b>", self.priority
            )
            return temp
        else:
            dt = str(self.date)
            dt = dt.split("-")
            self.date = "{}-{}-{}".format(dt[2],dt[1],dt[0])
            temp = "{}{}{}{}{}{}{}{}{}{}{}".format(
                "📜 <b>Задача: </b>", self.text, "\n",
                "📅 <b>Дата: </b>", self.date, "\n",
                "⌛️ <b>Время: </b>", str(self.time), "\n",
                "🔥 <b>Приоритет: </b>", self.priority
            )
            return temp