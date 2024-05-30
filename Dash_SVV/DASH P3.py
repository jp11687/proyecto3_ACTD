# DASH P3
import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
from dotenv import load_dotenv # pip install python-dotenv
import os
import keras
import psycopg2
import pandas as pd
import os
import plotly.express as px
import numpy as np
from sklearn.preprocessing import StandardScaler


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

#Extraer datos normales para visualización
data = pd.read_csv("C:\\Users\\ASUS\\Documents\\Uniandes\\8vo semestre\\Analítica\\Proyecto 3\\IcfesLimpio.csv", index_col=False)
data.head()

###########################
###########################
###########################
###########################
###########################
###########################

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


###########################
###########################
###########################
###########################
###########################
###########################
###########################
###########################
###########################
###########################
#Importar datos modificados para usar en el modelo
data3 = pd.read_csv("C:\\Users\\ASUS\\Documents\\Uniandes\\8vo semestre\\Analítica\\Proyecto 3\\datosModelo.csv", index_col=False)
data2=data3.drop(columns=['punt_global', 'punt_ingles', 'punt_matematicas', 'punt_sociales_ciudadanas', 'punt_c_naturales', 'punt_lectura_critica'])
#importar modelo
model = keras.models.load_model("C:\\Users\\ASUS\\Documents\\Uniandes\\8vo semestre\\Analítica\\Proyecto 3\\model.h5")

