#!/usr/bin/env python
# coding: utf-8

# # Importação de bibliotecas necessárias

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc


# # Carregamento de dados com caching para melhorar a performance

# In[2]:


@st.cache_data
def carregar_dados():
    # Conexão com o banco de dados SQL Server
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'  # Substitua pelo endereço do seu servidor SQL
        'DATABASE=AdventureWorks2019;'  # Substitua pelo nome da sua base de dados
        'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)

    # Consulta SQL para extração dos dados necessários
    query = '''
    SELECT
        soh.OrderDate,
        soh.TotalDue,
        addr.StateProvinceID,
        prod.Name AS ProductName
    FROM Sales.SalesOrderHeader soh
    JOIN Sales.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
    JOIN Person.Address addr ON soh.ShipToAddressID = addr.AddressID
    JOIN Production.Product prod ON sod.ProductID = prod.ProductID
    '''
    
    # Extração dos dados em um DataFrame do Pandas
    df = pd.read_sql(query, conn)
    conn.close()

    # Conversão da data e criação de colunas auxiliares para ano e mês
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Ano'] = df['OrderDate'].dt.year
    df['Mes'] = df['OrderDate'].dt.month

    return df


# In[3]:


# Carregar os dados
df = carregar_dados()
df.shape


# # Carregar os dados

# In[4]:


df = carregar_dados()


# # Manipulação e Análise de Dados

# In[5]:


# Verificação e limpeza de dados
st.write("Dados ausentes por coluna:")
st.write(df.isnull().sum())


# In[6]:


# Remoção de dados ausentes (se necessário)
df = df.dropna()


# In[7]:


# Remoção de duplicatas
df = df.drop_duplicates()


# In[8]:


# Verificação do tipo de dados
st.write("Tipos de dados:")
st.write(df.dtypes)


# In[9]:


# Configuração do título do dashboard
st.title("Sales Insights Dashboard")


# In[10]:


# Filtros interativos no sidebar
st.sidebar.header("Filtros")


# In[11]:


# Seleção múltipla de produtos e regiões
produto = st.sidebar.multiselect('Selecione os Produtos:', df['ProductName'].unique())
regiao = st.sidebar.multiselect('Selecione as Regiões:', df['StateProvinceID'].unique())


# In[12]:


# Seleção de data inicial e data final
data_inicial = st.sidebar.date_input('Data Inicial', df['OrderDate'].min())
data_final = st.sidebar.date_input('Data Final', df['OrderDate'].max())


# In[13]:


# Aplicação dos filtros aos dados
df_filtrado = df.query(
    "ProductName in @produto and StateProvinceID in @regiao and OrderDate >= @data_inicial and OrderDate <= @data_final"
)


# # Criação de Visualizações

# In[14]:


# Verificação se há dados filtrados para exibir
if df_filtrado.empty:
    st.write("Nenhum dado disponível para os filtros selecionados.")
else:
    # Gráfico de Barras - Vendas por Produto
    vendas_por_produto = df_filtrado.groupby('ProductName')['TotalDue'].sum().reset_index()
    fig_produto = px.bar(
        vendas_por_produto,
        x='ProductName',
        y='TotalDue',
        title="Vendas por Produto",
        labels={'TotalDue': 'Valor Total (R$)', 'ProductName': 'Produto'},
        text_auto=True
    )
    st.plotly_chart(fig_produto)

 # Gráfico de Linhas - Vendas ao Longo do Tempo
    vendas_por_tempo = df_filtrado.groupby(['Ano', 'Mes'])['TotalDue'].sum().reset_index()
    fig_tempo = px.line(
        vendas_por_tempo,
        x='Ano',
        y='TotalDue',
        title="Vendas ao Longo do Tempo",
        labels={'TotalDue': 'Valor Total (R$)', 'Ano': 'Ano'},
        markers=True
    )
    st.plotly_chart(fig_tempo)


# # KPI de Total de Vendas
# 

# In[15]:


# KPI de Total de Vendas
total_vendas = df_filtrado['TotalDue'].sum()
st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")

