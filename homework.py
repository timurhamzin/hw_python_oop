import datetime as dt


def today():
    return dt.datetime.today().date()


class Calculator:

    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def _get_stats(self, start_date, end_date):
        return sum([record.amount for record in self.records if start_date <= record.date <= end_date])

    def get_today_stats(self):
        return self._get_stats(today(), today())

    def get_week_stats(self):
        return self._get_stats(today() - dt.timedelta(days=7), today())

    def get_today_remained(self):
        return self.limit - self.get_today_stats()


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount: float, comment: str, date=None):
        if not date:
            date = dt.datetime.now()
        self.amount = amount
        if isinstance(date, str):
            try:
                date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
            except ValueError:
                raise ValueError(f'Wrong date format. Expected {self.DATE_FORMAT}. Provided: {date}.')
        elif isinstance(date, dt.datetime):
            date = date.date()
        self.date = date
        self.comment = comment


class CashCalculator(Calculator):
    USD_RATE = 60.
    EURO_RATE = 70.

    CURRENCIES = {
            'usd': (USD_RATE, 'USD'),
            'eur': (EURO_RATE, 'Euro'),
            'rub': (1, 'руб')
        }

    def conversion_rate(self, to_currency: str):
        return self.CURRENCIES[to_currency][0]

    def get_today_cash_remained(self, currency):
        remained_default_currency = super().get_today_remained()
        remained = remained_default_currency / self.conversion_rate(currency)
        currency_display_name = self.CURRENCIES[currency][1]
        if remained == 0:
            res = 'Денег нет, держись'
        elif remained > 0:
            remained_rounded = round(remained, 2)
            res = f'На сегодня осталось {remained_rounded} {currency_display_name}'
        else:
            debt = abs(round(remained, 2))
            res = f'Денег нет, держись: твой долг - {debt} {currency_display_name}'
        return res


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remained = super().get_today_remained()
        if remained > 0:
            res = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал'
        else:
            res = 'Хватит есть!'
        return res


if __name__ == '__main__':
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)
    # cash_calculator = CaloriesCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="29.04.2020"))

    print(cash_calculator.get_today_cash_remained("eur"))
    # должно напечататься
    # На сегодня осталось 555 руб

    # print(cash_calculator.get_week_stats())

    # print(cash_calculator.get_today_stats())
    # print(cash_calculator.get_today_remained())
    # print(cash_calculator.get_calories_remained())
    # print(cash_calculator.get_week_stats())
