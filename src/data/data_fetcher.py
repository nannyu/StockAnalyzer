import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from src.database.db_manager import DatabaseManager

class StockDataFetcher:
    def __init__(self):
        """初始化数据获取器，设置数据库管理器"""
        self.db_manager = DatabaseManager()
        
    def _format_stock_code(self, stock_code: str) -> str:
        """
        格式化股票代码
        
        Args:
            stock_code: 原始股票代码
            
        Returns:
            格式化后的股票代码
        """
        # 移除空格
        stock_code = stock_code.strip().upper()
        
        # 如果没有后缀，根据股票代码添加
        if '.' not in stock_code:
            if stock_code.startswith('6'):
                stock_code = f"{stock_code}.SS"  # 上海证券交易所
            elif stock_code.startswith(('0', '3')):
                stock_code = f"{stock_code}.SZ"  # 深圳证券交易所
                
        return stock_code

    def fetch_stock_data(self, stock_code: str, years: int = 10) -> pd.DataFrame:
        """
        获取股票历史数据，优先从本地数据库获取，如果没有则从Yahoo Finance获取
        
        Args:
            stock_code: 股票代码
            years: 获取年数，默认10年
            
        Returns:
            DataFrame包含OHLCV数据
        """
        try:
            # 格式化股票代码
            formatted_code = self._format_stock_code(stock_code)
            
            # 计算日期范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            
            # 尝试从数据库获取数据
            df = self.db_manager.get_stock_data(
                formatted_code, 
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
            
            if df is None or len(df) == 0:
                print(f"从Yahoo Finance获取股票 {formatted_code} 的数据...")
                # 从Yahoo Finance获取数据
                stock = yf.Ticker(formatted_code)
                df = stock.history(start=start_date, end=end_date)
                
                if df is not None and len(df) > 0:
                    # 保存到数据库
                    self.db_manager.save_stock_data(formatted_code, df)
                else:
                    raise Exception("无法获取股票数据")
            else:
                print(f"从本地数据库获取股票 {formatted_code} 的数据...")
            
            return df
            
        except Exception as e:
            raise Exception(f"获取股票数据失败: {str(e)}")
            
    def update_stock_data(self, stock_code: str):
        """
        更新指定股票的数据
        
        Args:
            stock_code: 股票代码
        """
        try:
            # 获取最新的完整数据
            df = self.fetch_stock_data(stock_code)
            
            # 保存到数据库
            formatted_code = self._format_stock_code(stock_code)
            self.db_manager.save_stock_data(formatted_code, df)
            
            print(f"股票 {formatted_code} 数据已更新")
            
        except Exception as e:
            print(f"更新股票数据失败: {str(e)}") 