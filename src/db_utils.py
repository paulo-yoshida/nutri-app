import sqlite3
import os

DATABASE_FILE = os.path.join('database', 'nutri.db')

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_FILE)
    # Retorna as linhas como dicionários para fácil acesso por nome de coluna
    conn.row_factory = sqlite3.Row
    return conn

def get_patient_list():
    """Busca uma lista de todos os pacientes (id e nome)."""
    conn = get_db_connection()
    patients = conn.execute("SELECT id, name FROM patients ORDER BY name ASC").fetchall()
    conn.close()
    return patients

def add_patient(name, birth_date, contact, medical_history):
    """Adiciona um novo paciente ao banco de dados."""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO patients (name, birth_date, contact, medical_history) VALUES (?, ?, ?, ?)",
        (name, birth_date, contact, medical_history)
    )
    conn.commit()
    conn.close()

def get_patient_details(patient_id):
    """Busca todos os detalhes de um paciente específico pelo seu ID."""
    conn = get_db_connection()
    patient = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return patient

def update_patient(patient_id, name, birth_date, contact, medical_history):
    """Atualiza as informações de um paciente existente."""
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE patients
        SET name = ?, birth_date = ?, contact = ?, medical_history = ?
        WHERE id = ?
        """,
        (name, birth_date, contact, medical_history, patient_id)
    )
    conn.commit()
    conn.close()

def delete_patient(patient_id):
    """Exclui um paciente do banco de dados."""
    conn = get_db_connection()
    # Futuramente, considere também excluir consultas associadas
    conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()