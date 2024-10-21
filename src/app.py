# src/app.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog
from text_analyzer import TextAnalyzer
from file_handler import extract_text_from_docx, extract_text_from_pdf

class TextAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Text Analysis Tool")

        # Инициализация анализатора текста
        self.analyzer = TextAnalyzer()

        # Текстовое поле для ввода текста
        self.text_input_label = ttk.Label(root, text="Введите текст для анализа:")
        self.text_input_label.pack(pady=5)

        self.text_input = tk.Text(root, height=10, width=60)
        self.text_input.pack(padx=10, pady=5)

        # Кнопка для загрузки файла
        self.upload_button = ttk.Button(root, text="Загрузить файл (DOCX/PDF)", command=self.upload_file, bootstyle=INFO)
        self.upload_button.pack(pady=5)

        # Настройки для длины аннотации
        self.length_label = ttk.Label(root, text="Длина аннотации:")
        self.length_label.pack(pady=5)

        self.length_var = tk.StringVar(value="средняя")
        self.length_options = ttk.Combobox(root, textvariable=self.length_var, values=["краткая", "средняя", "подробная"])
        self.length_options.pack(pady=5)

        # Настройки для количества ключевых слов
        self.keywords_label = ttk.Label(root, text="Количество ключевых слов:")
        self.keywords_label.pack(pady=5)

        self.keywords_var = tk.IntVar(value=5)
        self.keywords_spinbox = ttk.Spinbox(root, from_=1, to=20, textvariable=self.keywords_var)
        self.keywords_spinbox.pack(pady=5)

        # Кнопка для анализа текста
        self.analyze_button = ttk.Button(root, text="Анализировать текст", command=self.analyze_text, bootstyle=SUCCESS)
        self.analyze_button.pack(pady=5)

        # Кнопка для сохранения результатов
        self.save_button = ttk.Button(root, text="Сохранить результат", command=self.save_results, bootstyle=WARNING)
        self.save_button.pack(pady=5)

        # Поле для вывода результата
        self.result_label = ttk.Label(root, text="Результат анализа:")
        self.result_label.pack(pady=5)

        self.result_output = tk.Text(root, height=15, width=60)
        self.result_output.pack(padx=10, pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("DOCX files", "*.docx"), ("PDF files", "*.pdf")])
        if file_path:
            if file_path.endswith(".docx"):
                extracted_text = extract_text_from_docx(file_path)
            elif file_path.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(file_path)

            self.text_input.insert('end', extracted_text)

    def analyze_text(self):
        input_text = self.text_input.get("1.0", "end").strip()
        if not input_text:
            self.display_result("Пожалуйста, введите текст или загрузите файл.")
            return

        # Определение языка текста
        language = self.analyzer.detect_language(input_text)
        language_message = f"Обнаружен язык текста: {language}\n\n"

        # Создание аннотации
        summarized_text = self.analyzer.summarize_text(input_text, length=self.length_var.get())

        # Извлечение ключевых слов
        keywords = self.analyzer.extract_keywords(input_text, num_keywords=self.keywords_var.get())

        # Сохранение результатов для дальнейшего использования
        self.last_result = {
            "summary": summarized_text,
            "keywords": keywords
        }

        # Вывод результата
        result = f"{language_message}Аннотация:\n{summarized_text}\n\nКлючевые слова:\n{', '.join(keywords)}"
        self.display_result(result)

    def save_results(self):
        if not hasattr(self, 'last_result'):
            self.display_result("Нет результатов для сохранения. Пожалуйста, сначала выполните анализ текста.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("Аннотация:\n")
                    file.write(self.last_result["summary"] + "\n\n")
                    file.write("Ключевые слова:\n")
                    file.write(', '.join(self.last_result["keywords"]))
                self.display_result("Результаты успешно сохранены.")
            except Exception as e:
                self.display_result(f"Ошибка при сохранении файла: {e}")

    def display_result(self, result):
        self.result_output.config(state='normal')
        self.result_output.delete("1.0", "end")
        self.result_output.insert('end', result)
        self.result_output.config(state='disabled')


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = TextAnalysisApp(root)
    root.mainloop()
