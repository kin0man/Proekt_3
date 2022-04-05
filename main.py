from discord.ext import commands
from discord import File
import requests


def isfloat(str_):
    h = True
    for i in str_:
        if i not in '0123456789.' or str_.count('.') > 1:
            h = False
    return h


bot = commands.Bot(command_prefix='-')


@bot.command(name='place')
async def timer(ctx, *args):
    longitude = 47.25
    lattitude = 56.1
    if isfloat(args[0]) and isfloat(args[1]):
        if len(args) > 1 and -180 <= int(args[0]) <= 180 and -85 <= int(args[1]) <= 85:
            longitude = int(args[0])
            lattitude = int(args[1])
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{lattitude}&size=650,450&z=11&l=map"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    await ctx.send('Вы здесь:')
    await ctx.send(file=File('map.png'))


bot.run('ЗДЕСЬ БУДЕТ ТОКЕН ИЗ ВК')