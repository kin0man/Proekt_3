import discord
from discord.ext import commands
from discord import File
import requests


def image_map():
    global longitude, lattitude, layer
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{lattitude}&size=650,450&z=11&l={layer + traffic_mode}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def isfloat(str_):
    h = True
    for i in str_:
        if i not in '0123456789-.' or str_.count('.') > 1 or str_.count('-') > 1:
            h = False
    return h


def write(request):
    with open("search history.txt", mode="a") as file:
        file.write(request + '\n')


PREFIX = '-'
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')
layer = 'map'
longitude = 47.25
lattitude = 56.1
traffic_mode = ''
with open('token.txt', mode='r') as file:
    TOKEN = file.readlines()[0]


@bot.event
async def on_ready():
    print("Bot was connected to the server")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('планета Земля'))


@bot.command(name='place')
async def Place(ctx, *args):
    global longitude, lattitude, layer, traffic_mode
    Isfloat = False
    Coords = False
    traffic_mode = ''
    if len(args) == 2  and isfloat(args[0]) and isfloat(args[1]):
        Isfloat = True
        if -180 <= float(args[0]) <= 180 and -85 <= float(args[1]) <= 85:
            longitude = float(args[0])
            lattitude = float(args[1])
            Coords = True
    elif not args:
        Isfloat = True
        Coords = True
    if Isfloat and Coords:
        await ctx.send('Вы здесь:')
        image_map()
        await ctx.send(file=File('map.png'))
        if args:
            write(f"-place {args[0]} {args[1]}")
    elif not Isfloat:
        await ctx.send('Введите долготу и широту')
    elif not Coords:
        await ctx.send('Долгота должна быть в диапозоне от -180 до 180, а широта - от -85 до 85')


@bot.command(name='layer')
async def Layer(ctx, *change_layer):
    global layer
    list_layers = {'map': 'Схема', 'sat': 'Спутник', 'sat,skl': 'Гибрид'}
    if len(change_layer) == 1:
        try:
            await ctx.send(f'Слой был изменён с {list_layers[layer]} на {list_layers[change_layer[0]]}')
            layer = change_layer
        except Exception:
            await ctx.send(f'Введите название слоя (map - схема; sat - спутник; sat,skl - гибрид)')
    else:
        await ctx.send(f'Введите название слоя (map - схема; sat - спутник; sat,skl - гибрид)')


@bot.command(name='traffic')
async def Traffic(ctx, *args):
    global longitude, lattitude, layer, traffic_mode
    if layer == 'sat,skl':
        layer = 'sat'
    traffic_mode = ',trf,skl'
    if not args:
        image_map()
        await ctx.send(file=File('map.png'))
    else:
        await ctx.send('Кроме команды ничего писать не нужно')


@bot.command(name='help')
async def Help(ctx, *args):
    if not args:
        embed = discord.Embed(title='Команды', description="Здесь вы можете узнать команды и их описания")
        commands_list = ["help", 'clear', "place", "layer", "traffic", "place_history"]
        descriptions_for_commands = ["Список команд", 'Очистка последних сообщений (по умолчанию - 10)',
                                     "Ваше местоположение (по умолчанию - последнее)",
                                     "Изменение слоя (map - схема; sat - спутник; sat,skl - гибрид)",
                                     "Пробки по последним координатам", "История введённых координат"]
        for command_name, description_command in zip(commands_list, descriptions_for_commands):
            embed.add_field(name=f'-{command_name}', value=description_command, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Кроме команды ничего писать не нужно')


@bot.command(name="clear")
async def clear(ctx, *number):
    if number:
        if len(number) == 1 and number[0].isdigit():
            await ctx.channel.purge(limit=int(number[0]))
            await ctx.send(f"Было удалено {number[0]} сообщений")
        else:
            await ctx.send('Введите одно число - количество удаляемых сообщений')
    else:
        await ctx.channel.purge(limit=10)
        await ctx.send(f"Было удалено 10 сообщений")


@bot.command(name="place_history")
async def Place_history(ctx, *number):
    if number:
        if len(number) == 1 and number[0].isdigit():
            number = int(number[0])
        else:
            await ctx.send('Введите одно число - количество последних запросов координат')
            return
    else:
        number = 10
    try:
        with open("search history.txt", mode="r") as file:
            open_file = file.readlines()
            if number <= len(open_file):
                for i in range(number):
                    await ctx.send(f"{i + 1}. {open_file[i]}")
            else:
                for i in range(len(open_file)):
                    await ctx.send(f"{i + 1}. {open_file[i]}")
    except Exception:
        await ctx.send('Ваша история пуста')


@bot.command(name="game")
async def Game(ctx, *args):
    if args:
        await ctx.send('Кроме команды ничего писать не нужно')
        return
    try:
        await ctx.send(f"```Игра Страны```")
        await ctx.send(f"Правила игры:\n")
        await ctx.send(f"По изображению контура и флага страны вы должны угадать её"
                       f"и написать название в чат (без префиксов)\n"
                       f"*Вам даётся право на 3 ошибки*")
        await ctx.send(f"**Начнём?**")
    except Exception:
        await ctx.send('Ваша история пуста')


bot.run(TOKEN)