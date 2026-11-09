import requests
from bs4 import BeautifulSoup
import re
import sqlite3

search_name = input("Введите фамилию преподавателя: ").strip()

conn = sqlite3.connect('teachers.db')
cursor = conn.cursor()

cursor.execute("SELECT id, name FROM teachers WHERE name LIKE ?", ('%' + search_name + '%',))
results = cursor.fetchall()
conn.close()

if not results:
    print("Преподаватель не найден. Попробуйте другую фамилию.")
    exit()

if len(results) > 1:
    print("\nНайдено несколько преподавателей:")
    for i, (tid, name) in enumerate(results):
        print(f"{i + 1}. {name} (ID: {tid})")
    
    choice = input("\nВведите номер нужного преподавателя: ").strip()
    try:
        index = int(choice) - 1
        teacher_id, teacher_name = results[index]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        exit()
else:
    teacher_id, teacher_name = results[0]

print(f"\nИщем расписание для: {teacher_name}")

url = f"https://www.sgu.ru/schedule/teacher/{teacher_id}"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find_all('tr')

pattern = r'(\d{2}:\d{2})\s*(\d{2}:\d{2}).*?(\d+)\s*корпус,\s*(\d+)\s*комната'

print("\nРасписание (время + аудитория)")
found_any = False

for row in rows:
    text = row.get_text(separator=' ', strip=True)
    matches = re.findall(pattern, text)
    
    for match in matches:
        time_start = match[0]
        time_end = match[1]
        corpus = match[2]
        room = match[3]
        print(f"Время: {time_start} - {time_end} Корпус: {corpus}, Аудитория: {room}")
        found_any = True

if not found_any:
    print("Аудитории не найдены. Возможно, у преподавателя нет пар в расписании.")