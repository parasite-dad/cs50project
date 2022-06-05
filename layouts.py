from dash_bootstrap_components._components.Container import Container
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from datetime import datetime, date, timedelta
#import callbacks
# SIDEBAR_STYLE = {
# #    "position": "fixed",
# #    "top": 0,
#     "left": 0,
# #    "bottom": 0,
# #    "width": "16rem",
#     "padding": "1rem 1rem",
#     "background-color": "#f8f9fa",
# #    "background-color": "#f809fa",
# }
# SIDEBARRIGHT_STYLE = {
# #    "position": "fixed",
# #    "top": 0,
#     "right": 0,
# #    "bottom": 0,
# #    "width": "16rem",
#     "padding": "1rem 1rem",
#     "background-color": "#f8f9fa",
# #    "background-color": "#f809fa",
# }

# CONTENT_STYLE = {
#     "margin-left": "10rem",
#     "margin-right": "10rem",
#     #"padding": "2rem 1rem",
#     "padding": "1rem",
# }

# OPTIONS FOR DROPDOWN BOX
#overlap_studies=["SMA - Simple Moving Average","EMA - Exponential Moving Average","BBANDS - Bollinger Bands"]
overlap_studies=[{"label":"SMA - Simple Moving Average","value":"SMA"},{"label":"EMA - Exponential Moving Average","value":"EMA"},{"label":"BBANDS - Bollinger Bands","value":"BBANDS"}]
# momentum_indicator=["ADX - Average Directional Movement Index","DX - Directional Movement Index","MACD - Moving Average Convergence/Divergence","MOM - Momentum","RSI - Relative Strength Index","STOCH - Stochastic"]
momentum_indicator=[{"label":"ADX - Average Directional Movement Index","value":"ADX"},{"label":"DX - Directional Movement Index","value":"DX"},{"label":"MACD - Moving Average Convergence/Divergence","value":"MACD"},{"label":"MOM - Momentum","value":"MOM"},{"label":"RSI - Relative Strength Index","value":"RSI"},{"label":"STOCH - Stochastic","value":"STOCH"}]
volume_indicator=[{"label":"OBV - On Balance Volume","value":"OBV"}]
volatility_indicator=[{"label":"ATR - Average True Range","value":"ATR"}]
strategy=[{"label":"SMA Crossing","value":"SMACROSS"},{"label": "Golden Cross and Death Cross","value":"GOLDENDEATHCROSS"},{"label": "MACD Strategy","value":"MACDS"}]

