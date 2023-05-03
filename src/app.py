import dash
from dash import dcc
from dash import html
app = dash.Dash(__name__, use_pages=True)
server = app.server
app.config.suppress_callback_exceptions=True


app.layout = html.Div([
html.Div([
    html.Div(
        html.Img(src='assets/logo_BATMAJA.png', className='center-image', style={
                'width': '20%',
            }),
        className='left-div'
    ),
    html.A(
    html.Div(
        html.Img(src='assets/logo_cuvalley.png', className='right-top-image', style={
                'width': '70%',
        }),
        className='right-top-div'
    ), href='https://cuvalley.com/stworzenie-systemu-automatycznej-estymacji-poziomu-wody-w-rzece/')
], style={"display":"flex"}),
    html.Br(),
    html.H2([html.Span('R',style={'color':'#fcb040', 'font-size':'4rem'}),'iver ',
             html.Span('E',style={'color':'#fcb040','font-size':'4rem'}),'stimator'],
            style={'text-align': 'center', 'color': 'white', 'font-family':'Jua, sans-serif','font-weight': 'bold'}),


    html.Div(
        [
            html.Div([
                dcc.Link(
                    html.Button(f"{page['name']}", style={"margin-right":"1%", "margin-left":"1%", 'color':'white',
        'border-width':'2.5px'}), href=page["path"],
                )
                for page in dash.page_registry.values()]
            )
        ], style={'textAlign': 'center'}
    ),

	dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)