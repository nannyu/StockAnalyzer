import pandas as pd
import numpy as np

class DataProcessor:
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        清理和预处理股票数据
        
        Args:
            df: 原始股票数据DataFrame
            
        Returns:
            清理后的DataFrame
        """
        # 删除空值
        df = df.dropna()
        
        # 确保所有必需的列都存在
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("数据缺少必需的列")
        
        # 统一列名为小写
        df.columns = df.columns.str.lower()
            
        return df
    
    @staticmethod
    def resample_monthly(df: pd.DataFrame) -> pd.DataFrame:
        """
        将数据按月重采样
        
        Args:
            df: 原始数据框，日期应该是索引
        Returns:
            按月重采样后的数据框
        """
        # 按月重采样并聚合数据
        monthly_df = df.resample('ME').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        return monthly_df 