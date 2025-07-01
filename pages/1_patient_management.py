import streamlit as st
from datetime import datetime
from src import db_utils  # Importa nossas funções do banco de dados

st.set_page_config(page_title="Gestão de Pacientes", page_icon="👥")

st.title("👥 Gestão de Pacientes")

# --- LÓGICA PARA BUSCAR A LISTA DE PACIENTES ---
patient_list = db_utils.get_patient_list()
# Cria um dicionário para mapear nome para id, e vice-versa
patient_map = {patient['name']: patient['id'] for patient in patient_list}
patient_names = ["Cadastrar Novo Paciente"] + list(patient_map.keys())

# --- MENU DE SELEÇÃO ---
selected_patient_name = st.selectbox("Selecione um Paciente ou Cadastre um Novo", options=patient_names)

# --- LÓGICA DE EXIBIÇÃO ---

if selected_patient_name == "Cadastrar Novo Paciente":
    st.subheader("Formulário de Cadastro")
    with st.form("new_patient_form", clear_on_submit=True):
        name = st.text_input("Nome Completo", key="new_name")
        birth_date = st.date_input("Data de Nascimento", min_value=datetime(1920, 1, 1), key="new_bdate", format="DD/MM/YYYY")
        contact = st.text_input("Contato (Telefone/Email)", key="new_contact")
        medical_history = st.text_area("Histórico Clínico (patologias, alergias, objetivos...)", key="new_history")
        
        submitted = st.form_submit_button("Salvar Paciente")
        if submitted:
            if name:  # Validação simples para garantir que o nome não está vazio
                db_utils.add_patient(name, birth_date.strftime("%Y-%m-%d"), contact, medical_history)
                st.success(f"Paciente '{name}' cadastrado com sucesso!")
                st.rerun() # Recarrega a página para atualizar a lista
            else:
                st.error("O nome do paciente é obrigatório.")

else: # Se um paciente existente foi selecionado
    st.subheader(f"Informações de: {selected_patient_name}")
    
    patient_id = patient_map[selected_patient_name]
    patient_details = db_utils.get_patient_details(patient_id)

    if patient_details:
        with st.form("edit_patient_form"):
            # Converte a data de string para objeto date para o widget
            birth_date_obj = datetime.strptime(patient_details['birth_date'], '%Y-%m-%d').date()

            name = st.text_input("Nome Completo", value=patient_details['name'])
            birth_date = st.date_input("Data de Nascimento", value=birth_date_obj, min_value=datetime(1920, 1, 1))
            contact = st.text_input("Contato (Telefone/Email)", value=patient_details['contact'])
            medical_history = st.text_area("Histórico Clínico", value=patient_details['medical_history'], height=200)

            # Colunas para os botões de ação
            col1, col2 = st.columns(2)
            with col1:
                update_button = st.form_submit_button("✅ Atualizar Informações")
            with col2:
                delete_button = st.form_submit_button("❌ Excluir Paciente")

            if update_button:
                db_utils.update_patient(patient_id, name, birth_date.strftime("%Y-%m-%d"), contact, medical_history)
                st.success(f"Informações de '{name}' atualizadas com sucesso!")
                st.rerun() # Recarrega a página para refletir as mudanças

            if delete_button:
                # Adiciona um passo de confirmação para segurança
                st.session_state.confirm_delete = True
                st.session_state.patient_to_delete = (patient_id, name)
    
    # Lógica de confirmação da exclusão (fora do formulário principal)
    if 'confirm_delete' in st.session_state and st.session_state.confirm_delete:
        patient_id, name = st.session_state.patient_to_delete
        st.warning(f"**Atenção:** Você tem certeza que deseja excluir **{name}**? Esta ação não pode ser desfeita.")
        
        col1_conf, col2_conf, col3_conf = st.columns([1,1,3])
        with col1_conf:
            if st.button("Sim, excluir", type="primary"):
                db_utils.delete_patient(patient_id)
                st.success(f"Paciente '{name}' foi excluído.")
                del st.session_state.confirm_delete
                del st.session_state.patient_to_delete
                st.rerun()
        with col2_conf:
            if st.button("Não, cancelar"):
                del st.session_state.confirm_delete
                del st.session_state.patient_to_delete
                st.rerun()