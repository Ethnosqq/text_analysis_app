# src/text_analyzer.py
from langdetect import detect
from transformers import pipeline
from keybert import KeyBERT

class TextAnalyzer:
    def __init__(self):
        self.summarizer = pipeline("summarization")
        self.keyword_extractor = KeyBERT()

    def detect_language(self, text):
        try:
            return detect(text)
        except Exception as e:
            return f"Ошибка при определении языка: {e}"

    def summarize_text(self, text, length="средняя"):
        max_chunk_size = 800
        text_chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        summarized_text = []
        max_length = 50 if length == "краткая" else 100 if length == "средняя" else 200

        try:
            for chunk in text_chunks:
                summary = self.summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
                if summary and len(summary) > 0:
                    summarized_text.append(summary[0]['summary_text'])

            return ' '.join(summarized_text)
        except Exception as e:
            return f"Ошибка при аннотировании текста: {e}"

    def extract_keywords(self, text, num_keywords=5):
        try:
            keywords = self.keyword_extractor.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num_keywords)
            return [kw[0] for kw in keywords if kw]
        except Exception as e:
            return [f"Ошибка при извлечении ключевых слов: {e}"]