# Crear el layout de la aplicación
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
    ]),
    
    
    
    html.H3("Dashboard de Predicción"),

    # Inputs para las columnas del dataset
    html.Label("Tipo de Documento"),
    dcc.Dropdown(
        id='tipo-documento',
        options=[
            {'label': 'CC', 'value': 'CC'},
            {'label': 'TI', 'value': 'TI'},
            {'label': 'CE', 'value': 'CE'},
            {'label': 'CR', 'value': 'CR'},
            {'label': 'NES', 'value': 'NES'},
            {'label': 'PC', 'value': 'PC'},
            {'label': 'PE', 'value': 'PE'},
            {'label': 'PEP', 'value': 'PEP'},
            {'label': 'PPT', 'value': 'PPT'},
            {'label': 'RC', 'value': 'RC'},
            {'label': 'V', 'value': 'V'}
        ],
        value='CC'  # Valor por defecto
    ),
    
    html.Label("Ubicación"),
    dcc.Dropdown(
        id='ubicacion',
        options=[
            {'label': 'Rural', 'value': 'R'},
            {'label': 'Urbano', 'value': 'U'}
        ],
        value='R'  # Valor por defecto
    ),
    
    html.Label("Colegio Bilingüe"),
    dcc.Dropdown(
        id='colebil',
        options=[
            {'label': 'Si', 'value': 'S'},
            {'label': 'No', 'value': 'N'}
        ],
        value='S'  # Valor por defecto
    ),
    
    html.Label("Colegio Caracter"),
    dcc.Dropdown(
        id='colecar',
        options=[
            {'label': 'ACADEMICO', 'value': 'A'},
            {'label': 'NO APLICA', 'value': 'NA'},
            {'label': 'TÉCNICO', 'value': 'T'},
            {'label': 'TÉCNICO ACADÉMICO', 'value': 'TA'}
        ],
        value='A'  # Valor por defecto
    ),
    
    
    html.Label("Colegio Genero"),
    dcc.Dropdown(
        id='colegen',
        options=[
            {'label': 'FEMENINO', 'value': 'F'},
            {'label': 'MASCULINO', 'value': 'M'},
            {'label': 'MIXTO', 'value': 'MX'}
        ],
        value='M'  # Valor por defecto
    ),
    
    
    html.Label("Colegio Jornada"),
    dcc.Dropdown(
        id='colejor',
        options=[
            {'label': 'COMPLETA', 'value': 'C'},
            {'label': 'MAÑANA', 'value': 'M'},
            {'label': 'NOCHE', 'value': 'N'},
            {'label': 'SABATINA', 'value': 'S'},
            {'label': 'TARDE', 'value': 'T'},
            {'label': 'UNICA', 'value': 'U'}
        ],
        value='M'  # Valor por defecto
    ),
    
    html.Label("Colegio Naturaleza"),
    dcc.Dropdown(
        id='colenat',
        options=[
            {'label': 'NO OFICIAL', 'value': 'NO'},
            {'label': 'OFICIAL', 'value': 'O'}
        ],
        value='NO'  # Valor por defecto
    ),
    
    
    html.Label("estu_cod_depto_presentacion"),
    dcc.Dropdown(
        id='estu_cod_depto_presentacion',
        options=[
            #{'label': "PUTUMAYO", 'value': "86"},
            #{'label': "BOLIVAR", 'value': "13"},
            {'label': "ATLANTICO", 'value': "8"},
            {'label': "SUCRE", 'value': "70"},
            {'label': "CESAR", 'value': "20"},
            {'label': "VICHADA", 'value': "99"},
            {'label': "ARAUCA", 'value': "81"},
            {'label': "CAUCA", 'value': "19"},
            #{'label': "HUILA", 'value': "41"},
            {'label': "CUNDINAMARCA", 'value': "25"},
            {'label': "META", 'value': "50"},
            #{'label': "AMAZONAS", 'value': "91"},
            #{'label': "MAGDALENA", 'value': "47"},
            {'label': "BOGOTÁ", 'value': "11"},
            {'label': "RISARALDA", 'value': "66"},
            {'label': "BOYACA", 'value': "15"},
            {'label': "QUINDIO", 'value': "63"},
            {'label': "CALDAS", 'value': "17"},
            {'label': "CASANARE", 'value': "85"},
            #{'label': "GUAVIARE", 'value': "95"},
            {'label': "TOLIMA", 'value': "73"},
            {'label': "SANTANDER", 'value': "68"},
            #{'label': "VAUPES", 'value': "97"},
            {'label': "NORTE SANTANDER", 'value': "54"},
            {'label': "VALLE", 'value': "76"},
            {'label': "ANTIOQUIA", 'value': "5"}
            
        ],
        value='8'  # Valor por defecto
    ),
    
    
    html.Label("estu_cod_reside_depto"),
    dcc.Dropdown(
        id='estu_cod_reside_depto',
        options=[
            #{'label': "CAQUETA", 'value': "18"},
            #{'label': "PUTUMAYO", 'value': "86"},
            #{'label': "BOLIVAR", 'value': "13"},
            {'label': "SANTANDER", 'value': "68"},
            {'label': "BOYACA", 'value': "15"},
            {'label': "ANTIOQUIA", 'value': "5"},
            {'label': "VALLE", 'value': "76"},
            #{'label': "MAGDALENA", 'value': "47"},
            {'label': "CESAR", 'value': "20"},
            {'label': "ATLANTICO", 'value': "8"},
            {'label': "SUCRE", 'value': "70"},
            #{'label': "HUILA", 'value': "41"},
            #{'label': "GUAINIA", 'value': "94"},
            {'label': "ARAUCA", 'value': "81"},
            #{'label': "CAUCA", 'value': "19"},
            {'label': "TOLIMA", 'value': "73"},
            {'label': "NARIÑO", 'value': "52"},
            {'label': "BOGOTÁ", 'value': "11"},
            {'label': "RISARALDA", 'value': "66"},
            #{'label': "CORDOBA", 'value': "23"},
            {'label': "NORTE SANTANDER", 'value': "54"},
            #{'label': "GUAVIARE", 'value': "95"},
            {'label': "CUNDINAMARCA", 'value': "25"},
            {'label': "META", 'value': "50"},
            #{'label': "VAUPES", 'value': "97"},
            {'label': "CASANARE", 'value': "85"},
            {'label': "CALDAS", 'value': "17"},
            {'label': "QUINDIO", 'value': "63"}
            
        ],
        value='8'  # Valor por defecto
    ),
    
    
    html.Label("estu_estadoinvestigacion"),
    dcc.Dropdown(
        id='estu_estadoinvestigacion',
        options=[
            {'label': "NO SE COMPROBÓ IDENTIDAD DEL EXAMINADO", 'value': "NSC"},
            {'label': "PRESENTE CON LECTURA TARDIA", 'value': "PCL"},
            {'label': "PUBLICAR", 'value': "P"},
            {'label': "VALIDEZ OFICINA JURÍDICA", 'value': "VOJ"}
        ],
        value='P'  # Valor por defecto
    ),
    
    
    html.Label("estu_genero"),
    dcc.Dropdown(
        id='estu_genero',
        options=[
            {'label': "estu_genero_F", 'value': "F"},
            {'label': "estu_genero_M", 'value': "M"}
        ],
        value='F'  # Valor por defecto
    ),
    
    
    html.Label("estu_nacionalidad"),
    dcc.Dropdown(
        id='estu_nacionalidad',
        options=[
            {'label': "Colombia", 'value': "COL"},
            {'label': "Comoras", 'value': "COM"},
            {'label': "Corea del Norte", 'value': "CDN"},
            {'label': "Ecuador", 'value': "ECU"},
            {'label': "USA", 'value': "USA"},
            {'label': "Italia", 'value': "ITA"},
            {'label': "Jordania", 'value': "JOR"},
            {'label': "Venezuela", 'value': "VEN"}
        ],
        value='VEN'  # Valor por defecto
    ),
    
    html.Label("Privado de la libertad"),
    dcc.Dropdown(
        id='estu_privado',
        options=[
            {'label': "estu_privado_libertad_N", 'value': "NO"},
            {'label': "estu_privado_libertad_S", 'value': "SI"}
        ],
        value='NO'  # Valor por defecto
    ),
    
    
    html.Label("Cuartos en el hogar"),
    dcc.Dropdown(
        id='fami_cuartoshogar',
        options=[
            {'label': "fami_cuartoshogar_1 a 2", 'value': "1 a 2"},
            {'label': "fami_cuartoshogar_3 a 4", 'value': "3 a 4"},
            {'label': "fami_cuartoshogar_5 a 6", 'value': "5 a 6"},
            {'label': "fami_cuartoshogar_7 a 8", 'value': "7 a 8"},
            {'label': "fami_cuartoshogar_9 o más", 'value': "9 o más"}
        ],
        value='1 a 2'  # Valor por defecto
    ),
    
    
    
    html.Label("Educación madre"),
    dcc.Dropdown(
        id='edumadre',
        options=[
            {'label': "Madre profesional completa", 'value': "MPC"},
            {'label': "Madre profesional incompleta", 'value': "MPIC"},
            {'label': "Madre no aplica", 'value': "NA"},
            {'label': "Madre ninguno", 'value': "N"},
            {'label': "Madre no sabe", 'value': "NS"},
            {'label': "Madre postgrado", 'value': "P"},
            {'label': "Madre primaria completa", 'value': "PC"},
            {'label': "Madre primaria incompleta", 'value': "PIC"},
            {'label': "Madre bachillerato completo", 'value': "BC"},
            {'label': "Madre bachillerato incompleto", 'value': "BIC"},
            {'label': "Madre técnica o tecnológica completa", 'value': "TTC"},
            {'label': "Madre técnica o tecnológica incompleta", 'value': "TTIC"}
        ],
        value='MPC'  # Valor por defecto
    ),
    
    html.Label("Educación padre"),
    dcc.Dropdown(
        id='edupadre',
        options=[
            {'label': "Padre profesional completa", 'value': "PPC"},
            {'label': "Padre profesional incompleta", 'value': "PPIC"},
            {'label': "Padre no aplica", 'value': "NA"},
            {'label': "Padre ninguno", 'value': "N"},
            {'label': "Padre no sabe", 'value': "NS"},
            {'label': "Padre postgrado", 'value': "P"},
            {'label': "Padre primaria completa", 'value': "PC"},
            {'label': "Padre primaria incompleta", 'value': "PIC"},
            {'label': "Padre bachillerato completo", 'value': "BC"},
            {'label': "Padre bachillerato incompleto", 'value': "BIC"},
            {'label': "Padre técnica o tecnológica completa", 'value': "TTC"},
            {'label': "Padre técnica o tecnológica incompleta", 'value': "TTIC"}
        ],
        value='PPC'  # Valor por defecto
    ),

    html.Label("Estrato"),
    dcc.Dropdown(
        id='estrato',
        options=[
            {'label': "Estrato 1", 'value': "1"},
            {'label': "Estrato 2", 'value': "2"},
            {'label': "Estrato 3", 'value': "3"},
            {'label': "Estrato 4", 'value': "4"},
            {'label': "Estrato 5", 'value': "5"},
            {'label': "Estrato 6", 'value': "6"},
            {'label': "Sin Estrato", 'value': "SE"}
        ],
        value='3'  # Valor por defecto
    ),

    
    html.Label("Personas en hogar"),
    dcc.Dropdown(
        id='personashogar',
        options=[
            {'label': "1 a 2 personas", 'value': "1 a 2"},
            {'label': "3 a 4 personas", 'value': "3 a 4"},
            {'label': "5 a 6 personas", 'value': "5 a 6"},
            {'label': "7 a 8 personas", 'value': "7 a 8"},
            {'label': "9 o más personas", 'value': "9 o más"}
        ],
        value='3 a 4'  # Valor por defecto
    ),
    
    html.Label("Automovil"),
    dcc.Dropdown(
        id='Automovil',
        options=[
            {'label': "Tienen", 'value': "T"},
            {'label': "No Tienen", 'value': "NT"}
        ],
        value='T'  # Valor por defecto
    ),
    
    html.Label("Computador"),
    dcc.Dropdown(
        id='Computador',
        options=[
            {'label': "Tienen", 'value': "T"},
            {'label': "No Tienen", 'value': "NT"}
        ],
        value='T'  # Valor por defecto
    ),
    
    html.Label("Internet"),
    dcc.Dropdown(
        id='Internet',
        options=[
            {'label': "Tienen", 'value': "T"},
            {'label': "No Tienen", 'value': "NT"}
        ],
        value='T'  # Valor por defecto
    ),
    
    html.Label("Lavadora"),
    dcc.Dropdown(
        id='Lavadora',
        options=[
            {'label': "Tienen", 'value': "T"},
            {'label': "No Tienen", 'value': "NT"}
        ],
        value='T'  # Valor por defecto
    ),
    
    html.Label("Inglés"),
    dcc.Dropdown(
        id='ingles',
        options=[
            {'label': "A-", 'value': "A-"},
            {'label': "A1", 'value': "A1"},
            {'label': "A2", 'value': "A2"},
            {'label': "B+", 'value': "B+"},
            {'label': "B1", 'value': "B1"}
        ],
        value='A2'  # Valor por defecto
    ),
    
    html.Label("Semestre"),
    dcc.Dropdown(
        id='semestre',
        options=[
            {'label': "Semestre 1", 'value': "S1"},
            {'label': "Semestre 2", 'value': "S2"},
            {'label': "Semestre 4", 'value': "S4"}
        ],
        value='S2'  # Valor por defecto
    ),
    
    html.Label("Establecimiento:"),
    dcc.Input(
        id='est',
        type='number',  # Specifies that the input should be a number
        value=256.5528151610253  # Default value
    ),
    
    html.Label("Sede:"),
    dcc.Input(
        id='sede',
        type='number',  # Specifies that the input should be a number
        value=256.5528151610253  # Default value
    ),
    
    html.Label("Ubicación:"),
    dcc.Input(
        id='ubic',
        type='number',  # Specifies that the input should be a number
        value=256.5528151610253  # Default value
    ),
    html.Label("presentación:"),
    dcc.Input(
        id='pres',
        type='number',  # Specifies that the input should be a number
        value=256.5528151610253  # Default value
    ),
    html.Label("Reside:"),
    dcc.Input(
        id='res',
        type='number',  # Specifies that the input should be a number
        value=256.5528151610253  # Default value
    ),
    html.Label("Año:"),
    dcc.Input(
        id='anio',
        type='number',  # Specifies that the input should be a number
        value=2015  # Default value
    ),
    html.Label("Año nacimiento:"),
    dcc.Input(
        id='nac',
        type='number',  # Specifies that the input should be a number
        value=1999  # Default value
    ),



    # Botón para hacer la predicción
    html.Button('Predecir', id='predict-button', n_clicks=0),

    # Salida de la predicción
    html.Div(id='prediction-output')
])

