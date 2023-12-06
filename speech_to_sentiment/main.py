from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from textblob import TextBlob
import speech_recognition as sr

class Speech(QWidget):
    def __init__(self):
        super().__init__()
        self.recognized_text = ""
        self.settings()
        self.initUI()
        self.connects()
        
    def settings(self):
        self.setWindowTitle("Guest Speaker")
        self.setGeometry(250, 250, 300, 500)

    def initUI(self):
        title = QLabel("Guest Speaker")
        title.setFont(QFont("Myanmar MN", 35))
        self.output_label = QTextEdit("Spoken text will appear here:")
        self.sentiment_text = QLabel("Sentiment: ")
        self.sentiment_text.setObjectName("sentimentLabel")
        self.submit = QPushButton("Speak Now")
        self.save = QPushButton("Save Note")

        self.master = QVBoxLayout()
        self.master.addWidget(title, alignment=Qt.AlignCenter)
        self.master.addWidget(self.output_label, alignment=Qt.AlignCenter)
        self.master.addWidget(self.sentiment_text, alignment=Qt.AlignCenter)
        self.master.addWidget(self.submit, alignment=Qt.AlignCenter)
        self.master.addWidget(self.save, alignment=Qt.AlignCenter)
        self.setLayout(self.master)
        
        self.setStyleSheet("""
    QWidget {
        background-color: #FFE4C4; /* Slightly lighter background */
    }

    QPushButton {
        background-color: #4CAF50; /* Green for buttons */
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: 1px solid #388E3C; /* Slightly darker green for border */
        padding: 10px 15px;
        border-radius: 10px;
    }

    QPushButton:hover {
        background-color: #98FB98; /* Darker green on hover */
    }

    QTextEdit {
        background-color: #FFE4C4;
        border: 2px solid #aaa;
        padding: 5px;
        color: #555;
        font-size: 22px;
        font-family: Mynamar MN;
    }

    QLabel {
        color: #555; /* Slightly darker text color */
    }
    
    QLabel#sentimentLabel {
        font-size: 22px;
        font-family: "Myanmar MN", sans-serif;
        color: #2196F3; /* Blue color for sentiment label */
        font-weight: bold;
    }
""")
        
    def connects(self):
        self.submit.clicked.connect(self.button_clicked)
        self.save.clicked.connect(self.save_clicked)

    def speak(self):
        listener = sr.Recognizer()
        text = ""
        with sr.Microphone() as source:
            try:
                audio = listener.listen(source, timeout=2)
                text = listener.recognize_google(audio)
                print(text)
            except sr.UnknownValueError:
                print("Can't understand audio")
            except sr.RequestError as e:
                print(f"Can't request results from Google: {e}")
            except Exception as e:
                print(f"Error: {e}")
                
        self.recognized_text = text
        return text

    def get_sentiment(self, text):
        if text:
            try:
                res = TextBlob(text)
            except Exception as e:
                print(f"Error analyzing: {e}")

            if res.sentiment.polarity > 0.3:
                return "Positive"
            elif res.sentiment.polarity < -0.3:
                return "Negative"
            else:
                return "Neutral"
        return None

    def button_clicked(self):
        res = self.speak()
        sentiment = self.get_sentiment(res)
        if res and sentiment is not None:
            self.output_label.setPlainText(res)
            self.sentiment_text.setText("Sentiment: " + str(sentiment))

    def save_clicked(self):
        content = self.output_label.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Note', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            with open(file_path, 'w') as file:
                file.write(content)

if __name__ == "__main__":
    app = QApplication([])
    main = Speech()
    main.show()
    app.exec_()
