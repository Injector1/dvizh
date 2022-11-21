def get_from_database() -> dict:
    with open('./database/users.txt', 'r') as file:
        file_data = file.readline()[1:-1].split(', ')
        if len(file_data[0]) == 0:
            return dict()
        return dict([(s.split(': ')[0][1:-1], s.split(': ')[1][1:-1]) for s in file_data])


def add_to_database(user_id: str, team: str) -> None:
    items = get_from_database()
    with open('./database/users.txt', 'w+') as file:
        items[user_id] = team
        file.write(str(items))
