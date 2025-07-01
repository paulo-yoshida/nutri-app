import streamlit as st
import pandas as pd
from datetime import datetime
from src import db_utils  # Importa nossas funções do banco de dados

st.set_page_config(page_title="Gestão de Pacientes", page_icon="👥")

st.title("👥 Gestão de Pacientes")

# --- LÓGICA PARA BUSCAR A LISTA DE PACIENTES ---
patient_list = db_utils.get_patient_list()
# Cria um dicionário para mapear nome para id, e vice-versa
patient_map = {patient['name']: patient['id'] for _, patient in patient_list.iterrows()}
patient_names = ["Cadastrar Novo Paciente"] + list(patient_map.keys())

# --- MENU DE SELEÇÃO ---
selected_patient_name = st.selectbox("Selecione um Paciente ou Cadastre um Novo", options=patient_names)

# --- LÓGICA DE EXIBIÇÃO ---

if selected_patient_name == "Cadastrar Novo Paciente":
    st.subheader("Formulário de Cadastro")
    with st.form("new_patient_form", clear_on_submit=True):
        name = st.text_input("Nome Completo", key="new_name")
        birth_date = st.date_input("Data de Nascimento", min_value=datetime(1920, 1, 1), key="new_bdate", format="DD/MM/YYYY")
        sex = st.selectbox("Sexo", options=["Masculino", "Feminino"], key="new_sex")
        contact = st.text_input("Contato (Telefone/Email)", key="new_contact")
        medical_history = st.text_area("Histórico Clínico (patologias, alergias, objetivos...)", key="new_history")
        
        submitted = st.form_submit_button("Salvar Paciente")
        if submitted:
            if name:  # Validação simples para garantir que o nome não está vazio
                db_utils.add_patient(name, birth_date.strftime("%Y-%m-%d"), sex.lower(), contact, medical_history)
                st.success(f"Paciente '{name}' cadastrado com sucesso!")
                st.rerun() # Recarrega a página para atualizar a lista
            else:
                st.error("O nome do paciente é obrigatório.")

else: # Se um paciente existente foi selecionado
    patient_id = patient_map[selected_patient_name]
    patient_details = db_utils.get_patient_details(patient_id).iloc[0] # Pega a primeira (e única) linha do DataFrame

    # Formulário de Edição de Dados Cadastrais
    with st.expander("📝 Editar Dados Cadastrais", expanded=False):
        if not patient_details.empty:
            with st.form("edit_patient_form"):
                birth_date_obj = datetime.strptime(patient_details['birth_date'], '%Y-%m-%d').date()
                name = st.text_input("Nome Completo", value=patient_details['name'])
                birth_date = st.date_input("Data de Nascimento", value=birth_date_obj)
                sex = st.selectbox("Sexo", options=["Masculino", "Feminino"], index=0 if patient_details['sex'] == 'masculino' else 1)
                contact = st.text_input("Contato (Telefone/Email)", value=patient_details['contact'])
                medical_history = st.text_area("Histórico Clínico", value=patient_details['medical_history'], height=150)

                col1, col2 = st.columns([1, 1])
                with col1:
                    update_button = st.form_submit_button("✅ Atualizar Informações")
                with col2:
                    delete_button = st.form_submit_button("❌ Excluir Paciente")

                if update_button:
                    db_utils.update_patient(patient_id, name, birth_date.strftime("%Y-%m-%d"), sex.lower(), contact, medical_history)
                    st.success(f"Informações de '{name}' atualizadas com sucesso!")
                    st.rerun()

                if delete_button:
                    st.session_state.confirm_delete_patient = True # Usando chave específica
    
    # --- NOVO: Lógica de confirmação da exclusão do PACIENTE ---
    if st.session_state.get('confirm_delete_patient'):
        st.warning(f"**Atenção:** Você tem certeza que deseja excluir **{selected_patient_name}** e todas as suas consultas? Esta ação não pode ser desfeita.")
        col1_conf, col2_conf = st.columns(2)
        if col1_conf.button("Sim, excluir PACIENTE", type="primary"):
            db_utils.delete_patient(patient_id) # Futuramente, expandir para deletar consultas em cascata
            st.success(f"Paciente '{selected_patient_name}' foi excluído.")
            del st.session_state.confirm_delete_patient
            st.rerun()
        if col2_conf.button("Não, cancelar exclusão"):
            del st.session_state.confirm_delete_patient
            st.rerun()

    st.divider() # --- NOVO ---

    # --- NOVO: Seção de Acompanhamento de Consultas ---
    st.header("📈 Consultas e Acompanhamento")

    # Formulário para adicionar nova consulta
    with st.expander("➕ Registrar Nova Consulta"):
        with st.form("new_consultation_form", clear_on_submit=True):
            consultation_date = st.date_input("Data da Consulta", value=datetime.today())
            weight_kg = st.number_input("Peso (kg)", min_value=0.0, step=0.1, format="%.1f")
            height_cm = st.number_input("Altura (cm)", min_value=0.0, step=0.1, format="%.1f")
            body_fat_percentage = st.number_input("Percentual de Gordura (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
            notes = st.text_area("Anotações da Consulta (dificuldades, sucessos, observações)")
            
            submitted_consultation = st.form_submit_button("Salvar Consulta")
            if submitted_consultation:
                db_utils.add_consultation(patient_id, consultation_date.strftime("%Y-%m-%d"), weight_kg, height_cm, body_fat_percentage, notes)
                st.success("Nova consulta registrada com sucesso!")
                st.rerun()

    # Histórico de consultas
    st.subheader("Histórico de Consultas")
    consultations = db_utils.get_consultations_for_patient(patient_id)

    if consultations.empty:
        st.info("Nenhuma consulta registrada para este paciente ainda.")
    else:
        df_display = consultations[['consultation_date', 'weight_kg', 'height_cm', 'body_fat_percentage', 'notes']].copy()
        df_display.rename(columns={
            'consultation_date': 'Data',
            'weight_kg': 'Peso (kg)',
            'height_cm': 'Altura (cm)',
            'body_fat_percentage': '% Gordura',
            'notes': 'Anotações'
        }, inplace=True)
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # --- NOVO: Opção para deletar uma consulta específica ---
        consultation_to_delete = st.selectbox(
            "Selecione uma consulta para excluir:",
            options=[f"{row['consultation_date']} - Peso: {row['weight_kg']}kg" for _, row in consultations.iterrows()],
            index=None,
            placeholder="Selecione uma consulta..."
        )
        if consultation_to_delete:
            # Encontra o ID da consulta selecionada
            selected_index = consultations.index[consultations.apply(lambda row: f"{row['consultation_date']} - Peso: {row['weight_kg']}kg" == consultation_to_delete, axis=1)].tolist()[0]
            consultation_id_to_delete = int(consultations.loc[selected_index, 'id'])

            if st.button("Excluir consulta selecionada", type="primary"):
                db_utils.delete_consultation(consultation_id_to_delete)
                st.success("Consulta excluída com sucesso.")
                st.rerun()