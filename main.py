import os
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")
MESSAGE = "🤖 Welcome, human recruiter. Mibotech AI systems are now online."

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Mibotech AI CV Gateway", className="title"),
                html.Hr(),
                html.P("🎤 Prata med mitt CV – exklusiv åtkomst för rekryterare", className="subtitle"),
                dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord", className="input-field"),
                dbc.Button("Logga in", id="login-btn", color="primary", style={"width": "100%", "marginTop": "10px"}),
                html.Div(id="login-message", style={"marginTop": "15px"}),
                html.Div(id="redirect-div")
            ],
            className="login-container",
            id="login-box"
        )
    ],
    className="center-screen"
)

@app.callback(
    Output("login-message", "children"),
    Output("redirect-div", "children"),
    Input("login-btn", "n_clicks"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def check_password(n_clicks, pwd):
    if pwd == PASSWORD:
        return html.Div([
            html.Div(id="ai-message", className="terminal-text"),
            dcc.Interval(id="typewriter", interval=50, n_intervals=0),
            dcc.Interval(id="redirect-timer", interval=3500, n_intervals=0, max_intervals=1)
        ]), ""
    else:
        return html.Div("❌ Fel lösenord. Försök igen.", style={"color": "red"}), ""

@app.callback(
    Output("ai-message", "children"),
    Input("typewriter", "n_intervals"),
    prevent_initial_call=True
)
def typewriter_effect(n):
    return MESSAGE[:n]

@app.callback(
    Output("redirect-div", "children"),
    Input("redirect-timer", "n_intervals"),
    prevent_initial_call=True
)
def trigger_redirect(n):
    if n:
        return dcc.Location(href=GPT_LINK)
    return ""

server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=False)
