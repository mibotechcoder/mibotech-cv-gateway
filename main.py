import os
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Läs in variabler från Render Environment
PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Mibotech AI CV Gateway", className="title"),
        html.Hr(),
        html.Div(
            [
                html.P("🎤 Prata med mitt CV – exklusiv åtkomst för rekryterare", className="subtitle"),
                dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord", className="input-field"),
                dbc.Button("Logga in", id="login-btn", color="primary", className="login-btn"),
                html.Div(id="login-message", className="login-message"),
                html.Div(
                    [
                        html.P("Saknar du lösenord?", className="info-text"),
                        html.A("Kontakta mig via e-post", href="mailto:michael.bohman@pm.me", className="email-link")
                    ]
                ),
            ],
            className="login-container"
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("login-message", "children"),
    Input("login-btn", "n_clicks"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def check_password(n_clicks, pwd):
    if pwd == PASSWORD:
        return dcc.Location(href=GPT_LINK, id="redirect")
    else:
        return "❌ Fel lösenord. Försök igen."

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
