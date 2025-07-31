import os
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")

# PASSWORD = "test"
# GPT_LINK = "https://my-gpt-lnk"

MESSAGE = "🤖 Welcome, human recruiter. Mibotech AI systems are now online."
TYPING_INTERVAL = 30  # ms per tecken
REDIRECT_DELAY = len(MESSAGE) * TYPING_INTERVAL + 100  # Dynamisk tid

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# region Layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Mibotech AI CV Gateway", className="title"),
                html.Hr(),
                html.P("🎤 Prata med mitt CV – exklusiv åtkomst för rekryterare", className="subtitle"),
                
                dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord"),
                dbc.Button("Logga in", id="login-btn", color="primary", style={"width": "100%", "marginTop": "10px"}),
                html.Div(id="ai-message", className="terminal-text"),
                html.Div(id="login-message", style={"marginTop": "15px"}),
                html.Div(id="redirect-div"),

                # Intervals i layout från start (inaktiva)
                dcc.Interval(id="typewriter", interval=TYPING_INTERVAL, n_intervals=0, disabled=True),
                dcc.Interval(id="redirect-timer", interval=REDIRECT_DELAY, n_intervals=0, max_intervals=1)
            ],
            className="login-container",
        )
    ],
    className="center-screen"
)
# endregion

# region Login-callback
@app.callback(
    Output("login-message", "children"),
    Output("typewriter", "disabled"),
    Output("redirect-timer", "disabled"),
    Output("typewriter", "n_intervals"),
    Output("redirect-timer", "n_intervals"),
    Input("login-btn", "n_clicks"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def check_password(n_clicks, pwd):
    if pwd and pwd == PASSWORD:
        return html.Div(id="ai-message", className="terminal-text"), False, False, 0, 0
    else:
        return html.Div("❌ Fel lösenord. Försök igen.", style={"color": "red"}), True, True, 0, 0
# endregion

# region Ticker-callback
@app.callback(
    Output("ai-message", "children"),
    Input("typewriter", "n_intervals"),
    prevent_initial_call=True
)
def typewriter_effect(n):
    return MESSAGE[:n]
# endregion

#region Redirect-callback
@app.callback(
    Output("redirect-div", "children"),
    Input("redirect-timer", "n_intervals"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def trigger_redirect(n, access_granted):
    if n and access_granted:
        return dcc.Location(id="redirect-location", href=GPT_LINK, refresh=True)
    return ""
# endregion

server = app.server

if __name__ == "__main__":
    # RUN kommando för Render
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=False)
    # RUN kommando för lokat
    # app.run(debug=True)
    #app.run_server(debug=True, port=8051) # Vid användning av debugger
