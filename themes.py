# テーマごとのCSS
LIGHT_THEME = """
QWidget{
    background: #f5f5f5;
    color: #222;
}

QLineEdit, QTextEdit{
    background: white;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 6px;
}

QPushButton{
    background: #e0e0e0;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
}

QPushButton:hover{
    background: #d0d0d0;
}

QFrame#card{
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    background: white;
}

QFrame#card:hover{
    background: #f5f5f5;    
}

QLabel#code{
    background: #f8f8f8;
    color: #333;
    padding: 6px;
    border-radius: 4px;    
}
"""

DARK_THEME = """
QWidget{
    background: #282c34;
    color: #abb2bf;
}

QLineEdit{
    background: #21252b;
    color: #abb2bf;
    border: 1px solid #3e4451;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 14px;
    min-height: 22px;
}

QTextEdit{
    background: #21252b;
    color: #abb2bf;
    border: 1px solid #3e4451;
    border-radius: 6px;
    padding: 8px;
    font-size: 14px;
}

QPushButton{
    background: #3e4451;
    color: #abb2bf;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}

QPushButton:hover{
    background: #4b5263;
}

QFrame#card{
    border: 1px solid #3e4451;
    border-radius: 10px;
    padding: 10px;
    background: #3a3f4b;
}

QFrame#card:hover{
    background: #434957;
}

QLabel#code{
    background: #21252b;
    color: #abb2bf;
    padding: 6px;
    border-radius: 4px;
}
"""