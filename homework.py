import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        today_date = dt.datetime.today().date()
        today_stats = 0
        for record in self.records:
            if record.date == today_date:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        today = dt.datetime.today().date()
        stats = 0
        for record in self.records:
            if record.date > (today - dt.timedelta(days=7)):
                stats += record.amount
        return stats


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        self.comment = comment

    def __str__(self):
        return f"Количество: {self.amount} || Дата: {self.date} || Комментарий: {self.comment}"


class CashCalculator(Calculator):
    USD_RATE = 77
    EURO_RATE = 90

    def get_today_cash_remained(self, currency):
        self.currency = currency
        leftover = self.get_today_stats()

        if currency == "rub":
            self.currency = "руб"
        elif currency == "usd":
            leftover /= USD_RATE
            self.currency = "USD"
        elif currency == "euro":
            leftover /= EURO_RATE
            self.currency = "Euro"
        else:
            raise ValueError

        if leftover < self.limit:
            leftover = self.limit - leftover
            balance = f"На сегодня осталось {leftover} {self.currency}"
        if leftover == self.limit:
            balance = "Денег нет, держись"
        if leftover > self.limit:
            credit = leftover - self.limit
            balance = f"Денег нет, держись: твой долг - {credit} {self.currency}"
        
        return balance



class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        leftover = self.get_today_stats()

        if leftover < self.limit:
            leftover = self.limit - leftover
            return ("Сегодня можно съесть что-нибудь ещё, но с общей"
                    f"калорийностью не более {leftover} кКал")
        else:
            return "Хватит есть!"
