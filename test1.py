import discord
from datetime import date

today = date.today()
month_day_year = today.strftime("%m/%d/%y").split("/")
for (i,v) in enumerate(month_day_year):
    month_day_year[i] = int(v)
print(month_day_year)