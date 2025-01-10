import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class PortfolioAnalyzer:
    @staticmethod
    def parse_portfolio_input(input_str: str) -> Dict[str, float]:
        """
        解析用户输入的投资组合字符串
        
        Args:
            input_str: 格式如 "AAPL:0.4,GOOGL:0.6" 的字符串
            
        Returns:
            字典 {股票代码: 占比}
        """
        portfolio = {}
        try:
            for item in input_str.split(','):
                if ':' in item:
                    code, weight = item.strip().split(':')
                    portfolio[code.strip()] = float(weight)
                else:
                    # 如果没有指定权重，默认平均分配
                    portfolio[item.strip()] = 0
            
            # 如果有默认权重0的股票，平均分配剩余权重
            assigned_weight = sum(w for w in portfolio.values() if w > 0)
            remaining_weight = 1.0 - assigned_weight
            default_stocks = [k for k, v in portfolio.items() if v == 0]
            
            if default_stocks:
                weight_per_stock = remaining_weight / len(default_stocks)
                for stock in default_stocks:
                    portfolio[stock] = weight_per_stock
                    
            return portfolio
            
        except Exception as e:
            raise ValueError(f"投资组合格式错误: {str(e)}")
    
    @staticmethod
    def calculate_portfolio_return(returns: Dict[str, float], weights: Dict[str, float]) -> float:
        """
        计算投资组合总回报率
        
        Args:
            returns: 每只股票的回报率
            weights: 每只股票的权重
            
        Returns:
            投资组合总回报率
        """
        total_return = 0
        for stock_code in returns:
            if stock_code in weights:
                total_return += returns[stock_code] * weights[stock_code]
        return total_return
    
    @staticmethod
    def calculate_volatility(df: pd.DataFrame) -> float:
        """
        计算股票的年化波动率
        
        Args:
            df: 股票历史数据DataFrame
            
        Returns:
            年化波动率
        """
        # 计算日收益率
        daily_returns = df['close'].pct_change().dropna()
        
        # 计算年化波动率（假设一年252个交易日）
        annual_volatility = daily_returns.std() * np.sqrt(252)
        
        return annual_volatility
    
    @staticmethod
    def calculate_max_drawdown(df: pd.DataFrame) -> float:
        """
        计算最大回撤
        
        Args:
            df: 股票历史数据DataFrame
            
        Returns:
            最大回撤比例
        """
        prices = df['close']
        peak = prices.expanding(min_periods=1).max()
        drawdown = (prices - peak) / peak
        max_drawdown = drawdown.min()
        
        return max_drawdown 