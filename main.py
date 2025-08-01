import os
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")

# PASSWORD = "test"
# GPT_LINK = "https://my-gpt-lnk"

MESSAGE = "🤖 Welcome, human recruiter. Mibotech AI systems are now online."
TYPING_INTERVAL = 50  # ms per tecken
REDIRECT_DELAY = len(MESSAGE) * TYPING_INTERVAL + 400  # Dynamisk tid

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# region Layout
app.layout = html.Div(
    [
        html.Div(  # Login-rutan
            [
                html.H1("Mibotech AI CV Gateway", className="title"),
                html.Hr(),
                html.P("🎤 Prata med mitt CV – exklusiv åtkomst för rekryterare och samarbetspartners", className="subtitle"),
                
                dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord"),
                dbc.Button("Logga in", id="login-btn", color="primary", style={"width": "100%", "marginTop": "10px"}),
                html.Div(
                    html.Span(MESSAGE),  # hela texten direkt
                    id="ai-message",
                    className="terminal-text",
                    style={"display": "none"}
                ),
                html.Div(id="login-message", style={"marginTop": "15px"}),
                html.Div(id="redirect-div"),

                # Intervals i layout från start (inaktiva)
                dcc.Interval(id="typewriter", interval=TYPING_INTERVAL, n_intervals=0, disabled=True),
                dcc.Interval(id="redirect-timer", interval=REDIRECT_DELAY, n_intervals=0, max_intervals=1)
            ],
            className="login-container",
        ),

        html.Div(  # Info-rutan
            [
                html.Small(
                    [
                        "Är du en nyfiken samarbetspartner eller arbetar inom HR och rekrytering men saknar inloggning? ",
                        html.A("Skicka ett InMail på LinkedIn", 
                               href="https://www.linkedin.com/in/michaelbohman71/",
                               target="_blank",
                               style={"color": "#0A66C2", "textDecoration": "none", "fontWeight": "bold"})
                    ],
                    className="info-text"
                )
            ],
            style={"marginTop": "10px", "padding": "8px"}
        )
    ],
    className="center-screen"
)
# endregion

# region Login-callback
@app.callback(

    Output("login-message", "children"),
    Output("redirect-timer", "disabled"),
    Output("typewriter", "n_intervals"),
    Output("redirect-timer", "n_intervals"),
    Output("pwd-input", "value"),
    Output("ai-message", "style"),
    Input("login-btn", "n_clicks"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def check_password(n_clicks, pwd):
#    print(f"DEBUG: Login n_clicks={n_clicks}, pwd={pwd}")
    if pwd and pwd == PASSWORD:
        return "", False, 0, 0, pwd, {"display": "block"}
    else:
        focus_script = html.Script("""
        setTimeout(function(){
            document.getElementById('pwd-input').focus();
        }, 50);
        """)
        return html.Div([
            html.Div("❌ Fel lösenord. Försök igen.", style={"color": "red"}),
            focus_script
        ]), True, 0, 0, "", {"display": "none"}
# endregion

# region Ticker-callback
@app.callback(
    Output("ai-message", "style"),
    Input("typewriter", "n_intervals"),
    prevent_initial_call=True
)
def typewriter_effect(n):
    # print(f"DEBUG: Typewriter n_intervals={n} / len={len(MESSAGE)}")
    return {"display": "block"}  # Bara visa tickern, CSS gör rullningen
# endregion

#region Redirect-callback
@app.callback(
    Output("redirect-div", "children"),
    Input("redirect-timer", "n_intervals"),
    State("pwd-input", "value"),
    prevent_initial_call=True
)
def trigger_redirect(n, access_granted): # Används av Render
# def trigger_redirect(n, pwd): " Används vid lokal körning"
    # print(f"DEBUG: Redirect timer n_intervals={n}, pwd={pwd}")
    if n and access_granted: # Används av Render
    # if n and pwd == PASSWORD: # Används vid lokal körning
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
