import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from flask import render_template
from SistemaInventarios.modelsDB import *
import SistemaInventarios.crud as crud

from SistemaInventarios import appDash

appDash.index_string = "{%app_entry%} {%config%} {%scripts%} {%renderer%}"
appDash.layout = html.Div()

dfPieVentas = []
dfPieCompras = []


def dashboard_principal(tipoUsuario, usuario, infoUser, opcMenu):
    global dfPieVentas, dfPieCompras

    dfPieVentas = pd.DataFrame(crud.consultar_ventas_agrupada())
    dfPieCompras = pd.DataFrame(crud.consultar_compras_agrupada())

    dfLinVentas =  pd.DataFrame(crud.consultar_ventas_agrupada())
    dfLinCompras =  pd.DataFrame(crud.consultar_compras_agrupada())

    ## Importar la data barras 1
    df1 = pd.DataFrame(crud.consultar_nivelStock())

    #Crear una tabla dinámica
    pv1 = pd.pivot_table(df1, index=['nombreProducto'], columns=["nivel"], values=['cantidad'], aggfunc=sum, fill_value=0)
    trace11 = go.Bar(x=pv1.index, y=pv1[('cantidad', 'StockSeguridad')], name='StockSeguridad')
    trace12 = go.Bar(x=pv1.index, y=pv1[('cantidad', 'NivelStock')], name='NivelStock')
    trace13 = go.Bar(x=pv1.index, y=pv1[('cantidad', 'StockFaltante')], name='StockFaltante')

    ## Importar la data barras 2
    df2 = pd.DataFrame(crud.consultar_estadoVentas())
    pv2 = pd.pivot_table(df2, index=['nombreProducto'], columns=["trimestre"], values=['ventaTotal'], aggfunc=sum, fill_value=0)
    trace21 = go.Bar(x=pv2.index, y=pv2[('ventaTotal', 'Trimestre1')], name='Trimestre1')
    trace22 = go.Bar(x=pv2.index, y=pv2[('ventaTotal', 'Trimestre2')], name='Trimestre2')
    trace23 = go.Bar(x=pv2.index, y=pv2[('ventaTotal', 'Trimestre3')], name='Trimestre3')
    trace24 = go.Bar(x=pv2.index, y=pv2[('ventaTotal', 'Trimestre4')], name='Trimestre4')

    appDash.title = "Sistema de Inventarios GWM - Dashboard"

    # Personalizar HTML layout
    rtaHTML = render_template("Dashboard.html",title=appDash.title, usuario=usuario, infoUser=infoUser, opcMenu=opcMenu)
    rtaHTML = rtaHTML.replace("__app_entry__", "{%app_entry%}")
    rtaHTML = rtaHTML.replace("__config__", "{%config%}")
    rtaHTML = rtaHTML.replace("__scripts__", "{%scripts%}")
    rtaHTML = rtaHTML.replace("__renderer__", "{%renderer%}")
    html_layout = rtaHTML

    appDash.index_string = html_layout

    appDash.layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.H2(
                        children="DASHBOARD", className="header-title"
                    ),
                ],
                className="header",
            ),
            html.Table(
                children=[
                    # Linea 1
                    html.Tr(
                        children=[
                            # Linea 1 Columna 1
                            html.Td(
                                children= dcc.Graph(
                                    id='example-graph11',
                                    # config={"displayModeBar": False},     #displayModeBar": False No muestra el menu de la grafica
                                    config={"displayModeBar": True},
                                    figure={
                                        'data': [trace11, trace12, trace13],
                                        'layout':
                                        go.Layout(title='Estado del Stock de Productos', barmode='stack')
                                    },
                                ),
                                className="card",
                            ),
                            # Linea 1 Columna 2
                            html.Td(
                                children=dcc.Graph(
                                    id="price-chart12",
                                    config={"displayModeBar": True},
                                    figure={
                                        "data": [
                                            {
                                                "x": dfLinVentas["fecha"],
                                                "y": dfLinVentas["precioTotal"],
                                                "type": "lines",
                                                "hovertemplate": "$%{y:.2f}"
                                                                "<extra></extra>",
                                            },
                                        ],
                                        "layout": {
                                            "title": {
                                                "text": "Historico de Ventas",
                                                "x": 0.05,
                                                "xanchor": "left",
                                            },
                                            "xaxis": {"fixedrange": True},
                                            "yaxis": {
                                                "tickprefix": "$",
                                                "fixedrange": True,
                                            },
                                            "colorway": ["#17B897"],
                                        },
                                    },
                                ),
                                className="card",
                            ),
                        ]
                    ),
                    # Linea 2
                    html.Tr(
                        children=[
                            # Linea 2 Columna 1
                            html.Td(
                                children= dcc.Graph(
                                    id='example-graph21',
                                    config={"displayModeBar": True},
                                    figure={
                                        'data': [trace21, trace22, trace23, trace24],
                                        'layout':
                                        go.Layout(title='Estado de Ventas por Trimestre', barmode='stack')
                                    },
                                ),
                                className="card",
                            ),
                            # Linea 2 Columna 2
                            html.Td(
                                children=dcc.Graph(
                                    id="price-chart22",
                                    config={"displayModeBar": True},
                                    figure={
                                        "data": [
                                            {
                                                "x": dfLinCompras["fecha"],
                                                "y": dfLinCompras["costoTotal"],
                                                "type": "lines",
                                                "hovertemplate": "$%{y:.2f}"
                                                                "<extra></extra>",
                                            },
                                        ],
                                        "layout": {
                                            "title": {
                                                "text": "Historico de Compras",
                                                "x": 0.05,
                                                "xanchor": "left",
                                            },
                                            "xaxis": {"fixedrange": True},
                                            "yaxis": {
                                                "tickprefix": "$",
                                                "fixedrange": True,
                                            },
                                            "colorway": ["#17B897"],
                                        },
                                    },
                                ),
                                className="card",
                            ),
                        ]
                    ),
                    # Linea 3
                    html.Tr(
                        children=[
                            # Linea 3 Columna 1
                            html.Td(
                                children=[
                                    html.P("Distribución de Ventas - Items:", style={'color': 'black', 'background-color': 'White'}),
                                    dcc.Dropdown(
                                        id='items_ventas', 
                                        value='nombreProducto', 
                                        options=[{'value': x, 'label': x} 
                                                for x in ['nombreProducto', 'nombreUsuario']],
                                        clearable=False,
                                        style={'color': 'black', 'background-color': 'White'}
                                    ),
                                    html.P("Valores:", style={'color': 'black', 'background-color': 'White'}),
                                    dcc.Dropdown(
                                        id='valores_ventas', 
                                        value='precioTotal', 
                                        options=[{'value': x, 'label': x} 
                                                for x in ['precioTotal', 'cantVenta']],
                                        clearable=False,
                                        style={'color': 'black', 'background-color': 'White'}
                                    ),
                                    dcc.Graph(id="pie-chart31"),
                                ],
                                className="card",
                                style={'width': '600px', 'background-color': 'White'},
                            ),
                            # Linea 3 Columna 2
                            html.Td(
                                children=[
                                    html.P("Distribución de Compras - Items:", style={'color': 'black', 'background-color': 'White'}),
                                    dcc.Dropdown(
                                        id='items_compras', 
                                        value='nombreProducto', 
                                        options=[{'value': x, 'label': x} 
                                                for x in ['nombreProducto', 'nombreUsuario']],
                                        clearable=False,
                                        style={'color': 'black', 'background-color': 'White'}
                                    ),
                                    html.P("Valores:", style={'color': 'black', 'background-color': 'White'}),
                                    dcc.Dropdown(
                                        id='valores_compras', 
                                        value='costoTotal', 
                                        options=[{'value': x, 'label': x} 
                                                for x in ['costoTotal', 'cantCompra']],
                                        clearable=False,
                                        style={'color': 'black', 'background-color': 'White'}
                                    ),
                                    dcc.Graph(id="pie-chart32"),
                                ],
                                className="card",
                                style={'width': '600px', 'background-color': 'White'},
                            ),
                        ]
                    ),
                ],
                className="wrapper",
            ),
        ]
    )


@appDash.callback(
    Output("pie-chart31", "figure"), 
    [Input("items_ventas", "value"), 
    Input("valores_ventas", "value")])
def generate_chart1(items_ventas, valores_ventas):
    fig = px.pie(dfPieVentas, values=valores_ventas, names=items_ventas)
    return fig


@appDash.callback(
    Output("pie-chart32", "figure"), 
    [Input("items_compras", "value"), 
    Input("valores_compras", "value")])
def generate_chart2(items_compras, valores_compras):
    fig = px.pie(dfPieCompras, values=valores_compras, names=items_compras)
    return fig
