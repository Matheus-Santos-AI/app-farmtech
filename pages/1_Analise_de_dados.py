import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from importando_dados import generate_data

#'''CONFIGURANDO LAYOUT'''

st.set_page_config(page_title = 'Análise de Dados do Cultivo do Milho', layout = 'wide')
st.title('Explorando dados')

#1 - Carregar dados do banco de dados e Mostra na tela do Streamlit
dados_df = generate_data()

st.header('Dados do Cultivo do Milho')

df = generate_data()

st.subheader('Dados Armazenados')
st.dataframe(df)
st.write(f'Linhas: {df.shape[0]}')

#2 - Visualizar dados
df_types = pd.DataFrame({
    'Coluna': df.columns,
    'Tipos de Dados': df.dtypes.astype(str)
})
st.subheader('Tipos dos Dados')
st.write(df_types)

# Verificar valores ausentes
st.subheader('Valores Ausentes')
st.write(df.isnull().sum())
for _ in  (df.isnull() == 0):
    dados_nulos = 0
if dados_nulos == 0:
    st.write('Nenhum Dado Ausente')

# Estatísticas Descritivas
st.subheader('Estatísticas Descritivas')
st.write(df.describe())

# 3. Análise Univariada
# ================================================
st.header('3. Análise Univariada')
numeric_columns = ['NIVEL_N', 'NIVEL_P', 'NIVEL_K', 'VALOR_PH', 'UMIDADE_SOLO','PRODUTIVIDADE']
categorical_columns = ['TIPOS_SOLO']
# Histogramas das variáveis numéricas
st.subheader('Distribuições das Variáveis Numéricas')
for col in numeric_columns:
    st.write(f'**{col}**')
    fig = px.histogram(df, x=col, nbins=30, title=f'Distribuição de {col}')
    st.plotly_chart(fig, use_container_width=True)
# Box plots das variáveis numéricas
st.subheader('Box Plots das Variáveis Numéricas')
for col in numeric_columns:
    st.write(f'**{col}**')
    fig = px.box(df, y=col, points='all', title=f'Box Plot de {col}')
    st.plotly_chart(fig, use_container_width=True)
# Distribuição das variáveis categóricas
st.subheader('Distribuições das Variáveis Categóricas')
for col in categorical_columns:
    st.write(f'**{col}**')
    fig = px.histogram(df, x=col, title=f'Distribuição de {col}')
    st.plotly_chart(fig, use_container_width=True)

# 4. Análise Bivariada
# ================================================
st.header('4. Análise Bivariada')
# Gráficos de dispersão entre variáveis numéricas
st.subheader('Gráficos de Dispersão entre Variáveis Numéricas')
variable_pairs = [
    ('UMIDADE_SOLO', 'VALOR_PH'),
    ('NIVEL_N', 'NIVEL_P', 'NIVEL_K', 'VALOR_PH'),
    ('UMIDADE_SOLO', 'PRODUTIVIDADE'),
    ('VALOR_PH', 'PRODUTIVIDADE'),
    ('NIVEL_N', 'PRODUTIVIDADE'),
    ('NIVEL_P', 'PRODUTIVIDADE'),
    ('NIVEL_K', 'PRODUTIVIDADE')

]


# Distribuição de Produção por Fertilizante e Tipo de Solo
st.subheader('Distribuição de Produção por tipos de solo e ph')
# Por Fertilizante
st.write('**Produção por Umidade do Solo**')
fig = px.violin(
    df,
    x='UMIDADE_SOLO',
    y='PRODUTIVIDADE',
    box=True,
    points='all',
    title='Distribuição de produtividade por umidade do solo'
)
st.plotly_chart(fig, use_container_width=True)
# Por Tipo de Solo
st.write('**Produção por Tipo de Solo**')
fig = px.violin(
    df,
    x='TIPOS_SOLO',
    y='PRODUTIVIDADE',
    box=True,
    points='all',
    title='Distribuição de Produtividade por Tipo de Solo'
)
st.plotly_chart(fig, use_container_width=True)




