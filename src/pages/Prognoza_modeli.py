import dash
from dash import html, dcc,callback, Input, Output
from assets.plots import MLModels
dash.register_page(__name__, order=2)

ml = MLModels()
ml.load_data()
figure_1 = ml.model_forecast_plot()
figure_2 = ml.model_forecast_plot(model='Bayesian Ridge')
drop_style = {'background-color': '#fcb040', 'textAlign': 'center', 'margin': 'auto', 'color':'black'
              }
station_cols = ['GŁOGÓW (151160060) Stan wody [cm]','RACIBÓRZ-MIEDONIA (150180060) Stan wody [cm]']
drop_station = dcc.Dropdown(id='drop-6',
                            options=[{"label":i, "value":i} for i in station_cols],
                            placeholder='Wybierz stację do analizy', className='dropdown',multi=False,
                            style=drop_style)
layout = html.Div(
html.Div([
html.Br(),
dcc.Tabs(
        id='tabs-3',
        children=[
            dcc.Tab(label='Baseline', value='tab-1',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
            dcc.Tab(label='Bayesian Ridge', value='tab-2',style = {'color':'black'},selected_style ={"background":'#fcb040',"border":"#b3b3b3"}),
        ],
        value='tab-1',
    colors={
        "border":"#b3b3b3", #obwodka
        "background":'white', #tlo
        'primary':'#035891' #jesli wybrane

    },
),
html.Div(id='div-3')
])
)

@callback(
    Output('div-3', 'children'),
    [Input('tabs-3', 'value')]
)
def render_content(tab):
    if tab=='tab-1':
        return html.Div([
            html.Br(),
            drop_station,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id = 'graph-5',figure=figure_1),

            ],
                className='add_container twelve columns'
            )

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Br(),
            drop_station,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id = 'graph-5',figure=figure_2),

            ],
                className='add_container twelve columns'
            )

        ])
@callback(
        [Output('graph-5', 'figure'),
         ],
        [Input('drop-6', 'value'),
        Input('tabs-3', 'value')]
)
def update_graph(drop,tab):
    target_to_viz='GŁOGÓW (151160060) Stan wody [cm]'
    model='Baseline'
    if tab == 'tab-1':
        model='Baseline'
    elif tab == 'tab-2':
        model = 'Bayesian Ridge'
    if drop is not None:
        target_to_viz = drop
    figure = ml.model_forecast_plot(model=model, target_to_viz=target_to_viz)
    return [figure]
