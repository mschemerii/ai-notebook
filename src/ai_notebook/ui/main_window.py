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

from ai_notebook.services.ollama_client import OllamaClient


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ollama_client = OllamaClient()

        self.setWindowTitle("AI Notebook")
        self.resize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.open_document_button = QPushButton("Open Document")
        self.open_document_button.clicked.connect(self.open_document)
        main_layout.addWidget(self.open_document_button)

        self.document_info_label = QLabel(
            "Loaded: No document selected"
        )

        main_layout.addWidget(self.document_info_label)

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
        self.question_input.returnPressed.connect(self.ask_question)	

        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.ask_question)

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
            self.document_info_label.setText(
                f"Loaded: {file_path.split('/')[-1]} "
                f"({len(content):,} characters)"
            )

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

    def ask_question(self):
        document_text = self.document_preview.toPlainText()
        question = self.question_input.text()

        if not document_text.strip():
            self.answer_output.setPlainText(
                "Please load a document first."
            )
            return

        if not question.strip():
            self.answer_output.setPlainText(
                "Please enter a question."
            )
            return

        self.answer_output.setPlainText("Thinking...")

        try:
            answer = self.ollama_client.ask(
                document_text,
                question,
            )
            self.answer_output.setPlainText(answer)

        except ConnectionError as error:
            self.answer_output.setPlainText(str(error))
