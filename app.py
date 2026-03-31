import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 🔹 Database init
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

# 🏠 Home route
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    # 📊 Stats
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

# ➕ Add task
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

# ❌ Delete task
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# ✏️ Edit task
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

# 📅 ✅ ADD THIS HERE (Calendar Route)
@app.route('/calendar')
def calendar():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()

    return render_template('calendar.html', tasks=tasks)

# 🚀 Run app
if __name__ == '__main__':
    app.run(debug=True)