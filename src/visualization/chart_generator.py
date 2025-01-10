import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.font_manager as fm

class ChartGenerator:
    def __init__(self):
        self.style = mpf.make_mpf_style(base_mpf_style='charles')
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # MacOS 的中文字体
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
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