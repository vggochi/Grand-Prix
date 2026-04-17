import sqlite3

def create_db():
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id TEXT PRIMARY KEY,
        nome TEXT,
        setor TEXT,
        nascimento TEXT,
        iris_code TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_employee(id, nome, setor, nascimento, iris_code):
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO funcionarios VALUES (?, ?, ?, ?, ?)",
                   (id, nome, setor, nascimento, iris_code))
    conn.commit()
    conn.close()

def delete_employee(id):
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funcionarios WHERE id=?", (id,))
    conn.commit()
    conn.close()

def get_employee_by_iris(iris_code):
    conn = sqlite3.connect("funcionarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM funcionarios WHERE iris_code=?", (iris_code,))
    result = cursor.fetchone()
    conn.close()
    return result
