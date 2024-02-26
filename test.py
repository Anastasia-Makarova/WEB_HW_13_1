from datetime import date, timedelta, datetime

start = datetime.now()
seven_days_later = start+ timedelta(days=7)


day = datetime(year= 1978, month=2, day=22)

bday_this_year = datetime(year=start.year, month=day.month, day=day.day)

print(bday_this_year)

if bday_this_year >= start and bday_this_year <= seven_days_later:
    print('in range')
else:
    print('not in range')