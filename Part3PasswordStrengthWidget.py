class PasswordStrengthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.bars = [QLabel(self) for _ in range(4)]
        for bar in self.bars:
            bar.setFixedSize(20, 20)
            bar.setStyleSheet("background-color: lightgray; border-radius: 10px;")
            self.layout.addWidget(bar)
        self.strength_label = QLabel(self)
        self.layout.addWidget(self.strength_label)
        self.setLayout(self.layout)

    def set_strength(self, strength, strength_name):
        colors = ["red", "yellow", "green", "green"]
        for i in range(4):
            if i < strength:
                self.bars[i].setStyleSheet(f"background-color: {colors[strength - 1]}; border-radius: 10px;")
            else:
                self.bars[i].setStyleSheet("background-color: lightgray; border-radius: 10px;")
        self.strength_label.setText(strength_name)


        
