import pandas as pd
import numpy as np

class ReturnCalculator:
    @staticmethod
    def calculate_annual_return(df: pd.DataFrame) -> float:
        """
        计算年平均回报率
        
        Args:
            df: 股票历史数据DataFrame
            
        Returns:
            年平均回报率
        """
        try:
            initial_price = df['Close'].iloc[0]
            final_price = df['Close'].iloc[-1]
            years = len(df) / 252  # 假设每年约252个交易日
            
            # 计算年化收益率：(终值/初值)^(1/年数) - 1
            annual_return = (final_price / initial_price) ** (1/years) - 1
            
            return annual_return
            
        except Exception as e:
            raise Exception(f"计算年平均回报率失败: {str(e)}") 