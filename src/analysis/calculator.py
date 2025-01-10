import pandas as pd
import numpy as np
from typing import Dict, Tuple

class ReturnCalculator:
    @staticmethod
    def calculate_returns(df: pd.DataFrame) -> Tuple[float, float]:
        """
        计算总回报率和年化回报率
        
        Args:
            df: 股票历史数据DataFrame
            
        Returns:
            (总回报率, 年化回报率)
        """
        try:
            # 确保列名都是小写
            df.columns = df.columns.str.lower()
            
            initial_price = df['close'].iloc[0]
            final_price = df['close'].iloc[-1]
            
            # 计算总回报率
            total_return = (final_price / initial_price) - 1
            
            # 计算年化收益率
            years = len(df) / 252  # 假设每年约252个交易日
            annual_return = (1 + total_return) ** (1/years) - 1
            
            return total_return, annual_return
            
        except Exception as e:
            raise Exception(f"计算回报率失败: {str(e)}") 