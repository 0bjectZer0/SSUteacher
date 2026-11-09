from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    teacher_name = ""
    error = ""

    if request.method == 'POST':
        search_name = request.form.get('name', '').strip()
        teacher_name = search_name

        conn = sqlite3.connect('teachers.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM teachers WHERE name LIKE ?", ('%' + search_name + '%',))
        teachers = cursor.fetchall()
        conn.close()

        if not teachers:
            error = "Преподаватель не найден. Попробуйте другую фамилию."
        else:
            teacher_id, teacher_full_name = teachers[0]
            teacher_name = teacher_full_name

            url = f"https://www.sgu.ru/schedule/teacher/{teacher_id}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')

            pattern = r'(\d{2}:\d{2})\s*(\d{2}:\d{2}).*?(\d+)\s*корпус,\s*(\d+)\s*комната'

            for row in rows:
                text = row.get_text(separator=' ', strip=True)
                matches = re.findall(pattern, text)
                for match in matches:
                    results.append({
                        'time': f"{match[0]} - {match[1]}",
                        'corpus': match[2],
                        'room': match[3]
                    })

    return render_template('index.html', results=results, teacher_name=teacher_name, error=error)

if __name__ == '__main__':
    app.run(debug=True)