# Definir los callbacks para manejar la lógica
@app.callback(
    Output('prediction-output', 'children'),
    [
    Input('predict-button', 'n_clicks'),
    Input('tipo-documento', 'value'),
    Input('ubicacion', 'value'),
    Input('colebil', 'value'),
    Input('colecar', 'value'),
    Input('colegen', 'value'),
    Input('colejor', 'value'),
    Input('colenat', 'value'),
    Input('estu_cod_depto_presentacion', 'value'),
    Input('estu_cod_reside_depto', 'value'),
    Input('estu_estadoinvestigacion', 'value'),
    Input('estu_genero', 'value'),
    Input('estu_nacionalidad', 'value'),
    Input('estu_privado', 'value'),
    Input('fami_cuartoshogar', 'value'),
    Input('edumadre', 'value'),
    Input('edupadre', 'value'),
    Input('estrato', 'value'),
    Input('personashogar', 'value'),
    Input('Automovil', 'value'),
    Input('Computador', 'value'),
    Input('Internet', 'value'),
    Input('Lavadora', 'value'),
    Input('ingles', 'value'),
    Input('semestre', 'value'),
    Input('est', 'value'),
    Input('sede', 'value'),
    Input('ubic', 'value'),
    Input('pres', 'value'),
    Input('res', 'value'),
    Input('anio', 'value'),
    Input('nac', 'value')]
)








