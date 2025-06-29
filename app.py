
import streamlit as st

st.set_page_config(
    page_title="Meu Nutri App",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 Bem-vinda ao seu App de Nutrição!")

st.markdown("""
### Como usar a aplicação:

Use o menu na barra lateral à esquerda para navegar entre as seções:

- **1_patient_management:** Para cadastrar, buscar e acompanhar a evolução dos seus pacientes.
- **2_meal_plan_creator:** Para montar os planos alimentares personalizados.

Esta é a página inicial. O conteúdo de cada seção está nos arquivos dentro da pasta `pages/`.
""")