from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html",students = students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
            (name, age, course, email)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template("add_student.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        email = request.form['email']

        conn.execute(
            "UPDATE students SET name=?, age=?, course=?, email=? WHERE id=?",
            (name, age, course, email, id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    conn.close()
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('home'))



if __name__ == "__main__":
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    app.run(debug=True)