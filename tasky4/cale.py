from datetime import date, timedelta
print(date.today() - timedelta(days=5))

from datetime import date, timedelta
today = date.today()
print(today - timedelta(1))
print(today)
print(today + timedelta(1))

from datetime import datetime
print(datetime.now().replace(microsecond=0))


from datetime import datetime
d1 = datetime(2024, 5, 1, 12, 0, 0)
d2 = datetime(2024, 5, 1, 12, 0, 5)
print((d2 - d1).total_seconds())
