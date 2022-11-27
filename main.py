from aiogram import executor, types
from database import get_from_database, add_to_database
from parsers import get_latest_news, start_updating
import threading


def add_commands(commands: list) -> None:
    for command in commands:
        pass
        #dp.register_message_handler(command[0], commands=command[1])


async def add_team(message: types.Message):
    try:
        text = message.text
        username, team = message.chat['username'], ' '.join(text.split()[1:])
    except IndexError:
        await message.answer(f'Неверный формат. Попробуйте\n/set <название_команды>')
        return
    add_to_database(username, team)
    await message.answer(f'Пользователю {username} успешно '
                         f'была присвоена команда {team}.')


async def get_team(message: types.Message):
    username = message.chat['username']
    data = get_from_database()
    if username in data.keys():
        await message.answer(f'Для пользователя {username} '
                             f'зарегистрирована команда {data[username]}')
    else:
        await message.answer(f'Для пользователя {username} не '
                             f'зарегистрирована команда. Это можно сделать '
                             f'с помощью команды /set <название_команды>')


def main():
    commands = [
        (add_team, ['set']),
        (get_team, ['get']),
        (send_news, ['news'])
    ]
    add_commands(commands)
    executor.start_polling(dp, skip_updates=True)


async def send_news(message: types.Message):
    data = get_from_database()
    user = message.chat['username']
    if user in data.keys():
        team = data[user]
    else:
        await message.answer(f'Для пользователя {user} не '
                             f'зарегистрирована команда. Это можно сделать '
                             f'с помощью команды /set <название_команды>')
        return

    text = message.text.split()
    if len(text) == 1:
        title, href = get_latest_news(team)
    else:
        title, href = get_latest_news(team)
    await message.answer(f'{title}[.]({href})', parse_mode='Markdown')


if __name__ == "__main__":
    exit('Это устаревший файл. Сейчас запуск всего происходит из файта bot.py')
    thr1 = threading.Thread(target=start_updating).start()
    main()
