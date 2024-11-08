import pandas as pd
import requests
import os


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

    def get_stock(self, symbol):
        url = f"https://www.alphavantage.co/query?function={self._data_function}&symbol={symbol}&apikey={self._api_key}&outputsize=full"
        try:
            data = requests.get(url).json()
            df = pd.DataFrame(data["Time Series (Daily)"]).transpose().astype(float)        # eftersom vi har en daily tidsserie skulle vi kunna använda TTL cache för att slippa hämta data från API:et varje gång
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


class StockDataLocal:
    """Class with methods to get and process data from local files.
    """

    def __init__(self, data_folder="Data"):
        """
        Args:
            data_folder: Path to folder with data files
        """
        self._data_folder = data_folder

    def get_dataframe(self, stockname):
        stock_df = []
        for path_ending in ["_TIME_SERIES_DAILY_ADJUSTED.csv", 
                     "_TIME_SERIES_INTRADAY_EXTENDED.csv"]:
            path = os.path.join(self._data_folder, stockname + path_ending)
            stock = pd.read_csv(path, index_col=0, parse_dates=True)
            stock.index.rename("Data", inplace=True)
            stock_df.append(stock)
        return stock_df
    
        
def run_test():
    api_key = os.getenv("ALPHA_API_KEY")
    test = StockDataAPI(api_key)
    print(f"Result: {test.get_stock("AAPL")}")


if __name__ == "__main__":
    run_test()