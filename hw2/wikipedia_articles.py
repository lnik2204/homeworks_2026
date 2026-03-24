#!/usr/bin/env python3

"""
Веб-кроулер для Wikipedia.
Обходит статьи по ссылкам до заданной глубины и строит граф связей.
"""

import argparse
import json
import re
import time
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class WikipediaCrawler:
    """Кроулер для обхода статей Wikipedia."""
    
    def __init__(self, start_url, max_depth=2, delay=0.5):
        """
        Инициализация кроулера.
        
        Args:
            start_url: Начальная URL для обхода
            max_depth: Максимальная глубина обхода
            delay: Задержка между запросами (секунды)
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()  # Множество посещенных URL
        self.graph = {}  # Словарь {url: [список связанных url]}
        self.article_titles = {}  # {url: title}
        
        # Заголовки для имитации браузера
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _extract_wiki_links(self, url, soup):
        """
        Извлекает все внутренние ссылки Wikipedia из BeautifulSoup объекта.
        
        Args:
            url: Текущая URL (для построения абсолютных ссылок)
            soup: BeautifulSoup объект страницы
            
        Returns:
            list: Список абсолютных URL найденных статей
        """
        links = []
        
        # Ищем div с содержимым статьи (bodyContent)
        content = soup.find('div', {'id': 'bodyContent'})
        if not content:
            return links
        
        # Ищем все ссылки в содержимом
        for link in content.find_all('a', href=True):
            href = link['href']
            
            # Фильтруем только ссылки на статьи Wikipedia
            # Исключаем:
            # - внешние ссылки (http://, https://)
            # - специальные страницы (:, File:, Help:, etc.)
            # - якоря (#)
            if (href.startswith('/wiki/') and 
                not ':' in href and  # Исключаем служебные страницы
                not '#' in href and  # Исключаем якоря
                not 'Main_Page' in href):
                
                # Строим абсолютный URL
                full_url = urljoin(url, href)
                links.append(full_url)
        
        return links
    
    def _get_page_title(self, soup):
        """Извлекает заголовок статьи из HTML."""
        title_tag = soup.find('h1', {'id': 'firstHeading'})
        if title_tag:
            return title_tag.get_text().strip()
        return None
    
    def crawl(self):
        """
        Запускает процесс обхода.
        
        Returns:
            dict: Словарь с результатами обхода
        """
        # Используем очередь для BFS
        # Элементы: (url, depth)
        queue = deque()
        queue.append((self.start_url, 0))
        
        # Получаем заголовок начальной статьи
        try:
            response = requests.get(self.start_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            start_title = self._get_page_title(soup)
            self.article_titles[self.start_url] = start_title
        except Exception as e:
            print(f"Ошибка при загрузке начальной страницы: {e}")
            start_title = None
        
        print(f"Начинаем обход от: {start_title or self.start_url}")
        print(f"Максимальная глубина: {self.max_depth}")
        print("-" * 50)
        
        while queue:
            current_url, depth = queue.popleft()
            
            # Пропускаем уже посещенные
            if current_url in self.visited:
                continue
            
            # Отмечаем как посещенную
            self.visited.add(current_url)
            
            # Проверяем глубину
            if depth > self.max_depth:
                continue
            
            print(f"[Глубина {depth}] Обрабатываем: {current_url}")
            
            try:
                # Загружаем страницу
                response = requests.get(current_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Парсим HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Получаем заголовок статьи
                title = self._get_page_title(soup)
                if title:
                    self.article_titles[current_url] = title
                    print(f"  → Заголовок: {title}")
                
                # Извлекаем ссылки
                links = self._extract_wiki_links(current_url, soup)
                self.graph[current_url] = links
                print(f"  → Найдено ссылок: {len(links)}")
                
                # Добавляем новые ссылки в очередь
                for link in links:
                    if link not in self.visited and link not in [item[0] for item in queue]:
                        queue.append((link, depth + 1))
                
                # Задержка между запросами (уважаем сервер)
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"Ошибка при обработке: {e}")
                self.graph[current_url] = []
        
        print("-" * 50)
        print(f"Обход завершен. Всего страниц: {len(self.visited)}")
        
        return {
            'start_url': self.start_url,
            'start_title': self.article_titles.get(self.start_url),
            'max_depth': self.max_depth,
            'total_pages': len(self.visited),
            'graph': self.graph,
            'titles': self.article_titles
        }


def main():
    parser = argparse.ArgumentParser(description='Веб-кроулер для Wikipedia')
    parser.add_argument('--url', required=True, 
                        help='URL начальной статьи Wikipedia')
    parser.add_argument('--depth', type=int, default=2,
                        help='Максимальная глубина обхода (по умолчанию: 2)')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='Задержка между запросами (секунды, по умолчанию: 0.5)')
    parser.add_argument('--output', default=None,
                        help='Имя выходного JSON файла (по умолчанию: <start_article>.json)')
    
    args = parser.parse_args()
    
    # Проверяем, что URL ведет на Wikipedia
    if 'wikipedia.org' not in args.url:
        print("Ошибка: URL должен быть страницей Wikipedia")
        return 1
    
    # Создаем кроулер
    crawler = WikipediaCrawler(args.url, args.depth, args.delay)
    
    # Запускаем обход
    result = crawler.crawl()
    
    # Определяем имя выходного файла
    if args.output:
        output_file = args.output
    else:
        # Извлекаем название статьи из URL
        article_name = args.url.rstrip('/').split('/')[-1].replace('_', ' ')
        output_file = f"{article_name}.json"
    
    # Сохраняем результат в JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nРезультаты сохранены в: {output_file}")
    print(f"Граф содержит {len(result['graph'])} узлов и {sum(len(v) for v in result['graph'].values())} ребер")
    
    return 0


if __name__ == "__main__":
    exit(main())
