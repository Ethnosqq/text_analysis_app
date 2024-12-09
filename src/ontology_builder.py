# src/ontology_builder.py
import networkx as nx
import matplotlib.pyplot as plt
import json

class OntologyBuilder:
    def __init__(self):
        # Создаем граф для онтологии
        self.graph = nx.DiGraph()
        self.formula = ""

    def build_ontology(self, keywords):
        """
        Формирует онтологию из списка ключевых слов.
        :param keywords: список ключевых слов
        """
        for i, keyword in enumerate(keywords):
            concept = f"C{i+1}"  # Концепт, например, C1, C2
            self.graph.add_node(concept, label=keyword)

        # Пример связей между концептами
        if len(keywords) > 1:
            self.graph.add_edge("C1", "C2")
            self.graph.add_edge("C2", "C3")

        # Генерация формулы
        self.formula = "C1 <= *C2+C3"
        return self.formula

    def visualize_ontology(self):
        """
        Визуализирует граф онтологии.
        """
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        labels = nx.get_node_attributes(self.graph, 'label')
        nx.draw(self.graph, pos, with_labels=True, labels=labels, node_size=3000, node_color="skyblue", font_size=12)
        plt.title("Граф онтологии", fontsize=16)
        plt.show()

    def save_graph_as_image(self, file_path):
        """
        Сохраняет граф онтологии в файл изображения (PNG).
        :param file_path: путь к файлу для сохранения
        """
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        labels = nx.get_node_attributes(self.graph, 'label')
        nx.draw(self.graph, pos, with_labels=True, labels=labels, node_size=3000, node_color="skyblue", font_size=12)
        plt.title("Граф онтологии", fontsize=16)
        plt.savefig(file_path)
        plt.close()

    def save_ontology_as_json(self, file_path):
        """
        Сохраняет формулу и структуру графа онтологии в файл JSON.
        :param file_path: путь к файлу для сохранения
        """
        ontology_data = {
            "formula": self.formula,
            "nodes": [{"id": node, "label": data.get("label", "")} for node, data in self.graph.nodes(data=True)],
            "edges": list(self.graph.edges())
        }
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(ontology_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении онтологии: {e}")
