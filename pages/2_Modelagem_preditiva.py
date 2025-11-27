# 2_Modelagem_Preditiva.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from importando_dados import generate_data, maiores_produções  # Carrega os dados do banco de dados


# Configurações gerais
st.set_page_config(page_title='Modelagem Preditiva', layout='wide')
# Título do aplicativo
st.title('Modelagem Preditiva')
# ================================================
# 1. Carregar e Filtrar os Dados
# ================================================
st.header('1. Carregar e Filtrar os Dados')
# Carregar os dados gerados
df = generate_data()
# ----------------------------------

# 1.1. Filtros na Barra Lateral
# ----------------------------------
st.sidebar.title('Filtros de Dados')

# Filtro para Tipo de Solo
selected_soil = st.sidebar.multiselect(
    'Selecione o Tipo de Solo:',
    options=df['TIPOS_SOLO'].unique(),
    default=df['TIPOS_SOLO'].unique()
)
# Filtros para variáveis numéricas
st.sidebar.subheader('Intervalos das Variáveis Numéricas')


# Nitrogenio
n_min, n_max = st.sidebar.slider(
    'Nitrogênio (mg/dm³):',
    min_value=float(df['NIVEL_N'].min()),
    max_value=float(df['NIVEL_N'].max()),
    value=(float(df['NIVEL_N'].min()), float(df['NIVEL_N'].max()))
)
# Fósforo
p_min, p_max = st.sidebar.slider(
    'Fósforo (mg/dm³):',
    min_value=float(df['NIVEL_P'].min()),
    max_value=float(df['NIVEL_P'].max()),
    value=(float(df['NIVEL_P'].min()), float(df['NIVEL_P'].max()))
)
# Potassio
k_min, k_max = st.sidebar.slider(
    'Potácio (mmol/dm³):',
    min_value=float(df['NIVEL_K'].min()),
    max_value=float(df['NIVEL_K'].max()),
    value=(float(df['NIVEL_K'].min()), float(df['NIVEL_K'].max()))
)

# PH
ph_min, ph_max = st.sidebar.slider(
    'PH :',
    min_value=float(df['VALOR_PH'].min()),
    max_value=float(df['VALOR_PH'].max()),
    value=(float(df['VALOR_PH'].min()), float(df['VALOR_PH'].max()))
)

# PH
umi_min, umi_max = st.sidebar.slider(
    'Umidade do Solo (%):',
    min_value=float(df['UMIDADE_SOLO'].min()),
    max_value=float(df['UMIDADE_SOLO'].max()),
    value=(float(df['UMIDADE_SOLO'].min()), float(df['UMIDADE_SOLO'].max()))
)


# ----------------------------------
# 1.2. Aplicar Filtros aos Dados
# ----------------------------------
# Aplicar os filtros selecionados ao DataFrame
df_filtered = df[
    (df['TIPOS_SOLO'].isin(selected_soil)) &
    (df['NIVEL_N'] >= n_min) & (df['NIVEL_N'] <= n_max) &
    (df['NIVEL_P'] >= p_min) & (df['NIVEL_P'] <= p_max) &
    (df['NIVEL_K'] >= k_min) & (df['NIVEL_K'] <= k_max) &
    (df['VALOR_PH'] >= ph_min) & (df['VALOR_PH'] <= ph_max) &
    (df['UMIDADE_SOLO'] >= umi_min) & (df['UMIDADE_SOLO'] <= umi_max)

]
# Verificar se o DataFrame filtrado não está vazio
if df_filtered.empty:
    st.warning('Nenhum dado corresponde aos filtros selecionados. Por favor, ajuste os filtros.')
    st.stop()
else:
    st.subheader('Dados Filtrados')
    st.dataframe(df_filtered.head())
# ================================================
# 2. Preparar os Dados para Modelagem
# ================================================
st.header('2. Preparar os Dados para Modelagem')
# Transformar variáveis categóricas em variáveis dummies
df_ml = pd.get_dummies(df_filtered, columns=['TIPOS_SOLO'])
# Separar as variáveis independentes (X) e a variável dependente (y)
X = df_ml.drop(['PRODUTIVIDADE'], axis=1)  #remoce a coluna produtividade de um novo dataframe
y = df_ml['PRODUTIVIDADE']  #dataframe y somente a coluna produtividade

# Verificar se há dados suficientes para treinar o modelo
if len(X) < 200:
    st.warning('Dados insuficientes para treinar o modelo. Por favor, ajuste os filtros para incluir mais dados.')
    st.stop()
else:
    st.write(f'**Total de registros após filtragem:** {len(X)}')
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
umi_input = st.number_input('Umidade do Solo (%)', value=float(df['UMIDADE_SOLO'].mean()))  #valor defalt = mean da coluna (é especificado pelo value)
n_input = st.number_input('N (mg/dm³)', value=float(df['NIVEL_N'].mean()))
p_input = st.number_input('P (mg/dm³)', value=float(df['NIVEL_P'].mean()))
k_input = st.number_input('K (mmol/dm³)', value=float(df['NIVEL_K'].mean()))
ph_input = st.number_input('PH ', value=float(df['VALOR_PH'].mean()))
tipos_de_solo_input = st.selectbox('TIPOS_SOLO', df['TIPOS_SOLO'].unique())

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
if not (0 <= n_input <= 20):
    st.error('O valor de N deve estar entre 0 e 20.')
    input_error = True
