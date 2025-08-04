import os
import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

PASSWORD = os.environ.get("CV_BOT_PASSWORD", "defaultpassword")
GPT_LINK = os.environ.get("GPT_LINK", "https://my-gpt-lnk")

# PASSWORD = "test"
# GPT_LINK = "https://my-gpt-lnk"

MESSAGE = "🤖 Welcome, human recruiter. Mibotech AI systems are now online."
TYPING_INTERVAL = 50  # ms per tecken
REDIRECT_DELAY = len(MESSAGE) * TYPING_INTERVAL + 3000  # Dynamisk tid

# Läs in AI-info-texten från fil
with open("ai_popup_info.txt", encoding="utf-8") as f:
    AI_INFO_TEXT = f.read()

app = Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
    ]
)

# region Layout
app.layout = html.Div(
    [
        # Popup ruta med information och varning
        html.Div(
            [
                html.I(className="bi bi-question-circle-fill",  # Bootstrap-ikon
                       id="help-icon",
                       style={"fontSize": "2.5rem", "color": "#4074B2", "cursor": "pointer"})
            ],
            style={"position": "absolute", "top": "30px", "right": "30px", "zIndex": 10}
        ),

        # Popup/modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Viktigt om AI-svar")),
                dbc.ModalBody(AI_INFO_TEXT),
                dbc.ModalFooter(
                    dbc.Button("Stäng", id="close-help", className="ms-auto", n_clicks=0)
                ),
            ],
            id="help-modal",
            is_open=False,
            size="lg"
        ),


        # Wrapper för centrerad layout Infor-ruta
        html.Div(  
            [
                # Login-
                html.Div(  
                    [
                        html.H1("Mibotech AI CV Gateway", className="title"),
                        html.Hr(),
                        html.P([
                            "🎤 Chatta med mitt CV!",
                            html.Br(),
                            "Välkommen du som jobbar med rekrytering, HR eller som samarbetspartner."
                        ], className="subtitle"),   
                        dbc.Input(id="pwd-input", type="password", placeholder="Ange lösenord"),
                        dbc.Button("Logga in", id="login-btn", color="primary", style={"width": "100%", "marginTop": "10px"}),
                        html.Div(
                            html.Span(MESSAGE),
                            id="ai-message",
                            className="terminal-text",
                            style={"display": "none"}
                        ),
                        html.Div(id="login-message", style={"marginTop": "15px"}),
                        html.Div(id="redirect-div"),
                        html.Span([
                            "Är du en nyfiken samarbetspartner eller arbetar inom HR och rekrytering men saknar inloggning? ",
                            html.Br(),
                            html.A("Skicka ett InMail på LinkedIn", 
                                href="https://www.linkedin.com/in/michaelbohman71/",
                                target="_blank",
                                className="inmail-link")
                        ]),
                        dcc.Interval(id="typewriter", interval=TYPING_INTERVAL, n_intervals=0, disabled=True),
                        dcc.Interval(id="redirect-timer", interval=REDIRECT_DELAY, n_intervals=0, max_intervals=1)
                    ],
                    className="login-container"
                )
            ],
            className="center-screen"
        )
    ]
)
# endregion

# region popup
@app.callback(
    Output("help-modal", "is_open"),
    [Input("help-icon", "n_clicks"), Input("close-help", "n_clicks")],
    [dash.dependencies.State("help-modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
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
        ]), True, dash.no_update, dash.no_update, "", {"display": "none"}
# endregion

# region Ticker-callback
@app.callback(
    Output("ai-message", "style",allow_duplicate=True),
    Input("typewriter", "n_intervals"),
    prevent_initial_call=True
)
def typewriter_effect(n):
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
# def trigger_redirect(n, pwd): #" Används vid lokal körning"
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
