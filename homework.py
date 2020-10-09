import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        today_date = dt.date.today()
        today_stats = 0
        for record in self.records:
            if record.date == today_date:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        stats = 0
        for record in self.records:
            if week_ago < record.date <= today:
                stats += record.amount
        return stats


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        self.comment = comment

    def __str__(self):
        return f"Количество: {self.amount} || Дата: {self.date} || Комментарий: {self.comment}"


class CashCalculator(Calculator):
    USD_RATE = 77.0
    EURO_RATE = 90.0

    def get_today_cash_remained(self, currency):
        spent = self.get_today_stats()
        leftover = self.limit - self.get_today_stats()
        if currency == "rub":
            currency = "руб"
        elif currency == "usd":
            currency = "USD"
            leftover = round(leftover/self.USD_RATE, 2)
        elif currency == "eur":
            currency = "Euro"
            leftover = round(leftover/self.EURO_RATE, 2)
        else:
            raise ValueError

        if spent < self.limit:
            balance = f"На сегодня осталось {leftover} {currency}"
        if spent == self.limit:
            balance = "Денег нет, держись"
        if spent > self.limit:
            credit = leftover * (-1)
            balance = f"Денег нет, держись: твой долг - {credit} {currency}"
        
        return balance



class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        leftover = self.get_today_stats()

        if leftover < self.limit:
            leftover = self.limit - leftover
            return ("Сегодня можно съесть что-нибудь ещё, но с общей"
                    f" калорийностью не более {leftover} кКал")
        else:
            return "Хватит есть!"
