import discord
from discord.ext import commands
from discord import File
import requests
from random import randint, choice


# создание файла с картинкой
def image_map():
    global longitude, lattitude, layer, zoom
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{lattitude}&size=650,450&z={zoom}&l=" \
                  f"{layer + traffic_mode}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


# проверка того, что строка является числом
def isfloat(str_):
    h = True
    for i in str_:
        if i not in '0123456789-.' or str_.count('.') > 1 or str_.count('-') > 1:
            h = False
    return h


# добавление координат в текстовый файл
def write(request):  #
    with open("search history.txt", mode="a", encoding='UTF-8') as file:
        file.write(request + '\n')


PREFIX = '-'
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')
layer = 'map'
longitude = 47.25
lattitude = 56.1
zoom = 11
traffic_mode = ''
# считывание информации с текстового файла и добавление её в словарь со странами
with open("countries.txt", mode="r", encoding='UTF-8') as file:
    open_file = file.readlines()
    COUNTRIES = {open_file[0]: 'Аргентина', open_file[1]: 'Австралия', open_file[2]: 'Бельгия', open_file[3]: 'Канада',
                open_file[4]: 'Китай', open_file[5]: 'Египет', open_file[6]: 'Великобритания', open_file[7]:
                'Финляндия', open_file[8]: 'Франция', open_file[9]: 'Германия', open_file[10]: 'Греция',
                open_file[11]: 'Индия', open_file[12]: 'Испания', open_file[13]: 'Италия', open_file[14]: 'Казахстан',
                open_file[15]: 'Мексика', open_file[16]: 'Монголия', open_file[17]: 'Польша', open_file[18]:
                'Португалия', open_file[19]: 'Россия', open_file[20]: 'Швеция', open_file[21]:
                'Турция', open_file[22]: 'США'}
RIGHT_ANSWERS_WORDS = ['Правильно!', 'Так держать!', 'Молодец!', 'Отлично!', 'Всё верно!']
WRONG_ANSWERS_WORDS = ['К сожаленью, это неправильно', 'Увы, это не так', 'Вы не правы!', 'Вы ошибаетесь',
                       'Неверно!']


# изменение статуса бота, когда он появляется в сети
@bot.event
async def on_ready():
    print("Bot was connected to the server")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('планета Земля'))


# отправка картинки местоположения
@bot.command(name='place')
async def Place(ctx, *args):
    global longitude, lattitude, traffic_mode
    Isfloat = False
    Coords = False
    traffic_mode = ''
    if len(args) == 2 and isfloat(args[0]) and isfloat(args[1]):
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
            write(f"Долгота {longitude}, широта {lattitude}")
    elif not Isfloat:
        await ctx.send('Введите долготу и широту')
    elif not Coords:
        await ctx.send('Координаты должны быть рациональными числами. '
                       'Долгота должна быть в диапозоне от -180 до 180, а широта - от -85 до 85')


# изменение слоя
@bot.command(name='layer')
async def Layer(ctx, *change_layer):
    global layer
    list_layers = {'map': 'Схема', 'sat': 'Спутник', 'sat,skl': 'Гибрид'}
    if len(change_layer) == 1:
        try:
            await ctx.send(f'Слой был изменён с {list_layers[layer]} на {list_layers[change_layer[0]]}')
            layer = change_layer[0]
        except Exception:
            await ctx.send(f'Введите название слоя (map - схема; sat - спутник; sat,skl - гибрид)')
    else:
        await ctx.send(f'Введите название слоя (map - схема; sat - спутник; sat,skl - гибрид)')


# отображение пробок
@bot.command(name='traffic')
async def Traffic(ctx, *args):
    global layer, traffic_mode
    if layer == 'sat,skl':
        layer = 'sat'
    traffic_mode = ',trf,skl'
    if not args:
        image_map()
        await ctx.send(file=File('map.png'))
    else:
        await ctx.send('Кроме команды ничего писать не нужно')


