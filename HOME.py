import streamlit as st


st.set_page_config(
    page_title = "Analise Agricola",
    page_icon = '🌽',
    layout = 'wide'
)

st.title ("Analise Agricola 🌽")
st.write('Bem-vindo ao aplicativo agricula do Matheus')


st.markdown("""
            Este aplicatico permite explorar um banco de dados onde exitem dados simulados de produção agricola e fazer analise e predição 
            , tambem é disponibilisado uma ferramenta onde o usuario pode dafer download de uma tabela modelo para ser preenchida e em seguida carregada para que seja feita analise e predição .
            
            
            É criado com uma base de dados sinteticos da produção de milho , onde ja existe um modelo treinado como default, onde é possivel consultar esse tipo de plantação
            
            
            Utilize o menu a esqueda para navegar entre as paginas
            
            Grupo:
            
            - Matheus de S. Santos Rm566901
            - Ricardo José Amorin Rm567312
            - Klaus Lohany Barbosa de Oliveira
            - Victor Oliveira Fedeli Tate Rm566823
            - Paulo Roberto Silva Amaral Ribeiro Junior Rm568413
            """)

st.header("Mapa do APP")
st.subheader("Analise de Dados")
st.write("Aqui voce consegue ver a analise de dados sinteticos de algumas plantações de milho onde serão levados em consideração os seguintes valores:  ")
st.markdown("""
        
    - Nitogrênio (N)
    - Fósforo (P)
    - Potássio (k)
    - PH
    - Umidade do Solo
    - Tipo de Solo
    - Produtividade
    
    Serão gerados graficos para analise visual.
    """)
st.subheader("Modelagem Preditiva")
st.markdown("""Na Modelagem Preditiva será implementado os dados sinteticos do nosso banco de dados, para que seja feita a predição e tambem uma sujestão de irrigação  

A irrigação é sugerida atraves da conexão com o API meteorologico openweathermap.



                """)

st.subheader("Consulta Personalisada")

st.markdown(""" Aqui você pode fazer o download da nossa tabela modelo e após preenchida fazer um upload onde será executado um modelo de regressão para prediser sua produção atraves dos seus dados""")
