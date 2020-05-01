import datetime as dt


def today():
    return dt.datetime.today().date()


class Calculator:

    def __init__(self, limit: float):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def _get_stats(self, min_datetime, max_datetime):
        periods_amount = 0
        for record in self.records:
            if min_datetime <= record.date <= max_datetime:
                periods_amount += record.amount
        return periods_amount

    def get_today_stats(self):
        return self._get_stats(today(), today())

    def get_week_stats(self):
        return self._get_stats(today() - dt.timedelta(days=7), today())

    def get_today_remained(self):
        return self.limit - self.get_today_stats()


class Record:

    def __init__(self, amount: float, comment: str, date=dt.datetime.now()):
        self.amount = amount
        if isinstance(date, str):
            date_format = '%d.%m.%Y'
            try:
                date = dt.datetime.strptime(date, date_format).date()
            except ValueError:
                raise ValueError(f'Wrong date format. Expected {date_format}. Provided: {date}.')
        elif isinstance(date, dt.datetime):
            date = date.date()
        self.date = date
        self.comment = comment


class CashCalculator(Calculator):
    USD_RATE = 60.
    EURO_RATE = 70.

    currency_dict = {
        'usd': 'USD',
        'eur': 'Euro',
        'rub': 'руб'
    }

    def conversion_rate(self, to_currency: str):
        rate = 1
        if to_currency == 'usd':
            rate = self.USD_RATE
        elif to_currency == 'eur':
            rate = self.EURO_RATE
        elif to_currency != 'rub':
            raise ValueError(f'Unexpected currency name: {to_currency}')
        return rate

    def get_today_cash_remained(self, currency):
        remained_default_currency = super().get_today_remained()
        remained = remained_default_currency / self.conversion_rate(currency)
        if remained > 0:
            res = f'На сегодня осталось {round(remained, 2)} {self.currency_dict[currency]}'
        elif remained == 0:
            res = 'Денег нет, держись'
        else:
            res = f'Денег нет, держись: твой долг - {abs(round(remained, 2))} {self.currency_dict[currency]}'
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
