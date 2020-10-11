import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_date = dt.date.today()
        today_stats = [r.amount for r in self.records if r.date == today_date]
        today_stats = sum(today_stats)
        return today_stats

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        stats = 0
        for record in self.records:
            if week_ago < record.date <= today:
                stats += record.amount
        return stats

    def get_leftover(self):
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        self.comment = comment

    def __str__(self):
        return (f"Количество: {self.amount} || Дата: {self.date} "
                f"|| Комментарий: {self.comment}")


class CashCalculator(Calculator):
    USD_RATE = 77
    EURO_RATE = 90

    def get_today_cash_remained(self, currency):
        currencies = {
            "rub": (1, "руб"),
            "usd": (self.USD_RATE, "USD"),
            "eur": (self.EURO_RATE, "Euro")
        }
        leftover = self.get_leftover()

        if leftover == 0:
            return "Денег нет, держись"
        if currency not in currencies:
            return "Валюта не поддерживается"
        if currency in currencies:
            leftover = round(leftover/currencies[currency][0], 2)

        if leftover < 0:
            credit = abs(leftover)
            return (f"Денег нет, держись: твой долг - {credit} "
                    f"{currencies[currency][1]}")
        return f"На сегодня осталось {leftover} {currencies[currency][1]}"



class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        leftover = self.get_today_stats()

        if leftover < self.limit:
            leftover = self.get_leftover()
            return ("Сегодня можно съесть что-нибудь ещё, но с общей"
                    f" калорийностью не более {leftover} кКал")
        else:
            return "Хватит есть!"


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
                
print(cash_calculator.get_today_cash_remained("rub"))