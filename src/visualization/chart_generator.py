import mplfinance as mpf
import pandas as pd
from pathlib import Path

class ChartGenerator:
    def __init__(self):
        self.style = mpf.make_mpf_style(base_mpf_style='charles')
    
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