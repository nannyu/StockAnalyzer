import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.font_manager as fm
from typing import Dict
import os

class ChartGenerator:
    def __init__(self):
        self.style = mpf.make_mpf_style(base_mpf_style='charles')
        # 根据操作系统设置合适的中文字体
        if os.name == 'nt':  # Windows
            plt.rcParams['font.sans-serif'] = ['SimHei']
        elif os.name == 'posix':  # macOS/Linux
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_candlestick_chart(self, 
                                 df: pd.DataFrame, 
                                 save_path: str = None) -> None:
        """
        生成K线图
        
        Args:
            df: 股票数据DataFrame
            save_path: 图表保存路径
        """
        try:
            # 添加更多样式设置
            kwargs = dict(
                type='candle',
                volume=True,
                title='股票K线图',
                style=self.style,
                figsize=(15, 10),
                panel_ratios=(6,2),  # 主图与成交量图的比例
                datetime_format='%Y-%m-%d'
            )
            
            if save_path:
                # 保存到文件
                mpf.plot(df, savefig=save_path, **kwargs)
            else:
                # 显示图表
                mpf.plot(df, **kwargs)
                
        except Exception as e:
            raise Exception(f"生成K线图失败: {str(e)}")
            
    def generate_line_chart(self, df: pd.DataFrame, save_path: str = None, title: str = "股价走势图") -> None:
        """
        生成线图
        
        Args:
            df: 股票数据DataFrame
            save_path: 图表保存路径
            title: 图表标题
        """
        try:
            plt.figure(figsize=(15, 10))
            plt.plot(df.index, df['close'], label='收盘价')
            plt.title(title)
            plt.xlabel('日期')
            plt.ylabel('价格')
            plt.grid(True)
            plt.legend()
            
            if save_path:
                plt.savefig(save_path)
                plt.close()
            else:
                plt.show()
                
        except Exception as e:
            raise Exception(f"生成线图失败: {str(e)}") 

    def generate_portfolio_chart(self, 
                               stock_data: dict, 
                               portfolio: dict,
                               save_path: str = None,
                               ax = None):
        """
        生成投资组合走势图
        
        Args:
            stock_data: 字典，键为股票代码，值为该股票的DataFrame
            portfolio: 字典，键为股票代码，值为权重
            save_path: 图表保存路径
            ax: matplotlib的Axes对象，如果提供则在其上绘图
        """
        try:
            if ax is None:
                fig, ax = plt.subplots(figsize=(12, 6))
            
            # 计算每只股票的归一化价格
            for stock_code, df in stock_data.items():
                # 归一化价格（设第一天为100）
                normalized_price = df['close'] / df['close'].iloc[0] * 100
                ax.plot(df.index, normalized_price, 
                       label=f'{stock_code} ({portfolio[stock_code]*100:.0f}%)')
            
            # 设置图表属性
            ax.set_title('投资组合走势图（起始值=100）', fontsize=12)
            ax.set_xlabel('日期')
            ax.set_ylabel('价格（归一化）')
            ax.grid(True)
            ax.legend()
            
            # 旋转日期标签以防重叠
            plt.setp(ax.get_xticklabels(), rotation=45)
            
            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                plt.close()
            
        except Exception as e:
            raise Exception(f"生成投资组合走势图失败: {str(e)}") 