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