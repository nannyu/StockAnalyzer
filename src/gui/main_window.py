import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.data.data_fetcher import StockDataFetcher
from src.analysis.calculator import ReturnCalculator
from src.analysis.portfolio_analyzer import PortfolioAnalyzer
from src.visualization.chart_generator import ChartGenerator
import os

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("股票投资组合分析系统")
        self.window.geometry("1400x900")
        
        # 初始化组件
        self.data_fetcher = StockDataFetcher()
        self.calculator = ReturnCalculator()
        self.portfolio_analyzer = PortfolioAnalyzer()
        self.chart_generator = ChartGenerator()
        
        self._init_ui()
        
    def _init_ui(self):
        """初始化用户界面"""
        # 创建左右分栏
        left_frame = ttk.Frame(self.window, padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        right_frame = ttk.Frame(self.window, padding="10")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 左侧输入区域
        self._init_input_area(left_frame)
        
        # 右侧图表和结果显示区域
        self._init_display_area(right_frame)
        
    def _init_input_area(self, parent):
        """初始化输入区域"""
        # 投资组合输入
        ttk.Label(parent, text="投资组合配置").pack(anchor=tk.W)
        ttk.Label(parent, text="格式：代码1:权重1,代码2:权重2").pack(anchor=tk.W)
        
        self.portfolio_input = ttk.Entry(parent, width=30)
        self.portfolio_input.pack(pady=5)
        
        # 分析按钮
        ttk.Button(parent, text="分析投资组合", 
                  command=self._analyze_portfolio).pack(pady=10)
        
        # 结果文本区域
        ttk.Label(parent, text="分析结果").pack(anchor=tk.W, pady=(10,0))
        self.result_text = tk.Text(parent, width=40, height=20)
        self.result_text.pack(pady=5)
        
    def _init_display_area(self, parent):
        """初始化显示区域"""
        # 创建图表区域
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def _analyze_portfolio(self):
        """分析投资组合"""
        try:
            # 清空之前的结果
            self.result_text.delete(1.0, tk.END)
            self.ax.clear()
            
            # 解析投资组合
            portfolio_str = self.portfolio_input.get().strip()
            portfolio = self.portfolio_analyzer.parse_portfolio_input(portfolio_str)
            
            # 存储分析结果
            stock_data = {}
            returns = {}
            volatilities = {}
            drawdowns = {}
            
            # 分析每只股票
            for stock_code in portfolio:
                self.result_text.insert(tk.END, f"\n分析股票 {stock_code}...\n")
                self.result_text.see(tk.END)
                
                # 获取数据
                df = self.data_fetcher.fetch_stock_data(stock_code)
                df = df.copy()  # 创建副本以避免修改原始数据
                stock_data[stock_code] = df
                
                # 计算指标
                total_return, annual_return = self.calculator.calculate_returns(df)
                returns[stock_code] = total_return
                volatilities[stock_code] = self.portfolio_analyzer.calculate_volatility(df)
                drawdowns[stock_code] = self.portfolio_analyzer.calculate_max_drawdown(df)
                
                # 显示结果
                self.result_text.insert(tk.END, 
                    f"总回报率: {total_return:.2%}\n"
                    f"年化回报率: {annual_return:.2%}\n"
                    f"年化波动率: {volatilities[stock_code]:.2%}\n"
                    f"最大回撤: {drawdowns[stock_code]:.2%}\n"
                )
            
            # 计算组合回报率
            portfolio_return = self.portfolio_analyzer.calculate_portfolio_return(
                returns, portfolio
            )
            
            # 显示组合结果
            self.result_text.insert(tk.END, 
                f"\n投资组合整体分析结果:\n"
                f"总回报率: {portfolio_return:.2%}\n"
                f"年化回报率: {((1 + portfolio_return) ** (1/10) - 1):.2%}\n"
            )
            
            # 绘制图表
            self.chart_generator.generate_portfolio_chart(
                stock_data=stock_data,
                portfolio=portfolio,
                ax=self.ax
            )
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def run(self):
        """运行主窗口"""
        self.window.mainloop() 