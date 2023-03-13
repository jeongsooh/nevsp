from datetime import datetime, date, timedelta

today = datetime.now()
systemday = today.date()
startday = datetime.combine(date.today(),datetime.min.time()) -timedelta(days=1)

print('today: ', today, type(today))
print('systemday: ', systemday, type(systemday))
print('date.today(): ', date.today())
print('datetime.min.time(): ', datetime.min.time())
print('startday: ', startday, type(startday))
