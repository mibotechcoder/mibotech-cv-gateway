# import os
# import dash
# from dash import html, dcc, Input, Output, State
# import dash_bootstrap_components as dbc

# # Läs in variabler från Render Environment
# PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
# GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = dbc.Container(
#     [
#         html.H1("Mibotech AI CV Gateway", className="title"),
#         html.Hr(),
#         html.Div(
#             [
#                 html.P("🎤 Prata med mitt CV – exklusiv åtkomst för rekryterare", className="subtitle"),
#                 dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord", className="input-field"),
#                 dbc.Button("Logga in", id="login-btn", color="primary", className="login-btn"),
#                 html.Div(id="login-message", className="login-message"),
#                 html.Div(id="redirect-div"),
#                 html.Div(
#                     [
#                         html.P("Saknar du lösenord?", className="info-text"),
#                         html.A("Kontakta mig via e-post", href="mailto:michael.bohman@pm.me", className="email-link")
#                     ]
#                 ),
#             ],
#             className="login-container"
#         ),
#     ],
#     fluid=True,
# )

# MESSAGE = "🤖 Welcome, human recruiter. Mibotech AI systems are now online."

# @app.callback(
#     Output("login-message", "children"),
#     Input("login-btn", "n_clicks"),
#     State("pwd-input", "value"),
#     prevent_initial_call=True
# )
# def check_password(n_clicks, pwd):
#     if pwd == PASSWORD:
#         return html.Div([
#             html.Div(id="ai-message", className="terminal-text"),
#             dcc.Interval(id="typewriter", interval=50, n_intervals=0)
#         ])
#     else:
#         return "❌ Fel lösenord. Försök igen."


# @app.callback(
#     Output("ai-message", "children"),
#     Output("redirect-div", "children"),
#     Output("typewriter", "disabled"),
#     Input("typewriter", "n_intervals")
# )
# def typewriter_effect(n):
#     if n < len(MESSAGE):
#         return MESSAGE[:n+1], "", False
#     else:
#         return MESSAGE, dcc.Location(href=GPT_LINK), True
    
# server = app.server

# if __name__ == "__main__":
#     # app.run(debug=True)
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=False)

import os
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")

MESSAGE = "🤖 Welcome, human recruiter. Mibotech AI systems are now online."

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.Div(
                [
                    html.H1("Mibotech AI CV Gateway", className="title", style={"textAlign": "center"}),
                    html.Hr(),
                    html.Div(
                        [
                            html.P("🎤 Prata med mitt CV – exklusiv åtkomst för rekryterare", className="subtitle"),
                            dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord", className="input-field", style={"marginBottom": "10px"}),
                            dbc.Button("Logga in", id="login-btn", color="primary", className="login-btn", style={"width": "100%"}),
                            html.Div(id="login-message", className="login-message", style={"marginTop": "15px"}),
                            html.Div(id="redirect-script"),
                            html.Div(
                                [
                                    html.P("Saknar du lösenord?", className="info-text"),
                                    html.A("Kontakta mig via e-post", href="mailto:michael.bohman@pm.me", className="email-link")
                                ],
                                style={"marginTop": "10px", "textAlign": "center"}
                            ),
                        ],
                        className="login-container",
                        style={"maxWidth": "350px", "margin": "0 auto"}
                    ),
                ]
            ),
            width=12
        ),
        justify="center"
    ),
    fluid=True,
)

@app.callback(
    Output("login-message", "children"),
    Output("redirect-script", "children"),
    Input("login-btn", "n_clicks"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def check_password(n_clicks, pwd):
    if pwd == PASSWORD:
        return html.Div([
            html.Div(MESSAGE, className="terminal-typing")
        ]), html.Script(f"""
            setTimeout(function() {{
                var box = document.getElementById('login-box');
                if (box) {{
                    box.classList.add('fade-out');
                }}
            }}, 4000);
            setTimeout(function() {{
                window.location.href('{GPT_LINK}');
            }}, 4700);
        """)
    else:
        return "❌ Fel lösenord. Försök igen.", ""

server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=False)

