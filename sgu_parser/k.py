import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('teachers.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

url = "https://www.sgu.ru/schedule/teacher"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

teachers_list = soup.find('ul', id='search-results').find_all('li')

print(f"Найдено преподавателей: {len(teachers_list)}")

for teacher in teachers_list:
    teacher_id = teacher.get('data-id')
    teacher_name = teacher.text.strip()
    
    cursor.execute(
        "INSERT OR IGNORE INTO teachers (id, name) VALUES (?, ?)", 
        (teacher_id, teacher_name)
    )

conn.commit()
conn.close()

print("База данных teachers.db успешно создана!")