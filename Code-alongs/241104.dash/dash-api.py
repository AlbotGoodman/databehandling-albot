import os
from load_data import StockDataAPI
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly_express as px

api_key = os.getenv('ALPHA_API_KEY')
stock_data = StockDataAPI(api_key)
stock_dict = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla"}
stock_options = [{"label": name, "value": symbol} for symbol, name in stock_dict.items()]    # items hämtar både nycklar och värden

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Viewer"),
    html.P("Choose a stock:"),
    dcc.Dropdown(id="stock-picker-dropdown", className="", options=stock_options,
                 value="AAPL", placeholder="Apple"),
    dcc.Graph(id="stock_graph")
])

@app.callback(
    Output("stock_graph", "figure"),
    Input("stock-picker-dropdown", "value")
)
def update_graph(stock):
    df = stock_data.get_stock_data(stock)
    fig = px.line(df, df.index, "Close", title=f"Stock price for {stock_dict[stock]}", labels={"index": "Date"}, title=stock)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)