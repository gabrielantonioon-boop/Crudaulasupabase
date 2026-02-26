import streamlit as st
from supabase import create_client, Client
import time


URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]


supabase: Client = create_client(URL, KEY)

# Criar registros
def add_alunos(nome, email, cidade):
    supabase.table("alunos").insert({
        "nome" : nome,
        "email": email,
        "cidade" :cidade
    }).execute()


# Ler os dados da tabela
def get_alunos():
    resposta = supabase.table("alunos").select("*").order("nome").execute()
    return resposta.data

# Updates na tabela
def update_alunos(id, nome, email, cidade):
    supabase.table("alunos").update({
        "nome" : nome,
        "email": email,
        "cidade" :cidade
    }).eq("id", id).execute()

# Delete
def delete_aluno(id):
    supabase.table("alunos").delete().eq("id", id).execute()
    
# Iniciando com o Streamlit
st.title("Aprendendo CRUD")

read_alunos, create_aluno, atualizar_alunos, deletar_alunos = st.tabs(["Ver Alunos", "Criar Aluno", "Atualizar Alunos", "Deletar Alunos"])

with read_alunos:
    alunos = get_alunos()
    if alunos:
        for x in alunos:
            st.write(f"**{x["nome"]}**-- {x["email"]} -- {x["cidade"]}")

with create_aluno:
    with st.form("nome_aluno"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        cidade = st.text_input("Cidade")
        if st.form_submit_button("Adicionar"):
            if nome and email:
                add_alunos(nome, email, cidade)
                st.success(f"O {nome} foi salvo com sucesso!")
                time.sleep(20)
                st.rerun()

            else:
                st.warning("Nome e email são obrigatorios")
                

with atualizar_alunos:
    alunos= get_alunos()

    if not alunos:
        st.info("Nenhum aluno para editar")
    else:
        opcoes = {}
        chaves = []

    for aluno in alunos:
        chave_unica = aluno["nome"] +" (" +aluno["email"] + ")"
        opcoes[chave_unica] = aluno
        chaves.append(chave_unica)

    aluno_selecionado = st.selectbox(
            "Selecione",
            chaves,
            key = "edit_select"
        )
    aluno_selecionado_para_atualizar = opcoes[aluno_selecionado]

    with st.form("form_editar"):
        novo_nome = st.text_input("Nome", value = aluno_selecionado_para_atualizar["nome"])
        novo_email = st.text_input("Email",value=aluno_selecionado_para_atualizar["email"])
        nova_cidade = st.text_input("Cidade",value=aluno_selecionado_para_atualizar["cidade"])
        
        if st.form_submit_button("Salvar"):
            update_alunos(aluno_selecionado_para_atualizar["id"], novo_nome, novo_email, nova_cidade)
            st.success("Dados de aluno Atualizado")
            st.rerun()


with deletar_alunos:
    alunos = get_alunos()

    if not alunos:
        st.into("Nenhum aluno selecionado para excluir")
    else:
        opcoes = {}
        chaves = []

    for aluno in alunos:
        chave_unica =aluno["nome"] + " ("+ aluno["email"] + ")"
        opcoes[chave_unica] = aluno
        chaves.append(chave_unica)

    selecionado = st.selectbox(
        "Selecione o Aluno",
        chaves,
        key= "del_select"
    )
    
    aluno_selecionado = opcoes[selecionado]

    st.warning("Você esta prestes a excluir: **" + aluno_selecionado["nome"])

    if st.button("Excluir",type="primary"):
        delete_aluno(aluno_selecionado["id"])
        st.success("Excluido")








    