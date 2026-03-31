import sqlite3
from flask import Flask, render_template, request, redirect
from datetime import datetime   # 🔥 important

app = Flask(__name__)

# 🗄️ Create DB
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            date TEXT,
            time TEXT,
            priority TEXT,
            status TEXT,
            progress INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🏠 HOME (Dashboard + Auto Complete)
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    # 🔥 AUTO UPDATE STATUS BASED ON TIME
    for task in tasks:
        task_id = task[0]
        task_date = task[2]
        task_time = task[3]

        try:
            task_datetime = datetime.strptime(task_date + " " + task_time, "%Y-%m-%d %H:%M")

            if datetime.now() > task_datetime:
                cur.execute(
                    "UPDATE tasks SET status='Completed', progress=100 WHERE id=?",
                    (task_id,)
                )
        except:
            pass

    conn.commit()

    # reload updated tasks
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    # 📊 Dashboard stats
    total = len(tasks)
    completed = len([t for t in tasks if t[5] == 'Completed'])
    pending = len([t for t in tasks if t[5] == 'Pending'])
    progress = len([t for t in tasks if t[5] == 'In Progress'])

    conn.close()

    return render_template(
        'index.html',
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        progress=progress
    )

# ➕ ADD TASK
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        date = request.form['date']
        time = request.form['time']
        priority = request.form['priority']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO tasks (task_name, date, time, priority, status, progress)
            VALUES (?, ?, ?, ?, 'Pending', 0)
        """, (task_name, date, time, priority))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_task.html')

# ✏️ EDIT TASK
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        task_name = request.form['task_name']
        date = request.form['date']
        time = request.form['time']
        priority = request.form['priority']
        status = request.form['status']
        progress = request.form['progress']

        cur.execute("""
            UPDATE tasks
            SET task_name=?, date=?, time=?, priority=?, status=?, progress=?
            WHERE id=?
        """, (task_name, date, time, priority, status, progress, id))

        conn.commit()
        conn.close()
        return redirect('/')

    cur.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cur.fetchone()
    conn.close()

    return render_template('edit_task.html', task=task)

# ❌ DELETE TASK
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# 📅 CALENDAR
@app.route('/calendar')
def calendar():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    conn.close()
    return render_template('calendar.html', tasks=tasks)

# ▶️ RUN
if __name__ == '__main__':
    app.run(debug=True)
