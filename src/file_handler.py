# src/file_handler.py
import docx
import PyPDF2

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        return '\n'.join(full_text) if full_text else "Файл пустой или не содержит текста для анализа."
    except Exception as e:
        return f"Ошибка при извлечении текста из DOCX: {e}"

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text.append(page_text)
            return '\n'.join(full_text) if full_text else "Файл пустой или не содержит текста для анализа."
    except Exception as e:
        return f"Ошибка при извлечении текста из PDF: {e}"
