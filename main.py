from src.data.data_fetcher import StockDataFetcher
from src.data.data_processor import DataProcessor
from src.analysis.calculator import ReturnCalculator
from src.visualization.chart_generator import ChartGenerator
import os

class StockAnalyzer:
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.data_processor = DataProcessor()
        self.calculator = ReturnCalculator()
        self.chart_generator = ChartGenerator()
    
    def analyze_stock(self, stock_code: str):
        """
        分析指定的股票
        
        Args:
            stock_code: 股票代码
        """
        try:
            # 1. 获取数据
            print(f"正在获取股票 {stock_code} 的数据...")
            df = self.data_fetcher.fetch_stock_data(stock_code)
            
            # 2. 处理数据
            df = self.data_processor.clean_data(df)
            
            # 3. 计算年平均回报率
            annual_return = self.calculator.calculate_annual_return(df)
            print(f"年平均回报率: {annual_return:.2%}")
            
            # 4. 生成并显示K线图
            save_path = f"charts/{stock_code}_chart.png"
            os.makedirs("charts", exist_ok=True)
            self.chart_generator.generate_candlestick_chart(
                df, 
                save_path,
                warn_too_much_data=len(df) + 1000  # 添加参数避免警告
            )
            print(f"K线图已保存至: {save_path}")
            
        except Exception as e:
            print(f"分析过程中出现错误: {str(e)}")

def main():
    analyzer = StockAnalyzer()
    
    while True:
        stock_code = input("请输入股票代码（按Q退出）: ")
        if stock_code.upper() == 'Q':
            break
            
        analyzer.analyze_stock(stock_code)

if __name__ == "__main__":
    main() 