# Validar P
if not (0 <= p_input <= 20):
    st.error('O valor de P deve estar entre 0 e 20.')
    input_error = True
# Validar K
if not (0 <= k_input <= 10):
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
best_prodution = maiores_produções()

st.subheader('Melhores Produções')
st.write(best_prodution)

solo_selecionado = best_prodution[best_prodution['TIPOS_SOLO'] == tipos_de_solo_input]   #filtra o tipo de solo selecionado  dentre as 100 melhores produções

umidade_ideal = (solo_selecionado['UMIDADE_SOLO'].mean())  #calcula a media de umidadee do solo para as amostras
st.subheader(f'Melhores Produções com o Solo do tipo : {tipos_de_solo_input} ')
st.write(solo_selecionado)
st.write(f'Umidade média das melhores plantações com esse tipo de solo : {umidade_ideal:.2f} %')
cidade = st.cidade_input = ("Digite a Cidade em que a plantação se encontra:")








#PREVISÃO DO TEMPO
import requests
from datetime import datetime

# Configurações
API_KEY = "c98a2511f2c7256a82d3540e62431de6"  # Substitua pela sua chave válida
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

st.title("Previsão do Tempo e Chuva (OpenWeatherMap)")

cidade = st.text_input("Digite o nome da cidade:", "São Paulo")

if st.button("Buscar Previsão"):
    try:
        params = {
            "q": cidade,
            "appid": 'c98a2511f2c7256a82d3540e62431de6',
            "units": "metric",
            "lang": "pt_br"
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            dados = response.json()
            st.subheader(f"Previsão para {cidade}")

            previsoes = {}
            for item in dados['list']:
                dia = item['dt_txt'].split(" ")[0]
                temp = item['main']['temp']
                chuva_mm = item.get('rain', {}).get('3h', 0)
                probabilidade = item.get('pop', 0) * 100

                if dia not in previsoes:
                    previsoes[dia] = []
                previsoes[dia].append((temp, chuva_mm, probabilidade))

            for dia, valores in previsoes.items():
                temps = [v[0] for v in valores]
                chuvas = [v[1] for v in valores]
                probs = [v[2] for v in valores]

                media_temp = sum(temps) / len(temps)
                total_chuva = sum(chuvas)
                media_prob = sum(probs) / len(probs)

                data_formatada = datetime.strptime(dia, "%Y-%m-%d").strftime("%d/%m/%Y")
                st.write(f"📅 {data_formatada} → 🌡️ {media_temp:.1f}°C | 🌧️ Chuva: {total_chuva:.1f} mm | Probabilidade: {media_prob:.0f}%")

            if total_chuva == 0:
                diferenca_umidade = umidade_ideal - umi_input
                if diferenca_umidade < 0:
                    st.write("Umidade Ok")
                else:
                    if tipos_de_solo_input == 'Argiloso':
                        litros_agua = (diferenca_umidade / 7.69) * 10
                    if tipos_de_solo_input == 'Franco':
                        litros_agua = (diferenca_umidade / 7.14) * 10
                    if tipos_de_solo_input == 'Arenoso':
                        litros_agua = (diferenca_umidade / 6.25) * 10
                st.subheader("Sugestão de irrigação")
                st.write(f'De acordo com a previsão dos proximos SEIS dias é recomendado a irrigação de {litros_agua:.2f} Litros/M² distribuido ao longo dos dias para que mantenha o valor médio da umidade do solo de {umidade_ideal:.2f}% ')
            else:
                quantidade_chuva = sum(sum(v[1] for v in valores) for valores in previsoes.values())
                if tipos_de_solo_input == 'Argiloso':
                    quantidade_umidade_chuva = (quantidade_chuva /10) * 7.69
                if tipos_de_solo_input == 'Franco':
                    quantidade_umidade_chuva = (quantidade_chuva /10) * 7.14
                if tipos_de_solo_input == 'Arenoso':
                    quantidade_umidade_chuva = (quantidade_chuva /10) * 6.25

                diferenca_umidade = umidade_ideal - umi_input + quantidade_umidade_chuva
                if umidade_ideal < quantidade_umidade_chuva + umi_input:
                    st.write("Umidade Ok")
                if umidade_ideal > quantidade_umidade_chuva + umi_input:
                    litros_agua = (umidade_ideal - quantidade_umidade_chuva - umi_input)* 10

                st.subheader("Sugestão de irrigação")
                st.write(f'De acordo com a previsão dos proximos SEIS dias é recomendado a irrigação de {litros_agua:.2f} Litros/M² distribuido ao longo dos dias para que mantenha o valor médio da umidade do solo de {umidade_ideal:.2f}% ')
        elif response.status_code == 401:
            st.error("Erro: Chave da API inválida. Verifique sua chave no OpenWeatherMap.")
        elif response.status_code == 404:
            st.error("Cidade não encontrada. Verifique o nome digitado.")
        else:
            st.error(f"Erro inesperado: {response.status_code}")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")




