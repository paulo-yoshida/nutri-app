import pandas as pd
import os

def preprocess_taco_table(input_path, output_path):
    """
    Lê uma planilha da Tabela TACO, remove linhas em branco e cabeçalhos repetidos,
    e salva o resultado como um arquivo CSV.

    Args:
        input_path (str): O caminho para o arquivo .xlsx de entrada.
        output_path (str): O caminho para salvar o arquivo .csv de saída.
    """
    print(f"Iniciando o pré-processamento do arquivo: {input_path}")

    try:
        # A Tabela TACO geralmente possui algumas linhas de título antes dos dados.
        # O valor de 'skiprows' pode precisar de ajuste dependendo da sua planilha.
        # Ex: skiprows=3 pula as 3 primeiras linhas.
        df = pd.read_excel(input_path, skiprows=1)
        print(f"Arquivo lido com sucesso. Shape inicial: {df.shape}")

    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada não foi encontrado em '{input_path}'")
        print("Por favor, certifique-se de que o arquivo XLSX da Tabela TACO está na pasta 'data'.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo Excel: {e}")
        return

    # --- Início da Limpeza ---

    # 1. Remover linhas completamente em branco
    df_cleaned = df.dropna(how='all')
    print(f"Shape após remover linhas em branco: {df_cleaned.shape}")

    # 2. Remover linhas não numéricas na primeira coluna (que geralmente são cabeçalhos repetidos)
    if not df_cleaned.empty:
        first_col_name = df_cleaned.columns[0]
        initial_rows = len(df_cleaned)

        # Mantém apenas as linhas onde o valor na primeira coluna pode ser convertido para número
        is_numeric = pd.to_numeric(df_cleaned[first_col_name], errors='coerce').notna()
        df_cleaned = df_cleaned[is_numeric]

        rows_removed = initial_rows - len(df_cleaned)
        print(f"{rows_removed} linhas não numéricas (cabeçalhos) foram removidas da primeira coluna.")
        print(f"Shape final: {df_cleaned.shape}")

    # --- Fim da Limpeza ---

    # Salvar o DataFrame limpo em um arquivo CSV com codificação UTF-8
    try:
        df_cleaned.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Arquivo pré-processado salvo com sucesso em: {output_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo CSV: {e}")


if __name__ == "__main__":
    # Define a pasta de dados
    DATA_DIR = "data"
    # Adapte o nome do arquivo de entrada para o nome da sua planilha
    INPUT_FILENAME = "Taco-4a-Edicao.xlsx"
    OUTPUT_FILENAME = "taco.csv"

    # Garante que o diretório de dados exista
    os.makedirs(DATA_DIR, exist_ok=True)

    preprocess_taco_table(os.path.join(DATA_DIR, INPUT_FILENAME), os.path.join(DATA_DIR, OUTPUT_FILENAME))