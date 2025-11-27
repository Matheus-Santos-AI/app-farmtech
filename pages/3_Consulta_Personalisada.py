import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import plotly.express as px


from io import BytesIO

st.title("Tabela Editável e Download para Excel")
st.header("Faça o Download da tabela abaixo e preencha com os dados da sua plantação")
# Dados iniciais
dados = {
    "TIMESTAMP": [],
    "NIVEL_N": [],
    "NIVEL_P": [],
    "NIVEL_K": [],
    "VALOR_PH": [],
    "UMIDADE_SOLO": [],
    "TIPOS_SOLO": [],
    "PRODUTIVIDADE": []
}

df = pd.DataFrame(dados)

# Tabela editável
df_editado = st.data_editor(df, num_rows="dynamic")

# Converter para XLSX
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_editado.to_excel(writer, index=False, sheet_name='Dados')
excel_data = output.getvalue()

# Botão para download
st.download_button(
    label="Baixar Modelo da Tabela ",
    data=excel_data,
    file_name="dados_editados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.write("**Classifique seu solo entre Franco, Arenoso e Argiloso**")
st.write("**Recomendamos um minimo de 500 linhas de dados**")


#Carregando arquivos
st.header("Carregue seus Dados:")
st.subheader("Carregue sua tabela com os dados da sua produção para realizar a predição de sua produtividade")
arquivo = st.file_uploader(f"Envie a tabela modelo preenchida:", type = ['xlsx'])   #carrega um arquivo txt
if arquivo :
    # Ler o arquivo e transformar em DataFrame
    df_upload = pd.read_excel(arquivo).drop(columns = ['TIMESTAMP'])
    st.write(df_upload)
#=============================================================================================================

    # Configurações gerais
    st.set_page_config(page_title='Modelagem Preditiva', layout='wide')
    # Título do aplicativo
    st.title('Modelagem Preditiva')

    # 2. Preparar os Dados para Modelagem
    # ================================================
    st.header('2. Preparar os Dados para Modelagem')
    # Transformar variáveis categóricas em variáveis dummies
    df_ml = pd.get_dummies(df_upload, columns=['TIPOS_SOLO'])
    # Separar as variáveis independentes (X) e a variável dependente (y)
    X = df_ml.drop(['PRODUTIVIDADE'], axis=1)  #remoce a coluna produtividade de um novo dataframe
    y = df_ml['PRODUTIVIDADE']  #dataframe y somente a coluna produtividade

    # Verificar se há dados suficientes para treinar o modelo
    if len(X) < 200:
        st.warning('Dados insuficientes para treinar o modelo. Por favor, ajuste os filtros para incluir mais dados.')
        st.stop()
    else:
        st.write(f'**Total de registros carregados:** {len(X)}')
    # ================================================
    # 3. Treinar o Modelo de Machine Learning
    # ================================================
    st.header('3. Treinar o Modelo de Machine Learning')
    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # Instanciar o modelo de Random Forest Regressor
    model = RandomForestRegressor()
    # Treinar o modelo com os dados de treinamento
    model.fit(X_train, y_train)
    # Avaliar o modelo com os dados de teste
    score = model.score(X_test, y_test)
    st.write(f'**Acurácia do modelo (R² no conjunto de teste):** {score:.2f}')

    # ================================================
    # 4. Fazer Previsões com o Modelo
    # ================================================


    st.header('4. Fazer Previsões com o Modelo')
    st.subheader('Insira os Dados para Previsão')
    # Coletar entrada do usuário para previsão
    umi_input = st.number_input('Umidade do Solo (%)', value=float(df_upload['UMIDADE_SOLO'].mean()))  #valor defalt = mean da coluna (é especificado pelo value)
    n_input = st.number_input('N (mg/dm³)', value=float(df_upload['NIVEL_N'].mean()))
    p_input = st.number_input('P (mg/dm³)', value=float(df_upload['NIVEL_P'].mean()))
    k_input = st.number_input('K (mmol/dm³)', value=float(df_upload['NIVEL_K'].mean()))
    ph_input = st.number_input('PH ', value=float(df_upload['VALOR_PH'].mean()))
    tipos_de_solo_input = st.selectbox('TIPOS_SOLO', df_upload['TIPOS_SOLO'].unique())

    # ----------------------------------
    # 4.1. Validar Entradas do Usuário
    # ----------------------------------
    # Inicializar variável de controle
    input_error = False
    # Validar umidade
    if not (0 <= umi_input <= 100):
        st.error('A umidade deve estar entre 0 e 100')
        input_error = True
    # Validar ph
    if not (0 <= ph_input  <= 7):
        st.error('O valor de PH deve estar entre 0 e 7.')
        input_error = True
    # Validar N
    if not (0 <= n_input <= 100):
        st.error('O valor de N deve estar entre 0 e 20.')
        input_error = True
    # Validar P
    if not (0 <= p_input <= 1000):
        st.error('O valor de P deve estar entre 0 e 20.')
        input_error = True
    # Validar K
    if not (0 <= k_input <= 1000):
        st.error('O valor de K deve estar entre 0 e 10.')
        input_error = True

    # Se não houver erros nas entradas, proceder com a previsão
    if not input_error:
        # ----------------------------------
        # 4.2. Preparar os Dados de Entrada
        # ----------------------------------

        # Criar um dicionário com os dados de entrada
        input_data = {
            'UMIDADE_SOLO': [umi_input],
            'VALOR_PH': [ph_input],
            'NIVEL_N': [n_input],
            'NIVEL_P': [p_input],
            'NIVEL_K': [k_input],
            # Variáveis dummies para Fertilizante
            'Tipo de solo Argiloso': [1 if tipos_de_solo_input == 'Argiloso' else 0],
            'Tipo de solo Franco': [1 if tipos_de_solo_input == 'Franco' else 0],
            'Tipo de solo Arenoso': [1 if tipos_de_solo_input == 'Arenoso' else 0],

        }
        # Converter o dicionário em um DataFrame
        input_df = pd.DataFrame(input_data)
        # Garantir que todas as colunas necessárias estejam presentes
        for col in X.columns:
            if col not in input_df.columns:
                input_df[col] = 0  # Adicionar coluna com valor zero
        # Reordenar as colunas para corresponder ao conjunto de treinamento
        input_df = input_df[X.columns]
        # ----------------------------------
        # 4.3. Realizar a Previsão
        # ----------------------------------
        # Fazer a previsão com o modelo treinado
        prediction = model.predict(input_df)
        # Exibir o resultado da previsão
        st.subheader('Resultado da Previsão')
        st.write(f'**Previsão de Produção:** {prediction[0]:.2f} ton/ha')


    #-------------------------------------------------------------------

    # VALIAR MELHORES PRODUÇÕES E SEGERIR IRRIGAÇÃO
    df_ordenado = df_upload.sort_values(by ='PRODUTIVIDADE', ascending=False)


    best_prodution = df_ordenado.head(100)

    st.subheader('Melhores Produções')
    st.write(best_prodution)

    solo_selecionado = best_prodution[best_prodution['TIPOS_SOLO'] == tipos_de_solo_input]   #filtra o tipo de solo selecionado  dentre as 100 melhores produções

    umidade_ideal = (solo_selecionado['UMIDADE_SOLO'].mean())  #calcula a media de umidadee do solo para as amostras
    st.subheader(f'Melhores Produções com o Solo do tipo : {tipos_de_solo_input} ')
    st.write(solo_selecionado)
    st.write(f'Umidade média das melhores plantações com esse tipo de solo : {umidade_ideal:.2f} %')
    cidade = st.cidade_input = ("Digite a Cidade em que a plantação se encontra:")


#==================================================
    numeric_columns = ['NIVEL_N', 'NIVEL_P', 'NIVEL_K', 'VALOR_PH', 'UMIDADE_SOLO','PRODUTIVIDADE']
    categorical_columns = ['TIPOS_SOLO']
    # Histogramas das variáveis numéricas
    st.subheader('Distribuições das Variáveis Numéricas')
    for col in numeric_columns:
        st.write(f'**{col}**')
        fig = px.histogram(df_upload, x=col, nbins=30, title=f'Distribuição de {col}')
        st.plotly_chart(fig, use_container_width=True)



    df_ordenado= df_upload.sort_values(by ='PRODUTIVIDADE')
    # Criar gráfico de linha
    fig = px.line(
        df_ordenado,
        x="PRODUTIVIDADE",
        y="VALOR_PH",
        title="Produtividade em função do PH",
        labels={"PRODUTIVIDADE": "Produtividade","VALOR_PH": "PH"}
    )

    st.write(fig)


