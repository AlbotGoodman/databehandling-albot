import pandas as pd
import requests

class StockDataAPI:
    """Class with methods to get and process data from Alphga Vantage.
    """

    def __init__(self, api_key, data_function = "TIME_SERIES_DAILY"):
        """
        Args:
            api_key: API key from alphavantage
        """
        self._data_function = data_function
        self._api_key = api_key

    def get_stock_data(self, symbol):
        url = f"https://www.alphavantage.co/query?function={self._data_function}&symbol={symbol}&apikey={self._api_key}&outputsize=full"
        try:
            data = requests.get(url).json()
            df = pd.DataFrame(data["Time Series (Daily)"]).transpose().astype(float)
            df.index = pd.to_datetime(df.index)
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            return df
        except KeyError as err: # detta är bara exempel eftersom jag inte har någon datafil
            import pickle                                       # sparar data i en fil på hårddisken för att inte behöva hämta data från API:et varje gång
            with open("Data/stocks.pckl", "rb") as file:
                disk_data = pickle.load(file)
            disk_data = pd.concat(disk_data, axis=1)
            data = disk_data[symbol]
            df = pd.DataFrame(data["Time Series (Daily)"]).transpose().astype(float)
            df.index = pd.to_datetime(df.index)
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            
            return df
        
def run_test():
    import os
    api_key = os.getenv("ALPHA_API_KEY")
    test = StockDataAPI(api_key)
    print(f"Result: {test.get_stock("AAPL")}")


if __name__ == "__main__":
    run_test()