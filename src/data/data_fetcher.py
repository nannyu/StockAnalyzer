import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.cache = {}  # 简单的内存缓存

    def fetch_stock_data(self, stock_code: str, years: int = 10) -> pd.DataFrame:
        """
        从Yahoo Finance获取股票历史数据
        
        Args:
            stock_code: 股票代码
            years: 获取年数，默认10年
            
        Returns:
            DataFrame包含OHLCV数据
        """
        try:
            # 添加市场后缀检查
            if not ('.' in stock_code):
                # 对于中国股票自动添加市场后缀
                if stock_code.startswith('6'):
                    stock_code = f"{stock_code}.SS"
                elif stock_code.startswith('0') or stock_code.startswith('3'):
                    stock_code = f"{stock_code}.SZ"
                
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            
            # 检查缓存
            cache_key = f"{stock_code}_{start_date.date()}_{end_date.date()}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # 获取数据
            stock = yf.Ticker(stock_code)
            df = stock.history(start=start_date, end=end_date)
            
            # 存入缓存
            self.cache[cache_key] = df
            
            return df
            
        except Exception as e:
            raise Exception(f"获取股票数据失败: {str(e)}") 