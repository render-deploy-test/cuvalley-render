import dash
from dash import html, dcc,callback, Input, Output
from assets.plots import DataAnalysis
import plotly.graph_objs as go
dash.register_page(__name__, path='/', order=0)

da = DataAnalysis()
da.load_hydro_data(path = 'data/')
da.load_corr_stations()
figure_1 = da.line_plot("Stan poziomu wody w stacjach Głogów i Racibórz-Miedonia")
figure_2 = da.corr_stations()
figure_3 = da.corr_stations_2()
drop_style = {'background-color': '#fcb040', 'textAlign': 'center', 'margin': 'auto', 'color':'black'}
water_level_cols = ['GŁOGÓW (151160060) Stan wody [cm]','RACIBÓRZ-MIEDONIA (150180060) Stan wody [cm]']
hydro_cols = ['GŁOGÓW','RACIBÓRZ-MIEDONIA']
meteo_cols=da.df_corr.druga_stacja.unique()
meteo_cols = meteo_cols[:len(meteo_cols)-2]
drop_station = dcc.Dropdown(id='drop-1',
                            options=[{"label":i.split(")")[0]+')', "value":i} for i in water_level_cols],
                            placeholder='Wybierz stację do analizy', className='dropdown',multi=False,
                            style=drop_style
                            )
drop_hydro = dcc.Dropdown(id='drop-2',
                            options=[{"label":i, "value":i} for i in hydro_cols],
                            placeholder='Wybierz stację hydrologiczną do analizy', className='dropdown',multi=False,
                            style=drop_style
                            )
drop_meteo = dcc.Dropdown(id='drop-3',
                            options=[{"label":i.split(")")[0]+')', "value":i} for i in meteo_cols],
                            placeholder='Wybierz stację meteorologiczną do analizy', className='dropdown',multi=False,
                            style=drop_style
                            )


layout = html.Div([
# tytul

    html.Div([
    html.Br(),
    dcc.Tabs(
        id='tabs-1',
        children=[
            dcc.Tab(label='Porównanie poziomów pomiędzy stacjami', value='tab-1',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Korelacja oddziaływania pomiędzy stacjami', value='tab-2',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Korelacja oddziaływania pomiędzy stacjami,a opadami', value='tab-3',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"})
        ],
        value='tab-1',
    colors={
        "border":"#b3b3b3", #obwodka
        "background":'white', #tlo
        'primary':'#035891' #jesli wybrane

    },
),
    html.Div(id='div-1')
])])

@callback(
    Output('div-1', 'children'),
    [Input('tabs-1', 'value')]
)
def render_content(tab):
    if tab=='tab-1':
        return html.Div([
            html.Br(),
            drop_station,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id='graph-1',figure=figure_1),

            ],
                className='add_container twelve columns'
            )

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id = 'graph-2',figure=figure_2),

            ],
                className='add_container twelve columns'
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Br(),
            drop_hydro,
            html.Br(),
            drop_meteo,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id ='graph-3',figure=figure_3),

            ],
                className='add_container twelve columns'
            )
        ])

@callback(
        [Output('graph-1', 'figure')
         ],
        [Input('drop-1', 'value')]
)
def update_graph(drop):
    fig_1 = da.line_plot("Stan poziomu wody w stacjach Głogów i Racibórz-Miedonia")
    if drop is not None:
        trace1 = go.Scatter(x=da.hydro['Data'], y=da.hydro[drop],
                            name='Stacja'.format(drop.split("(")[0]), marker_color='#035891')
        traces = [trace1]
        layout = go.Layout(title='Stan poziomu wody w stacji {0}'.format(drop.split("(")[0]),
                           xaxis=dict(title='Czas', showgrid=False, color='#035891', title_font={"size": 20}),
                           yaxis=dict(title='Poziom wody', showgrid=False, title_font={"size": 20}, color='#035891'))
        fig_1 = go.Figure(data=traces, layout=layout)
        fig_1.layout.height = 600
        fig_1.layout.width = 1200
        fig_1.update_layout(title_font={'size': 30}, title_x=0.5, font_family="Lato, sans-serif",
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)')
    return [fig_1]

@callback(
        [
        Output('graph-3', 'figure')
         ],
        [
        Input('drop-2', 'value'),
        Input('drop-3', 'value')]
)
def update_graph(drop_1,drop_2):
    pierwsza_stacja = 'GŁOGÓW'
    druga_stacja = 'RACIBÓRZ (350180540) Suma opadów [mm]'
    if drop_1 is not None:
        pierwsza_stacja = drop_1
    if drop_2 is not None:
        druga_stacja = drop_2
    fig_2 = da.corr_stations_2(pierwsza_stacja=pierwsza_stacja,druga_stacja=druga_stacja)
    return [fig_2]
