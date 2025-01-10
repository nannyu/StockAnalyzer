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
            
        return df 