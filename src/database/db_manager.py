import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, Dict

class DatabaseManager:
    def __init__(self, db_path: str = "stock_data.db"):
        """
        初始化数据库管理器
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """创建必要的数据表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建股票数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_data (
                    date TEXT,
                    stock_code TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume REAL,
                    update_time TEXT,
                    PRIMARY KEY (date, stock_code)
                )
            ''')
            
            # 创建投资组合表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    create_time TEXT,
                    description TEXT
                )
            ''')
            
            # 创建投资组合成分表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolio_components (
                    portfolio_id INTEGER,
                    stock_code TEXT,
                    weight REAL,
                    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id),
                    PRIMARY KEY (portfolio_id, stock_code)
                )
            ''')
            
            conn.commit()
    
    def save_stock_data(self, stock_code: str, df: pd.DataFrame):
        """
        保存股票数据到数据库
        
        Args:
            stock_code: 股票代码
            df: 股票数据DataFrame
        """
        with sqlite3.connect(self.db_path) as conn:
            # 准备数据
            df = df.reset_index()
            df['stock_code'] = stock_code
            df['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 写入数据库
            df.to_sql('stock_data', conn, if_exists='replace', index=False)
    
    def get_stock_data(self, stock_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        从数据库获取股票数据
        
        Args:
            stock_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            股票数据DataFrame，如果没有数据则返回None
        """
        query = '''
            SELECT date, open, high, low, close, volume
            FROM stock_data
            WHERE stock_code = ? AND date BETWEEN ? AND ?
            ORDER BY date
        '''
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(stock_code, start_date, end_date))
            if len(df) > 0:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                return df
        return None
    
    def save_portfolio(self, name: str, components: Dict[str, float], description: str = ""):
        """
        保存投资组合到数据库
        
        Args:
            name: 投资组合名称
            components: 字典，键为股票代码，值为权重
            description: 投资组合描述
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 保存投资组合基本信息
            cursor.execute('''
                INSERT INTO portfolios (name, create_time, description)
                VALUES (?, ?, ?)
            ''', (name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), description))
            
            portfolio_id = cursor.lastrowid
            
            # 保存投资组合成分
            for stock_code, weight in components.items():
                cursor.execute('''
                    INSERT INTO portfolio_components (portfolio_id, stock_code, weight)
                    VALUES (?, ?, ?)
                ''', (portfolio_id, stock_code, weight))
            
            conn.commit()
    
    def get_portfolio(self, portfolio_id: int) -> Optional[Dict]:
        """
        获取投资组合信息
        
        Args:
            portfolio_id: 投资组合ID
            
        Returns:
            包含投资组合信息的字典
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 获取基本信息
            cursor.execute('''
                SELECT name, create_time, description
                FROM portfolios
                WHERE id = ?
            ''', (portfolio_id,))
            
            portfolio_info = cursor.fetchone()
            if not portfolio_info:
                return None
            
            # 获取成分股信息
            cursor.execute('''
                SELECT stock_code, weight
                FROM portfolio_components
                WHERE portfolio_id = ?
            ''', (portfolio_id,))
            
            components = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                'id': portfolio_id,
                'name': portfolio_info[0],
                'create_time': portfolio_info[1],
                'description': portfolio_info[2],
                'components': components
            } 