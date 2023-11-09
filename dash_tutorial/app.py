import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc



app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP,])

app.layout = html.Div([
    html.Div([
        html.Div(
            # dcc.Link(href='/page3')
        )
    ]),
    html.Link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"  # Use the appropriate version
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
    
    
    