#RIGHT SIDE CONTENT
sidebar_right = html.Div(
    [
        html.H3(
            "Navigate different indicator", className="fs-6 fw-bold text-left text-dark"
        ),
        html.Div([
            "Overlap Studies Functions",
            #dbc.DropdownMenu(label="Overlap Studies",children=overlap_studies,id="overlap"),
            #html.Button(id='submit-add1', n_clicks=0, children='Add')
            dcc.Dropdown(options=overlap_studies,id="overlap"),
            #dbc.Button("Add", color="primary", className="me-1",id='submit-add1',n_clicks=0),
            #BELOW MODAL POP UP IS STATIC WRITTEN

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please enter the periods",className="fs-6 fw-bold text-left text-dark")),
                    dbc.ModalBody(dcc.Input(id="overlap_input1", type="number",  style={'marginRight':'10px'})),
                    dbc.ModalFooter([
                        dcc.Store(id="overlap_modelinput1"),
                        dbc.Button(
                            "Add", id="overlap_add1", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="overlap_modal1",
                is_open=False,
                centered=True,
                size="sm",
                backdrop="static",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please enter the periods and std")),
                    dbc.ModalBody([
                        html.Div([
                            "Timeperiod",
                            dcc.Input(id="overlap_input2", type="number", style={'marginRight':'10px'}),
                        ]),
                        html.Div([
                            "Standard Derivation",
                            dcc.Input(id="overlap_input2_std", type="number", style={'marginRight':'10px'}),
                        ]),
                    ]),
                    dbc.ModalFooter([
                        dcc.Store(id="overlap_modelinput2"),
                        dbc.Button(
                            "Add", id="overlap_add2", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="overlap_modal2",
                is_open=False,
                centered=True,
                size="sm",
                backdrop="static",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please enter the fastperiod,slowperiod and signalperiod")),
                    dbc.ModalBody([
                        html.Div([
                            "Fast Period",
                            dcc.Input(id="inputnumber31", type="number", style={'marginRight':'10px'}),
                        ]),
                        html.Div([
                            "Slow Period",
                            dcc.Input(id="inputnumber32", type="number", style={'marginRight':'10px'}),
                        ]),
                        html.Div([
                            "Signal Period",
                            dcc.Input(id="inputnumber33", type="number", style={'marginRight':'10px'}),
                        ]),

                    ]),
                    dbc.ModalFooter([
                        dcc.Store(id="input_modelinput3"),
                        dbc.Button(
                            "Add", id="input_add3", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="input_modal3",
                is_open=False,
                centered=True,
                size="sm",
                backdrop="static",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please enter the Fast K,Slow K and Slow D")),
                    dbc.ModalBody([
                        html.Div([
                            "Fast K  ",
                            dcc.Input(id="inputnumber41", type="number", style={'marginRight':'10px'}),
                        ]),
                        html.Div([
                            "Slow K  ",
                            dcc.Input(id="inputnumber42", type="number", style={'marginRight':'10px'}),
                        ]),
                        html.Div([
                            "Slow D  ",
                            dcc.Input(id="inputnumber43", type="number", style={'marginRight':'10px'}),
                        ]),

                    ]),
                    dbc.ModalFooter([
                        dcc.Store(id="input_modelinput4"),
                        dbc.Button(
                            "Add", id="input_add4", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="input_modal4",
                is_open=False,
                centered=True,
                size="sm",
                backdrop="static",
            ),
        ]),
        html.Div([
            "Momentum Indicator Functions",
            dcc.Dropdown(momentum_indicator,id="momentum",clearable=False,style={'font-size':'0.05rem'}),
            #html.Button(id='submit-add2', n_clicks=0, children='Add')
            ]),
        html.Div([
            "Volume Indicator Functions",
            dcc.Dropdown(volume_indicator,id="volume"),
            #html.Button(id='submit-add3', n_clicks=0, children='Add')
            ]),
        html.Div([
            "Volatility Indicator Functions",
            dcc.Dropdown(volatility_indicator,clearable=False,id="volatility"),
            #html.Button(id='submit-add4', n_clicks=0, children='Add')
            ]),
        html.Hr(),
        html.Div([
            "Strategy Indicator",
            dcc.Dropdown(options=strategy,id="strategy",clearable=False),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please input the number of periods")),
                    #BELOW MODAL IS DYNAMICALLY GENERATE BY CALLBACKS.PY
                    dbc.ModalBody([
                        html.Div([
                            "SMA Crossing ",
                            dbc.Input(id="inputnumber51"),
                        ]),
                        html.Div([
                            "Golden Cross and Death Cross",
                            dbc.Input(id="inputnumber61"),
                            dbc.Input(id="inputnumber62"),
                        ]),
                        html.Div([
                            "MACD Stratgy",
                            dbc.Input(id="inputnumber71"),
                            dbc.Input(id="inputnumber72"),
                            dbc.Input(id="inputnumber73"),
                        ]),
                        #NO STATIC GENERATE
#                         html.Div([
#                             "SMA Crossing ",
#                             dbc.Input(id="inputnumber51", type="number", placeholder="Please enter time preiod", style={'marginRight':'10px'}),
#                         ]),
#                         html.Div([
#                             "Golden Cross and Death Cross",
#                             dbc.Input(id="inputnumber61", type="number", placeholder="Please enter SMA slow time preiod...200", style={'marginRight':'10px'}),
#                             dbc.Input(id="inputnumber62", type="number", placeholder="Please enter SMA fast time preiod...50", style={'marginRight':'10px'}),
#                         ]),
#                         html.Div([
#                             "MACD Stratgy",
#                             dbc.Input(id="inputnumber71", type="number", placeholder="Please enter Fast K...12",  style={'marginRight':'10px'}),
#                             dbc.Input(id="inputnumber72", type="number", placeholder="Please enter Slow K...26", style={'marginRight':'10px'}),
#                             dbc.Input(id="inputnumber73", type="number", placeholder="Please enter Slow D...9", style={'marginRight':'10px'}),
#                         ]),
                    ],id="strategy_content"),
                    dbc.ModalFooter([
                        dcc.Store(id="input_modelinput5"),
                        dbc.Button(
                            "Add", id="input_add5", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="input_modal5",
                is_open=False,
                centered=True,
                #size="sm",
                backdrop="static",
            ),
        ],className="d-grid gap-2 col-12 mx-auto"),
        html.Hr(),

        html.Div([
            "Indicator to remove",
            dcc.Dropdown(id="remove_indicator"),
            dbc.Button(id='submit-removal', n_clicks=0, children='Remove')
            ],className="d-grid gap-2 col-12 mx-auto"),

        html.Hr(),
        html.Div([
            "Save Current Chart",
            dbc.Button(id='submit-save', n_clicks=0, children='Save Chart'),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please enter the name of this save chart")),
                    dbc.ModalBody([
                        html.Div([
                            "Save Name",
                            dcc.Input(id="savefigure_name", type="text",placeholder="Please enter saved name", value="", style={'marginRight':'10px'},persistence=False),

                        ]),
                        html.Div([
                            "Notes",
                            #dbc.Input(id="inputnotes", placeholder="Write a notes reminder...", type="text"),
                            dcc.Textarea(id="inputnotes", placeholder="Write a notes reminder...",
                            style={'width': '100%', 'height': 200},persistence=False),
                        ]),

                    ]),
                    dbc.ModalFooter([
                        #dcc.Store(id="overlap_modelinput2"),
                        dbc.Button(
                            "Confirm Save", id="savefigure_name_save", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="Notes_modal",
                is_open=False,
                centered=True,
                size="lg",
                #backdrop="static",
            ),
            ],className="d-grid gap-2 col-12 mx-auto"),
        html.Div([
            "Load Historic Charts",
            dbc.Button(id='submit-load', n_clicks=0, children='Load Chart'),
            #BELOW TABLE IS DYNAMICALLY GENERATE
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Please search the historic charts")),
                    dbc.ModalBody([
                        #html.Div([html.H4(children='OHLC'),],id="tablerow"),
                        html.Div(id="tablerow",children=dash_table.DataTable(id="table"))

                    ]),
                    dbc.ModalFooter([
                        #dcc.Store(id="overlap_modelinput2"),
                        dbc.Button(
                            "Confirm Load", id="loadfigure_name_load", className="ms-auto", n_clicks=0
                        )
                    ]),
                ],
                id="Load_modal",
                is_open=False,
                centered=True,
                size="lg",
                scrollable=True,
                #backdrop="static",
            ),
            ],className="d-grid gap-2 col-12 mx-auto"),

        html.Div([
            "Download Chart to Html",
            dbc.Button(id="downloadChartbtn",n_clicks=0, children='Download Chart'),
            dcc.Download(id="downloadChart"),
            ],className="d-grid gap-2 col-12 mx-auto"),
    ],id="sidebar_right",
    #style=SIDEBARRIGHT_STYLE,
)

#LEFT SIDE CONTENT
sidebar = html.Div(
    [
        html.H2("Hi,today is {}".format(date.today().strftime("%b %d, %Y")), className="fs-3 fw-bold text-center text-dark",id="welcome"),
        html.H2("{}".format(date.today().strftime("%b %d, %Y")), className="fs-3 fw-bold text-center text-dark",id="time"),
        html.Div(
            [
                "Please enter valid ticker symbol",
                dbc.Input(type="search", placeholder="Search by enter ticker symbol",id="input-search"),
                dcc.Store(id="input-search-dcc"),
            ],className="d-grid gap-2 col-12 mx-auto"
        ),
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=date(2000, 1, 1),
                    max_date_allowed=date.today()-timedelta(days=1),
                    start_date_placeholder_text=date.today()-timedelta(days=365),
                    end_date_placeholder_text=date.today()-timedelta(days=1),
                    calendar_orientation='horizontal',
                    initial_visible_month=date(2021, 1, 1),
                    start_date=date.today()-timedelta(days=365),
                    end_date=date.today()-timedelta(days=1),
                    day_size=39,
                    with_portal =True,
                    className="d-grid gap-2 col-12 mx-auto"
                )
            ],
            className="d-grid gap-2 col-12 mx-auto"
            #style={"width":"50px" ,"height":"20px","font-size":""}
        ),
        html.Div(
            dbc.Button(
                "Search", color="primary",
                #className="ms-2",
                n_clicks=0, id="submit-search",className="d-grid gap-2 col-12 mx-auto"
            ),
            className="d-grid gap-2 col-12 mx-auto"
        ),
        html.Hr(),
        html.Div(
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col(html.A(html.Img(id="logo_url",src="",width='100%' ),id="website",href="https://www.amazon.com"),width=4),
                        dbc.Col([
                            html.H5(id="shortName",className="fw-bold text-center text-primary"),
                            html.H6(id="symbol",className="text-center text-primary"),

                            ],
                        ),
                        ],justify="between",align="start",
                    )
                ],fluid=True,
            ),
            #className="d-grid gap-2 col-12 mx-auto",
        ),
        html.Div(
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col(html.H1(id="currentPrice",className="fs-2 fw-bold text-center text-primary"),width=8),
                        dbc.Col(html.H5(id="diffPrice",className="fs-5 text-center text-primary"),width=4),
                        ],justify="between",align="center",
                    ),
                ])
            ),
       html.Div(
            dbc.Container(
                [
                    dcc.Loading(id="ticker_data",type="default",fullscreen=False,children=[
#SHOW FOR INDIVIUAL DATA INSTEAD OF TABLE
#                     dbc.Row([
#                         dbc.Col(html.P(children="Previous Close",className="fs-6 text-center text-secondary",style={"font-size":"5vw",'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="previousClose",className="text-center text-dark",style={'float': 'right'}),width=4),
#                         ],justify="between",align="start",
#                     ),
#                     dbc.Row([
#                         dbc.Col(html.P(children="Open",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="open",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),
#                     dbc.Row([
#                         dbc.Col(html.P(children="Day High",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="dayHigh",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),
#                     dbc.Row([
#                         dbc.Col(html.P(children="Day Low",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="dayLow",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),
#                     dbc.Row([
#                         dbc.Col(html.P(children="Volume",className="fs-6 text-center text-secondary", style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="volume1",className="text-center text-dark",style={'float': 'right'}),width=4),
#                         ],justify="between",align="start",
#                     ),
#                     dbc.Row([
#                         dbc.Col(html.P(children="Avg Volume(10d)",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=7),
#                         dbc.Col(html.H6(id="averageVolume10days",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),

#                     dbc.Row([
#                         dbc.Col(html.P(children="52 Week High",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="fiftyTwoWeekHigh",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),

#                     dbc.Row([
#                         dbc.Col(html.P(children="52 Week Low",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="fiftyTwoWeekLow",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),
#                     dbc.Row([
#                         dbc.Col(html.P(children="PE Ratio",className="fs-6 text-center text-secondary",style={'float': 'left'}),width=8),
#                         dbc.Col(html.H6(id="trailingPE",className="text-center text-dark",style={'float': 'right'})),
#                         ],justify="between",align="start",
#                     ),
                    ]

                    ), ],fluid=True,
            ),
            #className="d-grid gap-2 col-12 mx-auto",
        ),
    ],id="sidebar",
    #style=SIDEBAR_STYLE,
)

config={'scrollZoom': True,'responsive': True,'displaylogo':False}
#MIDDLE CHART CONTENT IN TAB CONSTRUCTION
content = html.Div(
    [
        dbc.Tabs([
            dbc.Tab([
                html.Div([
                    #dcc.Graph(id='stock-graph',figure=fig, config=config)
                     dcc.Loading(
                    id="loading-1",
                    type="default",
                    #fullscreen=True,
                    children=dcc.Graph(id='stock-graph',config = config,)
                ),
                ]),
            ],label="Chart",id="chart_tab"
            ),
#             dbc.Tab([
#                 #html.Div(id="strategy_tablerow",children=dash_table.DataTable(id="strategy_table"))
#                 #dbc.Table.from_dataframe(df,striped=True, bordered=True, hover=True,id="strategy_table")
#             ],label="Strategy",id="strategy_tab"
#             )
            dbc.Tab([
                html.Div(
                    [
                        dbc.Row(dbc.Col(html.Div("", id="strategyMessage",className="fs-2 fw-bold text-center text-primary"))),
                        dbc.Row(dbc.Col(html.Div("", id="strategyTable"))),
                        dbc.Row(
                            [
                                dbc.Col(html.Div("",id="strategySummary")),
                                #dbc.Col(html.Div("One of three columns")),
                            ]
                        ),
                    ]
                )
                #html.Div(id="strategy_tablerow",children=dash_table.DataTable(id="strategy_table"))
                #dbc.Table.from_dataframe(df,striped=True, bordered=True, hover=True,id="strategy_table")
            ],label="Strategy",id="strategy_tab"
            )

        ]
        )
    ],id="page-content",
    #style=CONTENT_STYLE,
)

#MODAL ERROR AND IT IS STATICALLY GENERATE
modal_error = html.Div(
    [
#        dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.Modal(
            [
                #dbc.ModalHeader(dbc.ModalTitle("Stock Not Found", id="model_title")),
                dbc.ModalHeader("Stock Not Found", id="modal_title"),
                dbc.ModalBody("We cannot find this stock symbol", id="modal_body"),
                # dbc.ModalFooter(
                #     dbc.Button(
                #         "Close", id="close", className="ms-auto", n_clicks=0
                #     )
                # ),
            ],
            id="modal_error",
            is_open=False,
        ),
    ]
)
#WHOLE LAYER
graph_layout=dbc.Row([dbc.Col([sidebar],width=2),dbc.Col([content],width=8),dbc.Col([sidebar_right],width=2),modal_error],className="g-0")

#INDEX_STRING TO DETERMINE WHETHER LOGIN OR NOT LOGIN AND IT IS HTML TEMPLATE FOR DASH APP TO RENDER AND ENTER POINT IS BELOW {%app_entry%}
index_string_login = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Mini Technical Analysis and Strategy</title>
        {%favicon%}
        {%css%}
        <meta charset="utf-8">
        <meta name="viewport" content="initial-scale=1, width=device-width">

        <!-- http://getbootstrap.com/docs/5.1/ -->
        <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" rel="stylesheet">
        <script crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"></script>

        <link href="https://cdn.jsdelivr.net/npm/shareon@1/dist/shareon.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/shareon@1/dist/shareon.min.js" type="text/javascript"></script>
</script>
        <!-- https://favicon.io/emoji-favicons/money-bag/ -->
        <link href="/static/favicon.ico" rel="icon">

        <link href="/static/styles.css" rel="stylesheet">
    </head>
    <body>
        <nav class="bg-info border navbar navbar-expand-md navbar-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="/"><img src="/static/favicon.ico"> <span class="black">Mini Technical Analysis and Strategy</span><img src="/static/favicon.ico"></a>
                <button aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbar" data-bs-toggle="collapse" type="button">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            <div style="overflow:hidden;width:40%;margin:auto;padding-top:10px">
            <H3 style="float:left;padding-top:5px"></H3>
            <!--https://shareon.js.org/-->
            <div class="shareon" style="overflow:hidden;width:600px;margin:auto;text-align:left">
                <a class="twitter"></a>
                <a class="facebook"></a>
                <!-- FB App ID is required for the Messenger button to function -->
                <!--  <a class="messenger" data-fb-app-id="0123456789012345"></a> -->
                <a class="linkedin"></a>
                <a class="reddit"></a>
                <a class="mastodon" data-text="Check this out!"></a>
                <a class="odnoklassniki"></a>
                <a class="pinterest"></a>
                <a class="pocket"></a>
                <a class="vkontakte"></a>
                <a class="viber" data-text="Check this out!"></a>
                <a class="telegram "data-text="Check this out!"></a>
                <a class="whatsapp" data-text="Check this out!"></a>
            </div>
        </div>
            <div class="collapse navbar-collapse" id="navbar">
                    <ul class="navbar-nav ms-auto mt-0">
                        <li class="nav-item"><a class="nav-link" href="/logout"><h3 id="logout">Log Out</h3></a></li>
                    </ul>
            </div>

        </nav>
        <!--<div>My Custom header</div>-->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''

index_string_logout = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Mini Technical Analysis and Strategy</title>
        {%favicon%}
        {%css%}
        <meta charset="utf-8">
        <meta name="viewport" content="initial-scale=1, width=device-width">

        <!-- http://getbootstrap.com/docs/5.1/ -->
        <link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" rel="stylesheet">
        <script crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"></script>

        <!-- https://favicon.io/emoji-favicons/money-bag/ -->
        <link href="/static/favicon.ico" rel="icon">

        <link href="/static/styles.css" rel="stylesheet">
    </head>
    <body>
        <nav class="bg-info border navbar navbar-expand-md navbar-light">
            <div class="container-fluid">
                <a class="navbar-brand" href="/"><img src="/static/favicon.ico"> <span class="black">Mini Technical Analysis and Strategy</span><img src="/static/favicon.ico"></a>
                <button aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbar" data-bs-toggle="collapse" type="button">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            <div class="collapse navbar-collapse" id="navbar">
                    <ul class="navbar-nav ms-auto mt-2">
                        <li class="nav-item"><a class="nav-link" href="/register"><h3 id="register">Register</h3></a></li>
                        <li class="nav-item"><a class="nav-link" href="/login"><h3 id="login">Log In</h3></a></li>
                    </ul>
            </div>

        </nav>
        <!--<div>My Custom header</div>-->
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''