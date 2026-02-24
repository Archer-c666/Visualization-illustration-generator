import os
import pandas as pd
import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt

import pandasai as pai
from pandasai import DataFrame
from pandasai_litellm.litellm import LiteLLM

from core import chart_templates
from core.ai_worker import AIWorker
from core.config import *
from UI.styles import MAIN_STYLE


TEMPLATES=[
    "自动(AI)",
    "柱状图",
    "折线图",
    "散点图",
    "饼图",
    "热力图",
    "箱线图",
    "回归图",
    "误差棒",
    "双Y轴"
]

class PlotCanvas(Canvas):
    def __init__(self):
        from matplotlib.figure import Figure
        self.fig=Figure(dpi=120)
        self.ax=self.fig.add_subplot(111)
        super().__init__(self.fig)

        self._pan=False
        self._last=None

    def show_img(self,img):
        self.ax.clear()
        self.ax.imshow(img)
        self.ax.axis("off")
        self.draw()

    # 滚轮缩放
    def wheelEvent(self,event):
        factor=1.2 if event.angleDelta().y()>0 else 0.8
        xlim=self.ax.get_xlim()
        ylim=self.ax.get_ylim()
        self.ax.set_xlim([x*factor for x in xlim])
        self.ax.set_ylim([y*factor for y in ylim])
        self.draw()

    # 拖动
    def mousePressEvent(self,event):
        if event.button()==1:
            self._pan=True
            self._last=event.pos()

    def mouseMoveEvent(self,event):
        if self._pan and self._last:
            dx=event.x()-self._last.x()
            dy=event.y()-self._last.y()

            xlim=self.ax.get_xlim()
            ylim=self.ax.get_ylim()

            self.ax.set_xlim(xlim[0]-dx,xlim[1]-dx)
            self.ax.set_ylim(ylim[0]+dy,ylim[1]+dy)

            self._last=event.pos()
            self.draw()

    def mouseReleaseEvent(self,event):
        self._pan=False

    # 双击重置
    def mouseDoubleClickEvent(self,event):
        self.ax.autoscale()
        self.draw()


class DataAnalysisWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("AI Data Lab 🧪")
            self.resize(1300,750)
            self.df=None

            llm=LiteLLM(model=LLM_MODEL,api_key=OPENAI_API_KEY)
            pai.config.set({
                "llm": llm,
                "save_charts": False
            })
            pai.api_key.set(OPENAI_API_KEY)   # ← 必须加上

            self.setStyleSheet(MAIN_STYLE)
            self.build_ui()

        def build_ui(self):
            root=QWidget(); self.setCentralWidget(root)
            layout=QHBoxLayout(root)

            # left
            left=QVBoxLayout()

            self.chat=QTextEdit(); self.chat.setReadOnly(True)
            self.input=QLineEdit()
            send=QPushButton("发送 ✨")
            send.clicked.connect(self.ask)

            load=QPushButton("加载数据 📂")
            load.clicked.connect(self.load)

            left.addWidget(load)
            # 模板选择
            self.template_box=QComboBox()
            self.template_box.addItems(TEMPLATES)
            left.addWidget(self.template_box)

            # 字体选择器
            self.font_box=QComboBox()
            self.font_box.addItems([
                "Times New Roman",
                "Arial",
                "Calibri",
                "SimHei",
                "SimSun",
                "Microsoft YaHei"
            ])
            self.font_box.currentTextChanged.connect(self.change_font)
            left.addWidget(self.font_box)

            # 主题选择器
            self.theme_box=QComboBox()
            self.theme_box.addItems(["Default","Dark","Nature","IEEE"])
            self.theme_box.currentTextChanged.connect(self.change_theme)
            left.addWidget(self.theme_box)

            left.addWidget(self.chat)
            left.addWidget(self.input)
            left.addWidget(send)

            # right
            right=QVBoxLayout()
            self.canvas=PlotCanvas()

            zoom=QPushButton("🔍 查看细节")
            zoom.clicked.connect(self.zoom_chart)

            export=QPushButton("💾 导出")
            export.clicked.connect(self.save)

            right.addWidget(self.canvas)
            right.addWidget(zoom)
            right.addWidget(export)

            layout.addLayout(left,3)
            layout.addLayout(right,5)

        def load(self):
            path,_=QFileDialog.getOpenFileName(self,"open","","CSV (*.csv);;Excel (*.xlsx)")
            if not path:return
            df=pd.read_csv(path) if path.endswith("csv") else pd.read_excel(path)
            self.df=DataFrame(df)
            self.chat.append(f"✅ 已加载 {os.path.basename(path)}")

        def ask(self):
            if self.df is None:
                self.chat.append("❌ 请先加载数据")
                return
            q=self.input.text().strip()
            if not q:return
            self.chat.append("🧑 "+q)
            self.input.clear()

            self.worker=AIWorker(q,self.df)
            self.worker.result.connect(self.handle)
            self.worker.error.connect(lambda e:self.chat.append("❌ "+e))
            self.worker.start()

        def handle(self,res):
            import re, base64
            from PIL import Image
            import io
            from pandasai.core.response import ChartResponse,StringResponse

            template=self.template_box.currentText()

            # ---------- 如果用户选模板 ----------
            if template!="自动(AI)" and self.df is not None:

                import pandas as pd
                if isinstance(self.df,pd.DataFrame):
                    df=self.df
                else:
                    df=self.df.to_pandas()

                try:
                    if template=="柱状图":
                        fig=chart_templates.bar(df,df.columns[0],df.columns[1])
                    elif template=="折线图":
                        fig=chart_templates.line(df,df.columns[0],df.columns[1])
                    elif template=="散点图":
                        fig=chart_templates.scatter(df,df.columns[0],df.columns[1])
                    elif template=="饼图":
                        fig=chart_templates.pie(df,df.columns[0],df.columns[1])
                    elif template=="热力图":
                        fig=chart_templates.heatmap(df)
                    elif template=="箱线图":
                        fig=chart_templates.boxplot(df,df.columns[0])
                    elif template=="回归图":
                        fig=chart_templates.regression(df,df.columns[0],df.columns[1])
                    elif template=="误差棒":
                        fig=chart_templates.errorbar(df,df.columns[0],df.columns[1])
                    elif template=="双Y轴":
                        fig=chart_templates.double_axis(df,df.columns[0],df.columns[1],df.columns[2])
                    else:
                        raise Exception("未知模板")

                    self.canvas.show_img(fig.canvas.buffer_rgba())
                    self.chat.append(f"📊 已使用模板：{template}")
                    return

                except Exception as e:
                    self.chat.append(f"模板绘图失败：{e}")
            if isinstance(res, ChartResponse):
                img = res._get_image()
                self.canvas.show_img(img)

                import matplotlib.pyplot as plt
                plt.close("all")
                self.chat.append("🤖 图表生成完毕")

            elif isinstance(res, StringResponse):

                text = res.value

                # 🔍 检测base64图片
                match = re.search(r"base64,(.*?)\"", text)

                if match:
                    img_data = base64.b64decode(match.group(1))
                    img = Image.open(io.BytesIO(img_data))
                    self.canvas.show_img(img)
                    plt.close("all")
                    self.chat.append("🤖 已解析AI生成图像")
                else:
                    self.chat.append("🤖 "+text)

            else:
                self.chat.append("🤖 "+str(res))

        def zoom_chart(self):
            dlg=QDialog(self)
            dlg.setWindowTitle("图像预览")
            lay=QVBoxLayout(dlg)
            big=PlotCanvas()
            big.ax.imshow(self.canvas.fig.canvas.buffer_rgba())
            big.ax.axis("off")
            lay.addWidget(big)
            dlg.resize(800,600)
            dlg.exec_()

        def change_font(self,font):
            import matplotlib.pyplot as plt
            plt.rcParams["font.sans-serif"]=[font]
            self.chat.append(f"🎨 字体已切换 → {font}")

        def change_theme(self,theme):
            import matplotlib.pyplot as plt

            themes={
                "Default":{},
                "Dark":{
                    "axes.facecolor":"#222",
                    "figure.facecolor":"#222",
                    "text.color":"white",
                    "axes.labelcolor":"white",
                    "xtick.color":"white",
                    "ytick.color":"white"
                },
                "Nature":{
                    "axes.grid":True,
                    "grid.alpha":0.3,
                    "axes.linewidth":1.2
                },
                "IEEE":{
                    "axes.grid":True,
                    "grid.linestyle":"--",
                    "lines.linewidth":2
                }
            }

            for k,v in themes[theme].items():
                plt.rcParams[k]=v

            self.chat.append(f"🎨 主题已切换 → {theme}")

        def save(self):
            path,_=QFileDialog.getSaveFileName(self,"save","chart.png","PNG (*.png)")
            if path:
                self.canvas.fig.savefig(path,dpi=300,bbox_inches="tight")