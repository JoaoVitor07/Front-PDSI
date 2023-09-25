import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
import streamlit as st
import requests

st.set_page_config(
    page_title="Meu Aplicativo",
    page_icon=":bar_chart:",
)

menu = ["Página Inicial", "Dados", "Consultar matrícula", "Configurações"]
escolha = st.sidebar.selectbox("Navegação", menu)

if escolha == "Página Inicial":

    st.markdown(
        "<h1 style='max-width: 100%; text-align: center;'>Bem-vindo ao Sistema de Acompanhamento de Desistência no Curso de Sistemas de Informação</h1>",
        unsafe_allow_html=True)
    # st.title("Bem-vindo ao Sistema de Acompanhamento de Desistência no Curso de Sistemas de Informação")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<h3 style='font-size: 24px;'>Neste sistema, fornecemos uma visão clara e informada das taxas de desistência dos alunos no curso. Através de análises detalhadas e métricas precisas, você terá acesso a informações cruciais que ajudarão a identificar tendências, fatores de risco e áreas de melhoria. Nosso objetivo é criar uma plataforma que permita a UFU, professores e administradores tomarem decisões fundamentadas para melhorar a retenção de alunos e oferecer um ambiente de aprendizado mais eficaz.</h3>",
        unsafe_allow_html=True)

elif escolha == "Dados":
    # Carregue os dados do gráfico de pizza e dos alunos
    with open('grafico.json', 'r') as json_grafico:
        dados = json.load(json_grafico)

    with open('pessoa.json', 'r') as json_file:
        matricula = json.load(json_file)


    # Crie uma função para exibir o modal
    def show_modal(matriculas):
        st.subheader("Matrículas dos Alunos:")
        for matricula in matriculas:
            st.write("Matrícula:", matricula)


    # Crie o gráfico de pizza interativo usando Plotly
    labels = ['Com perigo de desistencia', 'Sem perigo de desistencia', 'Normal']
    sizes = [dados["Com perigo de desistencia"]["qtd"], dados["Sem perigo de desistencia"]["qtd"], dados["Normal"]["qtd"]]
    colors = ['#c21b12', '#75baa8', '#f2cc67']

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, marker=dict(colors=colors))])

    # Adicione um título centralizado no topo do gráfico
    fig.add_annotation(
        text="Gráfico de alunos",
        x=0.5,
        y=1.2,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16),
    )

    # Use st.plotly_chart para exibir o gráfico no Streamlit
    st.plotly_chart(fig)

    # Capture o evento de clique no gráfico de pizza
    event = st.selectbox("Selecione uma opção:", labels)
    if event:
        # Verifique qual legenda foi clicada e exiba o modal correspondente
        if event == "Com perigo de desistencia":
            alunos = dados["Com perigo de desistencia"]["alunos"]
        elif event == "Sem perigo de desistencia":
            alunos = dados["Sem perigo de desistencia"]["alunos"]
        elif event == "Normal":
            alunos = dados["Normal"]["alunos"]

        show_modal([aluno["matricula"] for aluno in alunos])

# Pesquisar
elif escolha == "Consultar matrícula":
    #  with open('pessoa.json', 'r') as json_file:
    #    matricula = json.load(json_file)
    st.subheader("Consulta")
    termo_pesquisa = st.text_input("Consulta matrícula: ")
    if st.button("Consultar matrícula"):
        # URL para a qual você deseja fazer a requisição GET
        url = "https://4b09-200-131-207-109.ngrok-free.app/api/v1/desistenao/aluno"  # Substitua pela sua URL real
        # Fazer a requisição GET
        response = requests.get(url)
        # Verificar se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            data = response.json()  # Suponha que a resposta seja em formato JSON
            st.write("Dados obtidos com sucesso:")
            st.write(data)
        else:
            st.error(f"Falha na requisição (código de status {response.status_code})")
        # Aqui você pode implementar a lógica de pesquisa
        # st.write("Matrícula: ",response["matricula"])
        # st.write("Nome: ",response["nome"])
        # st.write("Idade: ",response["idade"])
        # st.write("Periodo: ",response["periodo"])
        # st.write("Probabilidade de evasão: ",response["probabilidade_evasao"])

# Configurações
elif escolha == "Configurações":
    st.subheader("Configurações")
