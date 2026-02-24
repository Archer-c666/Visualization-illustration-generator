MAIN_STYLE = """
QMainWindow {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
    stop:0 #fdfbfb, stop:1 #ebedee);
}

QFrame{
    background:white;
    border-radius:15px;
}

QPushButton{
    background:#6ec6ff;
    border:none;
    border-radius:12px;
    padding:8px 18px;
    color:white;
    font-weight:bold;
}
QPushButton:hover{
    background:#42a5f5;
}
QPushButton:pressed{
    background:#1e88e5;
}

QLineEdit{
    border:2px solid #90caf9;
    border-radius:12px;
    padding:10px;
    background:white;
}

QTextEdit{
    border-radius:12px;
    padding:12px;
    background:#fafcff;
}
"""