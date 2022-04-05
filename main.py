from discord.ext import commands
from discord import File
import requests


bot = commands.Bot(command_prefix='-')


@bot.command(name='place')
async def timer(ctx, *args):
    longitude = 47.25
    lattitude = 56.1
    if len(args) > 1:
        longitude = args[0]
        lattitude = args[1]
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{lattitude}&size=650,450&z=11&l=map"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    await ctx.send('Вы здесь:')
    await ctx.send(file=File('map.png'))


bot.run('ЗДЕСЬ БУДЕТ ТОКЕН ИЗ ВК')