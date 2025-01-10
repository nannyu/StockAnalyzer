from src.data.data_fetcher import StockDataFetcher
from src.data.data_processor import DataProcessor
from src.analysis.calculator import ReturnCalculator
from src.analysis.portfolio_analyzer import PortfolioAnalyzer
from src.visualization.chart_generator import ChartGenerator
import os
from typing import Dict

class StockAnalyzer:
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.data_processor = DataProcessor()
        self.calculator = ReturnCalculator()
        self.portfolio_analyzer = PortfolioAnalyzer()
        self.chart_generator = ChartGenerator()
    
    def analyze_portfolio(self, portfolio_str: str):
        """
        分析投资组合
        
        Args:
            portfolio_str: 格式如 "AAPL:0.4,GOOGL:0.6" 的字符串
        """
        try:
            # 解析投资组合
            portfolio = self.portfolio_analyzer.parse_portfolio_input(portfolio_str)
            
            # 存储每只股票的分析结果
            stock_data = {}
            returns = {}
            volatilities = {}
            drawdowns = {}
            
            # 分析每只股票
            for stock_code in portfolio:
                print(f"\n分析股票 {stock_code}...")
                
                # 1. 获取数据
                df = self.data_fetcher.fetch_stock_data(stock_code)
                df = self.data_processor.clean_data(df)
                stock_data[stock_code] = df
                
                # 2. 计算回报率
                total_return, annual_return = self.calculator.calculate_returns(df)
                returns[stock_code] = total_return
                
                # 3. 计算风险指标
                volatilities[stock_code] = self.portfolio_analyzer.calculate_volatility(df)
                drawdowns[stock_code] = self.portfolio_analyzer.calculate_max_drawdown(df)
                
                # 4. 输出个股分析结果
                print(f"股票 {stock_code} 分析结果:")
                print(f"总回报率: {total_return:.2%}")
                print(f"年化回报率: {annual_return:.2%}")
                print(f"年化波动率: {volatilities[stock_code]:.2%}")
                print(f"最大回撤: {drawdowns[stock_code]:.2%}")
            
            # 计算投资组合整体回报率
            portfolio_return = self.portfolio_analyzer.calculate_portfolio_return(
                returns, portfolio
            )
            
            # 生成并保存投资组合走势图
            save_path = "charts/portfolio_chart.png"
            os.makedirs("charts", exist_ok=True)
            self.chart_generator.generate_portfolio_chart(
                stock_data,
                portfolio,
                save_path
            )
            print(f"\n投资组合走势图已保存至: {save_path}")
            
            # 输出投资组合分析结果
            print("\n投资组合整体分析结果:")
            print(f"总回报率: {portfolio_return:.2%}")
            print(f"年化回报率: {((1 + portfolio_return) ** (1/10) - 1):.2%}")
            
        except Exception as e:
            print(f"分析过程中出现错误: {str(e)}")

def main():
    analyzer = StockAnalyzer()
    
    while True:
        portfolio_str = input("请输入投资组合（格式如 AAPL:0.4,GOOGL:0.6）（按Q退出）: ")
        if portfolio_str.upper() == 'Q':
            break
            
        analyzer.analyze_portfolio(portfolio_str)

if __name__ == "__main__":
    main() 