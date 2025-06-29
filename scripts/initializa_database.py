# scripts/initialize_database.py

import sqlite3
import pandas as pd
import os

# --- Configurações ---
DATABASE_FILE = os.path.join('database', 'nutri.db')
TACO_TABLE_FILE = os.path.join('data', 'taco_table.csv')
FOODS_TABLE_NAME = 'foods'
PATIENTS_TABLE_NAME = 'patients'
CONSULTATIONS_TABLE_NAME = 'consultations'

def create_tables(conn):
    """Cria as tabelas no banco de dados se não existirem."""
    cursor = conn.cursor()
    
    # Tabela de alimentos (da TACO)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {FOODS_TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        energy_kcal REAL,
        protein_g REAL,
        carbohydrate_g REAL,
        lipid_g REAL
    );
    """)

    # Tabela de pacientes
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {PATIENTS_TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birth_date TEXT,
        contact TEXT,
        medical_history TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Tabela de consultas/avaliações
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {CONSULTATIONS_TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        consultation_date TEXT NOT NULL,
        weight_kg REAL,
        height_cm REAL,
        body_fat_percentage REAL,
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES {PATIENTS_TABLE_NAME} (id)
    );
    """)
    
    conn.commit()
    print("Tabelas criadas com sucesso (se não existiam).")

def populate_foods_from_taco(conn):
    """Lê a tabela TACO e popula o banco de dados."""
    if not os.path.exists(TACO_TABLE_FILE):
        print(f"ERRO: Arquivo '{TACO_TABLE_FILE}' não encontrado. Pulei a população da tabela de alimentos.")
        return

    cursor = conn.cursor()
    # Verifica se a tabela já tem dados para não duplicar
    cursor.execute(f"SELECT COUNT(*) FROM {FOODS_TABLE_NAME}")
    if cursor.fetchone()[0] > 0:
        print("Tabela de alimentos já está populada. Pulei a inserção.")
        return

    # Adapte os nomes das colunas conforme o seu arquivo CSV da TACO
    df_taco = pd.read_csv(TACO_TABLE_FILE)
    df_to_insert = df_taco[['description', 'energy_kcal', 'protein_g', 'carbohydrate_g', 'lipid_g']].copy()
    
    df_to_insert.to_sql(FOODS_TABLE_NAME, conn, if_exists='append', index=False)
    print(f"Tabela '{FOODS_TABLE_NAME}' populada com {len(df_to_insert)} registros.")


if __name__ == '__main__':
    # Garante que o diretório do banco de dados exista
    os.makedirs('database', exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_FILE)
    try:
        create_tables(conn)
        populate_foods_from_taco(conn)
    finally:
        conn.close()
    
    print("Inicialização do banco de dados concluída.")