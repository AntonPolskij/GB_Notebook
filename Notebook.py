import uuid
import datetime

from pathlib import Path

MAIN_DIR = Path(__file__).parent


def open_note_book(file_name: str) -> list:
    note_book = []
    with open(MAIN_DIR / 'notes.csv', 'r', encoding='utf-8') as file:
        for line in file:
            temp = tuple(line.strip().split(';'))
            note_book.append(temp)
    return note_book


def menu(data: list):
    while (True):
        print("*" * 10)
        print("Выберите действие")
        print("1: - Создать новую запись")
        print("2: - Просмотреть все заметки")
        print("0: - Для выхода")
        print("*" * 10)
        get = input("Введите действие: ")
        if get == '0':
            print()
            print('До свидания')
            return False
        elif get == '1':
            # Добавляет запись.
            data = create(data, get_data())
        elif get == '2':
            if len(data) == 0:
                print("Список заметок пуст!")
                continue
            for elem in data:
                print(f'{elem}')
            select_note_ui(data)


def create(data: list, elem: tuple) -> list:
    data.append(elem)
    write_file(data)
    return data


def get_data() -> tuple:
    note_id = uuid.uuid1()
    header = input("Введите заголовок заметки: ")
    body = input("Введите текст заметки: ")
    date = datetime.datetime.now()
    print("*" * 10)
    print(f"Заметка создана: {header},{body},{date}")
    return f'{note_id}', header, body, f'{date.strftime("%Y-%m-%d %H:%M:%S")}'


def write_file(note_book: list):
    with open(MAIN_DIR / 'notes.csv', 'w', encoding='utf-8') as file:
        for element in note_book:
            template = f'{element[0]};{element[1]};{element[2]};{element[3]}\n'
            file.write(template)


def select_note_ui(data: list):
    print("*" * 10)
    print(
        "Для выбора конкретной заметки из списка, скопируйте в консоль её uiid('прим: cb4e613b-dc4f-11ed-937e-346f2485a1ca')")
    print("Для возврата в главное меню нажмите: Enter")
    get = input("Введите действие: ")
    if get == '':
        return
    else:
        note = find_note(get, data)
        print(note)
        if type(note) == tuple:
            print('Удалить запись: 1')
            print('Изменить данные: 2')
            print('Возврат: Enter')
            input_value = input()
            if input_value == '1':
                delete_note(data, note)


def find_note(note_uuid: str, notes_list: list):
    note_uuid = note_uuid.lower().strip("'")
    for el in notes_list:
        if el[0] == note_uuid:
            return el
    return f'Заметка с таким UUID не найдена'


def delete_note(note_book: list, note):
    note_book.remove(note)


menu(open_note_book('notes.csv'))
