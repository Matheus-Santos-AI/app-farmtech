import os
import oracledb
import pandas as pd
'''CONEXÃO COM BANCO DE DADOS'''
try:
    # Efetua a conexão com o Usuário no servidor
    conn = oracledb.connect(user='rm566901', password="160393", dsn='oracle.fiap.com.br:1521/ORCL')
    # Cria as instruções para cada módulo

    inst_consulta = conn.cursor()

except Exception as e:
    # Informa o erro
    print("Erro: ", e)
    # Flag para não executar a Aplicação
    conexao = False
else:
    # Flag para executar a Aplicação
    conexao = True
margem = '' * 4 # Define uma margem para a exibição da aplicação

'''Capturando dados do banco de dados '''
def generate_data():
    lista = []

    pd.set_option('display.max_columns', None)
    # Monta a instrução SQL de seleção de todos os registros da tabela
    inst_consulta.execute('SELECT * FROM DADOS_SIMULADOS_MILHO')
    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()

    # Insere os valores da tabela na Lista
    for dt in data:
        lista.append(dt)

    # ordena a lista
    lista = sorted(lista)

    # Gera um DataFrame com os dados da lista utilizando o Pandas
    dados_df = pd.DataFrame.from_records(lista, columns=['TIMESTAMP', 'NIVEL_N', 'NIVEL_P', 'NIVEL_K', 'VALOR_PH', 'UMIDADE_SOLO','TIPOS_SOLO','PRODUTIVIDADE'], index='TIMESTAMP')

    return dados_df

def maiores_produções():
    lista = []
    df = generate_data()
    df_ordenado = df.sort_values(by ='PRODUTIVIDADE', ascending=False)

    return df_ordenado.head(100)






