import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback


""" PLOTLY_LOGO is a object from s3 bucket."""
PLOTLY_LOGO = "https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png"

dash.register_page(
    __name__,
    path="/dashboard",
    name="dashboard",
)

''' modal for show pop-up when press the profile icon on nav.'''

modal = html.Div(
    [
        dbc.Button(html.I(className="fas fa-user"), id="open", n_clicks=0, color="link"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,

        ),
    ]
)
""" nav_iteam can be used for mention links on header parts. """
nav_item = dbc.NavItem([dbc.NavLink("Sign out", href="#")])

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("manageAccount", href='/manageAccount'),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

""" main layout of dashboard"""
navbar = html.Div(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        href="https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [dropdown, nav_item, modal],
                            className="ms-auto",
                            navbar=True,
                        ),
                        id="navbar-collapse2",
                        navbar=True,
                    ),
                ],
            ),
            color="dark",
            dark=True,
        ),
        dcc.Location(id="url"),  # Add the URL location component
    ],
)

''' slide bar header is atteched on slidebar '''
sidebar = html.Div(
    dbc.Nav(
        [
            html.H1('sidebar'),
            html.H2('fadg'),
        ],
        vertical=True,
        pills=True,
        className="bg-light"
    )
)

content = html.Div(id="page-content")

layout = html.Div(
    children=[
        html.Div(children=[navbar], className="child",),
        html.Div(
            children=[
                html.Div([sidebar], className="sidebar-div"),
                html.Div([content], className="child content"),
            ],
            className="main",
        ),
        html.Div("footer", className="child"),
    ],
    className="parent",
)

@callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