# демонстрация всех функций бота
@bot.command(name='help')
async def Help(ctx, *args):
    if not args:
        embed = discord.Embed(title='Команды', description="Здесь вы можете узнать команды и их описания")
        commands_list = ["help", 'clear', "place", "layer", "traffic", "place_history", "game", "find", "zoom"]
        descriptions_for_commands = ["Список команд", 'Очистка последних сообщений (по умолчанию - 10)',
                                     "Ваше местоположение (по умолчанию - последнее)",
                                     "Изменение слоя (map - схема; sat - спутник; sat,skl - гибрид)",
                                     "Пробки по последним координатам", "История введённых координат",
                                     "Географическая игра", "Поиск мест", "Изменение масштаба "
                                                                          "(натуральное число до 23)"]
        for command_name, description_command in zip(commands_list, descriptions_for_commands):
            embed.add_field(name=f'-{command_name}', value=description_command, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Кроме команды ничего писать не нужно')


# чистка сообщений
@bot.command(name="clear")
async def clear(ctx, *number):
    if number:
        if len(number) == 1 and number[0].isdigit():
            await ctx.channel.purge(limit=int(number[0]))
            await ctx.send(f"```Было удалено {number[0]} сообщений```")
        else:
            await ctx.send('Введите одно число - количество удаляемых сообщений')
    else:
        await ctx.channel.purge(limit=10)
        await ctx.send(f"```Было удалено 10 сообщений```")


# история запросов place
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
        with open("search history.txt", mode="r", encoding='UTF-8') as file:
            open_file = file.readlines()
            await ctx.send('```Ваша история координат:```')
            if number <= len(open_file):
                for i in range(len(open_file) - 1, len(open_file) - number - 1, -1):
                    await ctx.send(f"{i + 1}. {open_file[i]}")
            else:
                for i in range(len(open_file) - 1, 0, -1):
                    await ctx.send(f"{i + 1}. {open_file[i]}")
    except Exception:
        await ctx.send('Ваша история пуста')


# игра Страны
@bot.command(name="game")
async def Game(ctx, *args):
    global right_answer, answer
    if args:
        await ctx.send('Кроме команды ничего писать не нужно')
        return
    await ctx.send(f"```Игра «Страны»```")
    await ctx.send(f"``Правила игры:``\n"
                    f"По изображению контура и флага страны вы должны "
                    f"угадать её и написать название (очевидно, с заглавной буквы) в чат (без префиксов)\n"
                    f"Чтобы закночить игру напишите «Стоп»\n"
                    f"*Вам даётся право на 3 ошибки*")
    await ctx.send("**Начнём?**")
    answer = await bot.wait_for("message")
    answer = answer.content
    number_countries = [i for i in range(23)]
    if answer.lower() == 'да' or answer.lower() == 'конечно' or answer.lower() == 'погнали':
        await ctx.send("Отлично!")
        mistake_count = 3
        name_mistake_count = {1: 'а жизнь', 2: 'и жизни', 3: 'и жизни'}
        while answer.lower() != 'стоп' and answer.lower() != 'хватит' and len(number_countries) > 0 and \
                mistake_count > 0:
            choosing = number_countries.pop(randint(0, len(number_countries) - 1))
            await ctx.send('Следующая страна:')
            await ctx.send(list(COUNTRIES.keys())[choosing])
            answer = await bot.wait_for("message")
            answer = answer.content
            right_answer = COUNTRIES[list(COUNTRIES.keys())[choosing]]
            if answer == right_answer:
                await ctx.send(choice(RIGHT_ANSWERS_WORDS))
            elif answer.lower() == 'стоп' or answer.lower() == 'хватит' or len(number_countries) == 0:
                break
            else:
                mistake_count -= 1
                if mistake_count == 0:
                    break
                await ctx.send(f"{choice(WRONG_ANSWERS_WORDS)}.\nУ вас остал"
                                f"{name_mistake_count[mistake_count].split()[0]}сь {mistake_count}"
                                f" {name_mistake_count[mistake_count].split()[1]}")
                await ctx.send(f'Правильный ответ - {right_answer}')
                await ctx.send('Следующая страна:')
        if mistake_count == 3:
            await ctx.send('Наше почтение, вы не совершили ни одной ошибки!')
            await ctx.send('https://i.ytimg.com/vi/WseshSyT4p8/maxresdefault.jpg')
        elif mistake_count == 0:
            await ctx.send(f"Вы проиграли и набрали баллов - {23 - len(number_countries) - (3 - mistake_count)}")
        await ctx.send("Спасибо за игру")
    else:
        await ctx.send("Жаль(")


# поиск адреса и его отображение
@bot.command(name='find')
async def Find(ctx, *args):
    global longitude, lattitude, layer, traffic_mode, zoom
    traffic_mode = ''
    find_place = ' '.join(list(args))
    try:
        find_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=" \
                       f"json&geocode={find_place}&results=1"
        coords = requests.get(find_request).json()["response"]["GeoObjectCollection"]["featureMember"] \
            [0]["GeoObject"]["Point"]['pos'].split()
        longitude = coords[0]
        lattitude = coords[1]
        kind = requests.get(find_request).json()["response"]["GeoObjectCollection"]["featureMember"][0] \
                  ["GeoObject"]['metaDataProperty']['GeocoderMetaData']['kind']
        if kind == 'house':
            zoom = 18
        elif kind == 'street':
            zoom = 16
        elif kind == 'hydro':
            zoom = 6
        else:
            zoom = 11
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{lattitude}&size=650,450&z={zoom}&l=" \
                      f"{layer + traffic_mode}&pt={longitude},{lattitude},ya_ru"
        response = requests.get(map_request)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        await ctx.send(f'{find_place} здесь:')
        await ctx.send(file=File('map.png'))
        write(f"Долгота и широта [{find_place}]: {longitude}, {lattitude}")
    except Exception:
        await ctx.send('Увы, по вашему запросу ничего не было найдено')


# изменение масштаба
@bot.command(name='zoom')
async def Zoom(ctx, *change_zoom):
    global zoom
    try:
        await ctx.send(f'Масштаб был изменён с {zoom} на {change_zoom[0]}')
        zoom = int(change_zoom[0])
    except Exception:
        await ctx.send(f'Введите натуральное число до 23 - новый масштаб ')


bot.run('TOKEN')