# scripts/initialize_database.py

import sqlite3
import pandas as pd
import os

# --- Configurações ---
DATABASE_FILE = os.path.join('database', 'nutri.db')
TACO_TABLE_FILE = os.path.join('data', 'taco.csv')
FOODS_TABLE_NAME = 'foods'
PATIENTS_TABLE_NAME = 'patients'
CONSULTATIONS_TABLE_NAME = 'consultations'

def create_tables(conn):
    """Cria as tabelas no banco de dados se não existirem."""
    cursor = conn.cursor()
    
    # Tabela de alimentos (da TACO)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {FOODS_TABLE_NAME} (
        food_id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        moisture_percent REAL,
        energy_kcal REAL,
        protein_g REAL,
        lipid_g REAL,
        cholesterol_mg REAL,
        carbohydrate_g REAL,
        dietary_fiber_g REAL,
        ash_g REAL,
        calcium_mg REAL,
        magnesium_mg REAL,
        manganese_mg REAL,
        phosphorus_mg REAL,
        iron_mg REAL,
        sodium_mg REAL,
        potassium_mg REAL,
        copper_mg REAL,
        zinc_mg REAL,
        retinol_mcg REAL,
        retinol_equivalent_mcg REAL,
        retinol_activity_equivalent_mcg REAL,
        thiamin_mg REAL,
        riboflavin_mg REAL,
        pyridoxine_mg REAL,
        niacin_mg REAL,
        vitamin_c_mg REAL
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
        -- Dobras Cutâneas (mm)
        skinfold_triceps_mm REAL,
        skinfold_subscapular_mm REAL,
        skinfold_biceps_mm REAL,
        skinfold_chest_mm REAL,
        skinfold_midaxillary_mm REAL,
        skinfold_suprailiac_mm REAL,
        skinfold_abdominal_mm REAL,
        skinfold_thigh_mm REAL,
        skinfold_medial_calf_mm REAL,
        -- Circunferências (cm)
        circ_arm_cm REAL,
        circ_waist_cm REAL,
        circ_abdominal_cm REAL,
        circ_hip_cm REAL,
        circ_thigh_cm REAL,
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
    # Dicionário completo para renomear as colunas do CSV
    column_mapping = {
        'Número do Alimento': 'food_id',
        'Descrição dos alimentos': 'description',
        'Umidade': 'moisture_percent',
        'Energia': 'energy_kcal',
        'Proteína': 'protein_g',
        'Lipídeos': 'lipid_g',
        'Colesterol': 'cholesterol_mg',
        'Carboidrato': 'carbohydrate_g',
        'Fibra alimentar': 'dietary_fiber_g',
        'Cinzas': 'ash_g',
        'Cálcio': 'calcium_mg',
        'Magnésio': 'magnesium_mg',
        'Manganês': 'manganese_mg',
        'Fósforo': 'phosphorus_mg',
        'Ferro': 'iron_mg',
        'Sódio': 'sodium_mg',
        'Potássio': 'potassium_mg',
        'Cobre': 'copper_mg',
        'Zinco': 'zinc_mg',
        'Retinol': 'retinol_mcg',
        'RE': 'retinol_equivalent_mcg',
        'RAE': 'retinol_equivalent_mcg',
        'Tiamina': 'thiamin_mg',
        'Riboflavina': 'riboflavin_mg',
        'Piridoxina': 'pyridoxine_mg',
        'Niacina': 'niacin_mg',
        'Vitamina C': 'vitamin_c_mg'
    }
    
    # Renomeia as colunas do DataFrame para o padrão do banco de dados
    df_taco.rename(columns=column_mapping, inplace=True)
    
    df_to_insert = df_taco.copy()
    
    df_to_insert.to_sql(FOODS_TABLE_NAME, conn, if_exists='replace', index=False)
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