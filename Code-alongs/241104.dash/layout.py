import dash_bootstrap_components as dbc
from dash import html, dcc

class Layout:
    def __init__(self, symbol_dict):
        self._symbol_dict = symbol_dict
        self.stock_options_dropdown = [
            {"label": name, "Value": symbol}
            for symbol, name in self._symbol_dict.items()
            ]
        self.ohlc_options = [
            {"label": option.capitalize(), "value": option}
            for option in ["open", "high", "low", "close"]
            ]
        self.slider_marks = {
            i: mark
            for i, mark in enumerate(["1 day", "1 week", "3 months", "1 year", "5 years", "MAX"])
        }
    
    def layout(self):
        return dbc.Container(
            [
                dbc.Card(
                    [
                        html.H1(
                            "Stocks viewer",
                            className="card-title text-dark mx-3",
                        )
                    ], 
                    className="mt-4"),
                dbc.Row(
                    className="mt-4",
                    children = [
                        dbc.Col(
                            html.P("Choose a stock"),
                            xs="12", 
                            sm="12",
                            md="6",
                            lg="4",
                            xl=3,
                            className="mt-1"
                        ),
                        dbc.Col(
                            dcc.Dropdown(id="stock-picker-dropdown", className="", 
                                         options=self.stock_options_dropdown,
                                         value="AAPL", placeholder="Apple"),
                                         xs="12", 
                            sm="12",
                            md="6",
                            lg="4",
                            xl=3,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dcc.RadioItems(
                                            id="ohlc-radio",
                                            className="mt-1",
                                            options=self.ohlc_options,
                                            value="close"
                                        )
                                    ]
                                )
                            ], 
                            xs="12",
                            sm="12",
                            md="12",
                            lg="4",
                            xl="3"
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Graph(id="stock-graph"),
                                dcc.Slider(
                                id="time-slider",
                                min=0,
                                max=5,
                                step=None,
                                value=2,
                                marks=self.slider_marks
                                )
                            ],
                            lg={"size": "6", "offset": 1},
                            xl={"size": "6", "offset": 1}
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Card(
                                            [
                                                html.H2("Highest value", 
                                                        className="h5 mt-3 mx-3"),
                                                        html.P(
                                                            id="highest-value",
                                                            className="text-success h1 mx-2"
                                                        )
                                            ]
                                        )
                                    ]                       # fick fel med indentering så gav upp i slutet
                                )
                            ]
                        )
                    ]
                )
            ]
        )