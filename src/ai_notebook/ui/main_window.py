from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Notebook")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.open_document_button = QPushButton("Open Document")
        self.open_document_button.clicked.connect(self.open_document)
        main_layout.addWidget(self.open_document_button)

        main_layout.addWidget(QLabel("Document Preview"))

        self.document_preview = QTextEdit()
        self.document_preview.setPlaceholderText(
            "Loaded document text will appear here."
        )
        main_layout.addWidget(self.document_preview)

        question_layout = QHBoxLayout()

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Ask a question about the document..."
        )

        self.ask_button = QPushButton("Ask")

        question_layout.addWidget(self.question_input)
        question_layout.addWidget(self.ask_button)

        main_layout.addLayout(question_layout)

        main_layout.addWidget(QLabel("Answer"))

        self.answer_output = QTextEdit()
        self.answer_output.setPlaceholderText(
            "AI response will appear here."
        )
        self.answer_output.setReadOnly(True)

        main_layout.addWidget(self.answer_output)

    def open_document(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "Text Files (*.txt *.md);;All Files (*)",
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if not content.strip():
                QMessageBox.warning(
                    self,
                    "Empty File",
                    "The selected file is empty.",
                )
                return

            self.document_preview.setPlainText(content)

        except UnicodeDecodeError:
            QMessageBox.critical(
                self,
                "File Error",
                "Could not read this file as text.",
            )
        except OSError as error:
            QMessageBox.critical(
                self,
                "File Error",
                f"Could not open file:\n{error}",
            )
