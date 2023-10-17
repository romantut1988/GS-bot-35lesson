import discord
import requests
import random

client = discord.Client()

# token = "MTE2Mzc3NTE5NjAxNzIxNzU0Ng.G9OnTu.vUpagzRq5pF6x1E4rX7f5nOg5WGx209sbFMc2c"

GIF_KEY = "Eo4g0uN9HE0CtvcoXGqlARNW0og9ZZ4S"


async def get_gifs(search: str):
    params = {
        'api_key': GIF_KEY,
        'q': search,
        'limit': 5,
        'rating': 'g',
        'lang': 'ru'
    }
    response = requests.get(f"https://api.giphy.com/v1/gifs/search", params=params)
    j_data = response.json().get('data')
    result = []
    for gif in j_data:
        result.append(gif["url"])
    return result


@client.event
async def on_ready():
    print(f'Залогинился под именем {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:  # Чтобы не реагировать на сообщения бота
        return  # Ничего не делаем

    if message.content == 'ping':
        await message.channel.send('pong')

    if message.content.startswith('$Привет'):
        await message.channel.send('Привет, друг!')

    if message.content.startswith('!gif '):
        req = message.content[4:]
        gifs = await get_gifs(req)
        await message.channel.send(random.choice(gifs))

    if message.content == '!hello':
        await message.channel.send(f'Приветствую тебя, {message.author.name}!')

    if message.content == '!help':
        await message.channel.send('Я знаю команды...')

    if check_caps(message.content):
        reason = 'Злоупотребление CAPS LOCK'
        # await message.channel.purge(limit=1)  # Удаляем последнее сообщение
        await message.author.send(f'Вы были выгнаны по причине: {reason}')
        # await message.author.ban(reason='reason')  # Баним пользователя
        emb = make_ban_embed(message.author, reason)  # Получаем рамку
        await message.channel.send(embed=emb)  # Выводим на экран рамку


def check_caps(text):  # Функция определения CAPS LOCK
    if len(text) < 6:  # Если длина текста меньше 6 символов
        return False  # то ничего не делаем.
    count = 0  # Счетчик количества больших букв
    for i in text:  # Цикл перебора букв в сообщении
        if i.isupper():  # Если найдена большая буква
            count += 1  # Увеличиваем счетчик на 1
    return count > len(text) // 4 * 3  # Если букв больше, чем 75% текста


def make_ban_embed(author, reason):
    emb = discord.Embed(title='Нарушение правил чата', colour=discord.Color.red())
    emb.set_author(name=author.name, icon_url=author.avatar_url)
    emb.add_field(name='Бан пользователя', value=f'Пользователь {author.mention} был забанен')
    emb.set_footer(text=f'Причина бана: {reason}')
    return emb


client.run(token)
