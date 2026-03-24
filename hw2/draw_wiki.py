#!/usr/bin/env python3
"""
Визуализация графа Wikipedia из JSON файла.
"""

import argparse
import json
import os
import sys

try:
    import networkx as nx
    import matplotlib.pyplot as plt
except ImportError:
    print("Установите необходимые библиотеки:")
    print("pip install networkx matplotlib")
    sys.exit(1)


def load_graph(json_file):
    """Загружает граф из JSON файла."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def draw_graph(data, output_image='graph.png', max_nodes=30):
    """
    Визуализирует граф связей.
    
    Args:
        data: Словарь с данными из JSON
        output_image: Имя выходного файла изображения
        max_nodes: Максимальное количество узлов для отображения (ограничиваем для читаемости)
    """
    graph_data = data.get('graph', {})
    titles = data.get('titles', {})
    start_title = data.get('start_title', 'Unknown')
    total_pages = data.get('total_pages', 0)
    
    if not graph_data:
        print("Граф пуст!")
        return
    
    print(f"Строим граф для статьи: {start_title}")
    print(f"Всего страниц в JSON: {total_pages}")
    print(f"Узлов в графе: {len(graph_data)}")
    
    # Создаем ориентированный граф
    G = nx.DiGraph()
    
    # Добавляем узлы и ребра
    for source, targets in graph_data.items():
        # Получаем короткое имя для отображения
        source_name = titles.get(source, source.split('/')[-1].replace('_', ' '))
        if len(source_name) > 40:
            source_name = source_name[:37] + "..."
        
        G.add_node(source, name=source_name)
        
        for target in targets[:max_nodes // 2]:  # Ограничиваем количество ребер
            target_name = titles.get(target, target.split('/')[-1].replace('_', ' '))
            if len(target_name) > 40:
                target_name = target_name[:37] + "..."
            G.add_node(target, name=target_name)
            G.add_edge(source, target)
    
    print(f"Узлов в визуализации: {G.number_of_nodes()}")
    print(f"Ребер в визуализации: {G.number_of_edges()}")
    
    # Настройка визуализации
    plt.figure(figsize=(16, 12))
    
    # Позиционирование узлов (используем spring layout)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue',
                          node_size=2000,
                          alpha=0.8)
    
    # Рисуем ребра
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          alpha=0.5,
                          arrows=True,
                          arrowsize=15)
    
    # Рисуем метки
    labels = {node: G.nodes[node].get('name', node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Выделяем начальную статью
    start_node = list(graph_data.keys())[0] if graph_data else None
    if start_node and start_node in G:
        nx.draw_networkx_nodes(G, pos,
                              nodelist=[start_node],
                              node_color='red',
                              node_size=3000,
                              alpha=0.9)
    
    # Заголовок
    plt.title(f"Wikipedia Graph: {start_title}\nTotal pages: {total_pages} | Displayed: {G.number_of_nodes()} nodes",
             fontsize=14, fontweight='bold')
    
    plt.axis('off')
    plt.tight_layout()
    
    # Сохраняем изображение
    plt.savefig(output_image, dpi=150, bbox_inches='tight')
    print(f"\nГраф сохранен в: {output_image}")
    
    # Показываем
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Визуализация графа Wikipedia')
    parser.add_argument('--json', required=True,
                        help='JSON файл с результатами обхода')
    parser.add_argument('--output', default='graph.png',
                        help='Имя выходного файла изображения (по умолчанию: graph.png)')
    parser.add_argument('--max-nodes', type=int, default=30,
                        help='Максимальное количество узлов для отображения (по умолчанию: 30)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.json):
        print(f"Ошибка: файл {args.json} не найден")
        return 1
    
    data = load_graph(args.json)
    draw_graph(data, args.output, args.max_nodes)
    
    return 0


if __name__ == "__main__":
    exit(main())
