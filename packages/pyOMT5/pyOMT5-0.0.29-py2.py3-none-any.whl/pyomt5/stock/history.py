import time
import logging
import pandas as pd
from datetime import datetime, timedelta
from pyomt5.api import MT5TimeFrame
from pyomt5.api import MetatraderCom, ConnectionTimeoutError, DataNotFoundError

log = logging.getLogger("pyomt5")


class StockPriceHistory():
    def __init__(self, use_cache=False, **kw):
        self.use_cache = use_cache
        self.price_cache = dict()

        self.number_of_retry = 1
        if kw.get('retry'):
            self.number_of_retry = kw.get('retry')

        self.request_timeout = 1.5
        if kw.get('timeout'):
            self.request_timeout = kw.get('timeout')

        self.mt_timeout = 500
        if kw.get('mt_timeout'):
            self.mt_timeout = kw.get('mt_timeout')

    def _convert_to_dataframe(self, data):
        df = pd.DataFrame.from_dict(data)

        df.close = pd.to_numeric(df.close)
        df.open = pd.to_numeric(df.open)
        df.low = pd.to_numeric(df.low)
        df.high = pd.to_numeric(df.high)
        df.volume = pd.to_numeric(df.volume)
        df.date = pd.to_datetime(df.date,
                                 format='%Y.%m.%d %H:%M',
                                 errors='ignore')

        return df

    def _prepare_data(self, symbol, data):
        df = self._convert_to_dataframe(data)

        df['symbol'] = symbol

        return df.reset_index().\
            sort_values(by=["symbol", "date"],
                        ascending=True).set_index(["symbol", "date"]).\
            drop(columns=["index"])

    def get_price_from(self, symbol: str, from_date: datetime,
                       to_date: datetime, timeframe: MT5TimeFrame) -> list:
        """ Get prices from history data and return it 
            in a pandas DataFrame format
            Args:
                symbol (str): symbol of stock
                timeframe (MT5TimeFrame): interval between each price-time
                periods: amount of data that'll be returned
            Returns:
                list: a list with all data in the OHLC format 
                Ex:
                                    close   high    low   open     volume
                symbol date
                PETR4  2018-09-20    19.18  19.64  19.07  19.56   56002300
                       2018-09-21    19.44  19.60  19.26  19.45   58278000
        """
        end_date = to_date
        start_date = from_date

        c = MetatraderCom(timeout=self.mt_timeout)
        nRetry = 0
        price_history = None
        while nRetry < self.number_of_retry:
            try:

                if self.use_cache and (symbol in self.price_cache):
                    log.debug(f"Getting data for {symbol} [using cache]")
                    price_history = self.price_cache[symbol]
                    break

                log.debug(f"Getting data for {symbol}")
                price_history = c.get_historical(symbol, timeframe.value,
                                                 start_date, end_date)

                self.price_cache[symbol] = price_history
                break

            except ConnectionTimeoutError:
                nRetry += 1
                log.debug(
                    f"Connection Failed. Waiting for reconnection.. Retry #{nRetry}"
                )
                time.sleep(self.request_timeout)

        if not price_history:
            raise DataNotFoundError()

        return self._prepare_data(symbol, price_history)
