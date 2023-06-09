# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_excel('Vendas.xlsx')


##criando o gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group") # x e y são as colunas que serão buscadas no excel ( read_excel)

opcoes = list(df['ID Loja'].unique())  ## opcoes é uma lista com o Id da loja (nomes dos shoppings) e unique() é para pegar só um valor de cada
opcoes.append("Todas as lojas")  #adicona na lista opcoes "todas as lojas"

app.layout = html.Div(children=[
    html.H1(children='Faturamento das lojas'),
    html.H2(children='Gráfico com o faturamento de todos os itens separados por lojas'),
    html.Div(children='''
        Obs: Esee gráfico mostra a quantidade de produtos vendidos, não o faturamento
    '''),

    html.Div(id="texto", className="dark-theme"),
    dcc.Dropdown(options=opcoes, value='Todas as lojas', id='lista_lojas', className="dark-theme"),

    # value = valor inicial, id = nome do dropdown(botão)

    dcc.Graph(
        id='Gráfico quantidade de vendas',  # id = nome do gráfico
        figure=fig
    )], className="dark-theme")

app.css.append_css({
    'external_url': 'assets/style.css'
})

@app.callback(
    Output('Gráfico quantidade de vendas', 'figure'),
    Input('lista_lojas', 'value')
)

def update_output(value):
    if value == 'Todas as lojas':
        tabela_filtrada = df
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == value, :]

    fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    fig.update_layout(template='plotly_dark')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
