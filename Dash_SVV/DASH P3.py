# DASH P3
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


data = pd.read_csv("IcfesLimpio.csv", index_col=False)
data.head()

# Create histograms
fig_estrato = px.histogram(data, x='punt_global', color='fami_estratovivienda',
                           title='Distribución del puntaje global por estrato de vivienda',
                           labels={'punt_global': 'Puntaje Global', 'fami_estratovivienda': 'Estrato de Vivienda'},
                           barmode='overlay')

fig_naturaleza = px.histogram(data, x='punt_global', color='cole_naturaleza',
                              title='Distribución del puntaje global por naturaleza del colegio',
                              labels={'punt_global': 'Puntaje Global', 'cole_naturaleza': 'Naturaleza del Colegio'},
                              barmode='overlay')

fig_area_ubicacion = px.histogram(data, x='punt_global', color='cole_area_ubicacion',
                                  title='Distribución del puntaje global por área de ubicación del colegio',
                                  labels={'punt_global': 'Puntaje Global', 'cole_area_ubicacion': 'Área de Ubicación del Colegio'},
                                  barmode='overlay')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('Visualización del Puntaje Global'),

    html.Div([
        html.H2('Histograma del Puntaje Global por Estrato de Vivienda'),
        dcc.Graph(figure=fig_estrato)
    ]),
    
    html.Div([
        html.H2('Histograma del Puntaje Global por Naturaleza del Colegio'),
        dcc.Graph(figure=fig_naturaleza)
    ]),

    html.Div([
        html.H2('Histograma del Puntaje Global por Área de Ubicación del Colegio'),
        dcc.Graph(figure=fig_area_ubicacion)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)