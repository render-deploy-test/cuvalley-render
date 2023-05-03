import dash
from dash import html, dcc,callback, Input, Output
from assets.plots import MLModels
import re

dash.register_page(__name__, order=1)

ml = MLModels()
ml.load_data()
figure_1 = ml.model_evaluation_plot()
figure_2 = ml.model_evaluation_plot(model='Bayesian Ridge')
dataframe = ml.models_historical_forecasts
dataframe_2 = ml.dataset

drop_style = { 'background-color': '#fcb040','textAlign': 'center', 'margin': 'auto', 'color':'black'}
station_cols = ml.models_historical_forecasts['Stacja'].unique()
horizon_cols = ml.models_historical_forecasts.columns.drop(labels=['Data','Model','Stacja','Zmienne'])
drop_station = dcc.Dropdown(id='drop-4',
                            options=[{"label":i, "value":i} for i in station_cols],
                            placeholder='Wybierz stację do analizy', className='dropdown',multi=False,
                            style=drop_style
                            )
drop_horizon = dcc.Dropdown(id='drop-5',
                            options=[{"label":i, "value":i} for i in horizon_cols],
                            placeholder='Wybierz horyzont czasowy do analizy', className='dropdown',multi=False,
                            style=drop_style
                            )




layout = html.Div(
html.Div([
html.Br(),
dcc.Tabs(
        id='tabs-2',
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
html.Div(id='div-2')
])
)

@callback(
    Output('div-2', 'children'),
    [Input('tabs-2', 'value')]
)
def render_content(tab):
    if tab=='tab-1':
        return html.Div([
            html.Br(),
            drop_station,
            html.Br(),
            drop_horizon,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id="graph-4",figure=figure_1),

            ],
                className='add_container twelve columns'
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Br(),
            drop_station,
            html.Br(),
            drop_horizon,
            html.Br(),
            html.Div([
                html.Br(),
                dcc.Graph(id="graph-4",figure=figure_2),

            ],
                className='add_container twelve columns'
            )

        ])
@callback(
        [Output('graph-4', 'figure'),
         ],
        [Input('drop-4', 'value'),
        Input('drop-5', 'value'),
        Input('tabs-2', 'value')]
)
def update_graph(drop,drop_2,tab):
    target_to_viz='GŁOGÓW (151160060) Stan wody [cm]'
    horizon_to_viz = 7
    model = 'Baseline'
    if tab == 'tab-1':
        model='Baseline'
    elif tab == 'tab-2':
        model = 'Bayesian Ridge'
    if drop is not None:
        target_to_viz = drop
    elif drop_2 is not None:
        horizon_to_viz = int(re.findall(r'\d+', drop_2)[0])
    figure = ml.model_evaluation_plot(model=model, target_to_viz=target_to_viz, horizon_to_viz=horizon_to_viz)
    return [figure]




