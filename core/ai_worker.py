from PyQt5.QtCore import QThread, pyqtSignal

class AIWorker(QThread):
    result = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, query, df):
        super().__init__()
        self.query=query
        self.df=df

    def run(self):
        try:
            res=self.df.chat(self.query)
            self.result.emit(res)
        except Exception as e:
            self.error.emit(str(e))

class DataInspector:
    '''数据分析'''
    @staticmethod
    def analyze(df):

        import pandas as pd

        if not isinstance(df,pd.DataFrame):
            df=df.to_pandas()

        return {
            "rows":len(df),
            "columns":len(df.columns),
            "missing":float(df.isna().mean().mean()),
            "duplicates":int(df.duplicated().sum()),
            "numeric_cols":list(df.select_dtypes("number").columns),
            "categorical_cols":list(df.select_dtypes("object").columns)
        }


class ChartRecommender:
    '''推荐图表'''
    @staticmethod
    def recommend(df):

        import pandas as pd
        if not isinstance(df,pd.DataFrame):
            df=df.to_pandas()

        num=len(df.select_dtypes("number").columns)
        cat=len(df.select_dtypes("object").columns)

        if num>=2:
            return "散点图","检测到多个数值列，适合相关性分析"

        if num==1 and cat>=1:
            return "柱状图","分类 vs 数值数据"

        if num==1:
            return "直方图","单变量分布"

        return "表格","数据结构不适合绘图"
    
#论文模式
def apply_paper_style():

    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.dpi":600,
        "font.family":"serif",
        "axes.linewidth":1.2,
        "lines.linewidth":2,
        "legend.frameon":False
    })
