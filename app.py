#!/usr/bin/env python
# coding: utf-8

# # 1. Importação de Bibliotecas

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc


# # 2. Carregar Dados

# In[2]:


# Função para carregar dados com caching
@st.cache_data
def carregar_dados():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=AdventureWorks2019;'
        'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    
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
    
    df = pd.read_sql(query, conn)
    conn.close()
        
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Ano'] = df['OrderDate'].dt.year
    df['Mes'] = df['OrderDate'].dt.month
    return df


# # 3. Configurar Dashboard

# In[3]:


# Carregar dados
df = carregar_dados()

# Criação do dashboard no Streamlit
st.title("Sales Insights Dashboard")


# # 4. Filtros Interativos

# In[4]:


# Filtros interativos
st.sidebar.header("Filtros")

produto = st.sidebar.selectbox('Selecione o Produto:', df['ProductName'].unique())
regiao = st.sidebar.selectbox('Selecione a Região:', df['StateProvinceID'].unique())
data_inicial = st.sidebar.date_input('Data Inicial', df['OrderDate'].min())
data_final = st.sidebar.date_input('Data Final', df['OrderDate'].max())


# # 5. Aplicação de Filtros e Visualizações

# In[5]:


# Aplicando os filtros de forma eficiente
df_filtrado = df.query(
    "ProductName == @produto and StateProvinceID == @regiao and OrderDate >= @data_inicial and OrderDate <= @data_final"
)

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


# In[6]:


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


# # 6. KPI de Total de Vendas

# In[7]:


# KPI de Total de Vendas
total_vendas = df_filtrado['TotalDue'].sum()
st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")