def update_output(n_clicks, tipo_documento, ubicacion, colebil, colecar, colegen, colejor, colenat, estu_cod_depto_presentacion,estu_cod_reside_depto,estu_estadoinvestigacion, estu_genero, estu_nacionalidad, estu_privado, fami_cuartoshogar, edumadre, edupadre, estrato,personashogar, Automovil,Computador,Internet,Lavadora,ingles,semestre,est,sede,ubic,pres,res,anio,nac):
    if n_clicks > 0:
        # Crear un array de entrada para el modelo basado en los inputs del usuario
        input_data = np.zeros((1, len(data2.columns)))  # Ajusta según el número de columnas de tus datos

        # Asignar valores basados en el tipo de documento
        input_data[0, data2.columns.get_loc('estu_tipodocumento_CC')] = True if tipo_documento == 'CC' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_TI')] = True if tipo_documento == 'TI' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_CE')] = True if tipo_documento == 'CE' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_CR')] = True if tipo_documento == 'CR' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_NES')] = True if tipo_documento == 'NES' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_PC')] = True if tipo_documento == 'PC' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_PE')] = True if tipo_documento == 'PE' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_PEP')] = True if tipo_documento == 'PEP' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_PPT')] = True if tipo_documento == 'PPT' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_RC')] = True if tipo_documento == 'RC' else False
        input_data[0, data2.columns.get_loc('estu_tipodocumento_V')] = True if tipo_documento == 'V' else False
        
        #Asignar valores basados en ubicación
        input_data[0, data2.columns.get_loc('cole_area_ubicacion_RURAL')] = True if ubicacion == 'R' else False
        input_data[0, data2.columns.get_loc('cole_area_ubicacion_URBANO')] = True if ubicacion == 'U' else False
        
        #Asignar valores basados colegio bilingüe
        
        input_data[0, data2.columns.get_loc('cole_bilingue_N')] = True if colebil == 'N' else False
        input_data[0, data2.columns.get_loc('cole_bilingue_S')] = True if colebil == 'S' else False
        
        #Asignar valores basados colegio caracter
        input_data[0, data2.columns.get_loc('cole_caracter_ACADÉMICO')] = True if colecar == 'A' else False
        input_data[0, data2.columns.get_loc('cole_caracter_NO APLICA')] = True if colecar == 'NA' else False
        input_data[0, data2.columns.get_loc('cole_caracter_TÉCNICO')] = True if colecar == 'T' else False
        input_data[0, data2.columns.get_loc('cole_caracter_TÉCNICO/ACADÉMICO')] = True if colecar == 'TA' else False

        #Asignar valores basados colegio genero
        input_data[0, data2.columns.get_loc('cole_genero_MASCULINO')] = True if colegen == 'M' else False
        input_data[0, data2.columns.get_loc('cole_genero_FEMENINO')] = True if colegen == 'F' else False
        input_data[0, data2.columns.get_loc('cole_genero_MIXTO')] = True if colegen == 'MX' else False
        #Asignar valores basados colegio jornada
        input_data[0, data2.columns.get_loc('cole_jornada_COMPLETA')] = True if colejor == 'C' else False
        input_data[0, data2.columns.get_loc('cole_jornada_MAÑANA')] = True if colejor == 'M' else False
        input_data[0, data2.columns.get_loc('cole_jornada_NOCHE')] = True if colejor == 'N' else False
        input_data[0, data2.columns.get_loc('cole_jornada_SABATINA')] = True if colejor == 'S' else False
        input_data[0, data2.columns.get_loc('cole_jornada_TARDE')] = True if colejor== 'T' else False
        input_data[0, data2.columns.get_loc('cole_jornada_UNICA')] = True if colejor == 'U' else False
        #Asignar valores basados colegio naturaleza
        input_data[0, data2.columns.get_loc('cole_naturaleza_NO OFICIAL')] = True if colenat == 'NO' else False
        input_data[0, data2.columns.get_loc('cole_naturaleza_OFICIAL')] = True if colenat == 'O' else False
        
         #Asignar valores basados estu_cod_depto_presentacion
        
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_86')] = True if estu_cod_depto_presentacion == '86' else False
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_13')] = True if estu_cod_depto_presentacion == '13' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_8')] = True if estu_cod_depto_presentacion == '8' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_70')] = True if estu_cod_depto_presentacion == '70' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_20')] = True if estu_cod_depto_presentacion == '20' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_99')] = True if estu_cod_depto_presentacion == '99' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_81')] = True if estu_cod_depto_presentacion == '81' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_19')] = True if estu_cod_depto_presentacion == '19' else False
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_41')] = True if estu_cod_depto_presentacion == '41' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_25')] = True if estu_cod_depto_presentacion == '25' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_50')] = True if estu_cod_depto_presentacion == '50' else False
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_91')] = True if estu_cod_depto_presentacion == '91' else False
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_47')] = True if estu_cod_depto_presentacion == '47' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_11')] = True if estu_cod_depto_presentacion == '11' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_66')] = True if estu_cod_depto_presentacion == '66' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_15')] = True if estu_cod_depto_presentacion == '15' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_63')] = True if estu_cod_depto_presentacion == '63' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_17')] = True if estu_cod_depto_presentacion == '17' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_85')] = True if estu_cod_depto_presentacion == '85' else False
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_95')] = True if estu_cod_depto_presentacion == '95' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_73')] = True if estu_cod_depto_presentacion == '73' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_68')] = True if estu_cod_depto_presentacion == '68' else False
        #input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_97')] = True if estu_cod_depto_presentacion == '97' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_54')] = True if estu_cod_depto_presentacion == '54' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_76')] = True if estu_cod_depto_presentacion == '76' else False
        input_data[0, data2.columns.get_loc('estu_cod_depto_presentacion_5')] = True if estu_cod_depto_presentacion == '5' else False
        
        
        #Asignar valores basados estu_cod_depto_presentacion

        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_18')] = True if estu_cod_reside_depto == '18' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_86')] = True if estu_cod_reside_depto == '86' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_13')] = True if estu_cod_reside_depto == '13' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_68.0')] = True if estu_cod_reside_depto == '68' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_15.0')] = True if estu_cod_reside_depto == '15' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_5.0')] = True if estu_cod_reside_depto == '5' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_76.0')] = True if estu_cod_reside_depto == '76' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_47')] = True if estu_cod_reside_depto == '47' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_20.0')] = True if estu_cod_reside_depto == '20' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_8.0')] = True if estu_cod_reside_depto == '8' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_70.0')] = True if estu_cod_reside_depto == '70' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_41')] = True if estu_cod_reside_depto == '41' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_94')] = True if estu_cod_reside_depto == '94' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_81.0')] = True if estu_cod_reside_depto == '81' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_19')] = True if estu_cod_reside_depto == '19' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_73.0')] = True if estu_cod_reside_depto == '73' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_52.0')] = True if estu_cod_reside_depto == '52' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_11.0')] = True if estu_cod_reside_depto == '11' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_66.0')] = True if estu_cod_reside_depto == '66' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_23')] = True if estu_cod_reside_depto == '23' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_54.0')] = True if estu_cod_reside_depto == '54' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_85.0')] = True if estu_cod_reside_depto == '85' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_95')] = True if estu_cod_reside_depto == '95' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_25.0')] = True if estu_cod_reside_depto == '25' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_50.0')] = True if estu_cod_reside_depto == '50' else False
        #input_data[0, data2.columns.get_loc('estu_cod_reside_depto_97')] = True if estu_cod_reside_depto == '97' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_17.0')] = True if estu_cod_reside_depto == '17' else False
        input_data[0, data2.columns.get_loc('estu_cod_reside_depto_63.0')] = True if estu_cod_reside_depto == '63' else False
        
        
        #Asignar valores basados estu_estadoinvestigacion

        input_data[0, data2.columns.get_loc('estu_estadoinvestigacion_NO SE COMPROBO IDENTIDAD DEL EXAMINADO')] = True if estu_estadoinvestigacion == 'NSC' else False
        input_data[0, data2.columns.get_loc('estu_estadoinvestigacion_PRESENTE CON LECTURA TARDIA')] = True if estu_estadoinvestigacion == 'PCL' else False
        input_data[0, data2.columns.get_loc('estu_estadoinvestigacion_PUBLICAR')] = True if estu_estadoinvestigacion == 'P' else False
        input_data[0, data2.columns.get_loc('estu_estadoinvestigacion_VALIDEZ OFICINA JURÍDICA')] = True if estu_estadoinvestigacion == 'VOJ' else False
        
        #Asignar valores estu_genero
        input_data[0, data2.columns.get_loc('estu_genero_F')] = True if estu_genero == 'F' else False
        input_data[0, data2.columns.get_loc('estu_genero_M')] = True if estu_genero == 'M' else False
        
        
        # Asignar valores basados en la nacionalidad
        input_data[0, data2.columns.get_loc('estu_nacionalidad_COLOMBIA')] = True if estu_nacionalidad == 'COL' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_COMORAS')] = True if estu_nacionalidad == 'COM' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_COREA DEL NORTE')] = True if estu_nacionalidad == 'CDN' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_ECUADOR')] = True if estu_nacionalidad == 'ECU' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_ESTADOS UNIDOS')] = True if estu_nacionalidad == 'USA' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_ITALIA')] = True if estu_nacionalidad == 'ITA' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_JORDANIA')] = True if estu_nacionalidad == 'JOR' else False
        input_data[0, data2.columns.get_loc('estu_nacionalidad_VENEZUELA')] = True if estu_nacionalidad == 'VEN' else False
        
        
        #Asignar valores basados privado de la libertad
        input_data[0, data2.columns.get_loc('estu_privado_libertad_N')] = True if estu_privado == 'NO' else False
        input_data[0, data2.columns.get_loc('estu_privado_libertad_S')] = True if estu_privado == 'SI' else False
        
        
        
        # Asignar valores basados en cuartos familia
        input_data[0, data2.columns.get_loc('fami_cuartoshogar_1 a 2')] = True if fami_cuartoshogar == '1 a 2' else False
        input_data[0, data2.columns.get_loc('fami_cuartoshogar_3 a 4')] = True if fami_cuartoshogar == '3 a 4' else False
        input_data[0, data2.columns.get_loc('fami_cuartoshogar_5 a 6')] = True if fami_cuartoshogar == '5 a 6' else False
        input_data[0, data2.columns.get_loc('fami_cuartoshogar_7 a 8')] = True if fami_cuartoshogar == '7 a 8' else False
        input_data[0, data2.columns.get_loc('fami_cuartoshogar_9 o más')] = True if fami_cuartoshogar == '9 o más' else False
        
        
        #Asignar valores basados educación madre

        input_data[0, data2.columns.get_loc('fami_educacionmadre_Educación profesional completa')] = True if edumadre == 'MPC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Educación profesional incompleta')] = True if edumadre == 'MPIC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Ninguno')] = True if edumadre == 'N' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_No Aplica')] = True if edumadre == 'NA' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_No sabe')] = True if edumadre == 'NS' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Postgrado')] = True if edumadre == 'P' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Primaria completa')] = True if edumadre == 'PC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Primaria incompleta')] = True if edumadre == 'PIC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Secundaria (Bachillerato) completa')] = True if edumadre == 'BC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Secundaria (Bachillerato) incompleta')] = True if edumadre == 'BIC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Técnica o tecnológica completa')] = True if edumadre == 'TTC' else False
        input_data[0, data2.columns.get_loc('fami_educacionmadre_Técnica o tecnológica incompleta')] = True if edumadre == 'TTIC' else False
        
        #Asignar valores basados educación padre

        input_data[0, data2.columns.get_loc('fami_educacionpadre_Educación profesional completa')] = True if edupadre == 'PPC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Educación profesional incompleta')] = True if edupadre == 'PPIC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Ninguno')] = True if edupadre == 'N' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_No Aplica')] = True if edupadre == 'NA' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_No sabe')] = True if edupadre == 'NS' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Postgrado')] = True if edupadre == 'P' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Primaria completa')] = True if edupadre == 'PC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Primaria incompleta')] = True if edupadre == 'PIC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Secundaria (Bachillerato) completa')] = True if edupadre == 'BC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Secundaria (Bachillerato) incompleta')] = True if edupadre == 'BIC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Técnica o tecnológica completa')] = True if edupadre == 'TTC' else False
        input_data[0, data2.columns.get_loc('fami_educacionpadre_Técnica o tecnológica incompleta')] = True if edupadre == 'TTIC' else False
        
        
         #Asignar valores basados estrato

        input_data[0, data2.columns.get_loc('fami_estratovivienda_Estrato 1')] = True if estrato == '1' else False
        input_data[0, data2.columns.get_loc('fami_estratovivienda_Estrato 2')] = True if estrato == '2' else False
        input_data[0, data2.columns.get_loc('fami_estratovivienda_Estrato 3')] = True if estrato == '3' else False
        input_data[0, data2.columns.get_loc('fami_estratovivienda_Estrato 4')] = True if estrato == '4' else False
        input_data[0, data2.columns.get_loc('fami_estratovivienda_Estrato 5')] = True if estrato == '5' else False
        input_data[0, data2.columns.get_loc('fami_estratovivienda_Estrato 6')] = True if estrato == '6' else False
        input_data[0, data2.columns.get_loc('fami_estratovivienda_Sin Estrato')] = True if estrato == 'SE' else False
        
        # Asignar valores basados en personas familia
        input_data[0, data2.columns.get_loc('fami_personashogar_1 a 2')] = True if personashogar == '1 a 2' else False
        input_data[0, data2.columns.get_loc('fami_personashogar_3 a 4')] = True if personashogar == '3 a 4' else False
        input_data[0, data2.columns.get_loc('fami_personashogar_5 a 6')] = True if personashogar == '5 a 6' else False
        input_data[0, data2.columns.get_loc('fami_personashogar_7 a 8')] = True if personashogar == '7 a 8' else False
        input_data[0, data2.columns.get_loc('fami_personashogar_9 o más')] = True if personashogar == '9 o más' else False
        
        #Tienen automovil Computador
        input_data[0, data2.columns.get_loc('fami_tieneautomovil_Si')] = True if Automovil == 'T' else False
        input_data[0, data2.columns.get_loc('fami_tieneautomovil_No')] = True if Automovil== 'NT' else False
        input_data[0, data2.columns.get_loc('fami_tienecomputador_Si')] = True if Computador == 'T' else False
        input_data[0, data2.columns.get_loc('fami_tienecomputador_No')] = True if Computador== 'NT' else False
        input_data[0, data2.columns.get_loc('fami_tieneinternet_Si')] = True if Internet == 'T' else False
        input_data[0, data2.columns.get_loc('fami_tieneinternet_No')] = True if Internet== 'NT' else False
        input_data[0, data2.columns.get_loc('fami_tienelavadora_Si')] = True if Lavadora == 'T' else False
        input_data[0, data2.columns.get_loc('fami_tienelavadora_No')] = True if Lavadora== 'NT' else False
        
        
        #Desempeño Inglés
        
        input_data[0, data2.columns.get_loc('desemp_ingles_A-')] = True if ingles== 'A-' else False
        input_data[0, data2.columns.get_loc('desemp_ingles_A1')] = True if ingles == 'A1' else False
        input_data[0, data2.columns.get_loc('desemp_ingles_A2')] = True if ingles== 'A2' else False
        input_data[0, data2.columns.get_loc('desemp_ingles_B+')] = True if ingles == 'B+' else False
        input_data[0, data2.columns.get_loc('desemp_ingles_B1')] = True if ingles== 'B1' else False
        
        #semestre
        input_data[0, data2.columns.get_loc('semestre_1')] = True if semestre== 'S1' else False
        input_data[0, data2.columns.get_loc('semestre_2')] = True if semestre== 'S2' else False
        input_data[0, data2.columns.get_loc('semestre_4')] = True if semestre== 'S4' else False
        
        
        input_data[0, data2.columns.get_loc('cole_cod_dane_establecimiento_encoded')] =  est
        input_data[0, data2.columns.get_loc('cole_cod_dane_sede_encoded')] =  sede
        input_data[0, data2.columns.get_loc('cole_cod_mcpio_ubicacion_encoded')] =  ubic
        input_data[0, data2.columns.get_loc('estu_cod_mcpio_presentacion_encoded')] =  pres
        input_data[0, data2.columns.get_loc('estu_cod_reside_mcpio_encoded')] =  res
        input_data[0, data2.columns.get_loc('año')] =  anio
        input_data[0, data2.columns.get_loc('año_nacimiento')] =  nac
        
        
        
        scaler = StandardScaler()

        # Fit the scaler to your data (compute mean and standard deviation)
        scaler.fit(input_data)

        # Scale the input_data
        scaled_input_data = scaler.transform(input_data)

        # Realizar la predicción
        prediction = model.predict(scaled_input_data)

        # Devuelve el resultado de la predicción
        return f'Predicción: {prediction[0]}'
    else:
        return "Presiona el botón para hacer una predicción"





if __name__ == '__main__':
    app.run_server(debug=True)