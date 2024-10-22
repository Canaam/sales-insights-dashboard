# Sales Insights Dashboard

Este projeto é um dashboard interativo que exibe insights sobre as vendas de uma base de dados fictícia (AdventureWorks). Os usuários podem filtrar vendas por produto, região e período, e visualizar gráficos interativos sobre o desempenho das vendas ao longo do tempo e por produto.

## Funcionalidades
- Filtros interativos por produto, região e datas.
- Gráficos de vendas por produto (gráfico de barras) e ao longo do tempo (gráfico de linhas).
- KPI com o total de vendas filtradas.

## Pré-requisitos

- Python 3.8+
- Um servidor de banco de dados SQL Server com a base de dados AdventureWorks instalada.
- Instalar as dependências listadas no arquivo `requirements.txt`.

### Instalação da base AdventureWorks
Você pode seguir o guia de instalação do AdventureWorks aqui:
https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure

Certifique-se de que o SQL Server esteja configurado corretamente e acessível a partir da máquina onde o dashboard será executado.

## Como rodar o projeto

1. Clone o repositório: `git clone <URL_DO_REPOSITORIO>`
2. Navegue até o diretório do projeto: `cd sales-insights-dashboard`
3. Instale as dependências: `pip install -r requirements.txt`
4. Certifique-se de que o SQL Server com a base AdventureWorks está rodando e acessível.
5. Execute o script Streamlit: `streamlit run app.py`
6. O dashboard estará acessível em seu navegador no endereço: `http://localhost:8501`

### Utilizando o Dashboard
Após iniciar o dashboard, você poderá:
- Selecionar produtos e regiões a partir do menu de filtros na barra lateral.
- Definir o intervalo de datas para visualização.
- Ver as vendas por produto em um gráfico de barras.
- Visualizar as vendas ao longo do tempo em um gráfico de linhas.
- Ver o KPI do total de vendas para os filtros selecionados.

## Problemas Comuns

### Erro de conexão com o banco de dados
Se você receber um erro de conexão com o banco de dados, verifique se:
- O SQL Server está rodando.
- As credenciais de conexão estão corretas no arquivo de configuração.
- O driver ODBC está instalado corretamente.

### O dashboard não carrega
Certifique-se de que está rodando o comando correto: `streamlit run app.py`.
Se ainda assim não funcionar, tente atualizar as dependências com `pip install --upgrade -r requirements.txt`.
