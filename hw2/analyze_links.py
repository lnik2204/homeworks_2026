#!/usr/bin/env python3
"""
Скрипт для анализа количества ссылок в статье Wikipedia.
Помогает выбрать статью с оптимальным количеством ссылок для обхода.
"""

import argparse
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin


def count_wiki_links(url):
    """
    Подсчитывает количество внутренних ссылок Wikipedia на странице.
    
    Returns:
        dict: Статистика по ссылкам
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"\n Анализируем: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Получаем заголовок статьи
        title_tag = soup.find('h1', {'id': 'firstHeading'})
        title = title_tag.get_text().strip() if title_tag else "Неизвестно"
        
        # Ищем содержимое статьи
        content = soup.find('div', {'id': 'bodyContent'})
        
        if not content:
            return {
                'url': url,
                'title': title,
                'error': 'Не найден блок bodyContent'
            }
        
        # Собираем все ссылки на статьи
        all_links = []
        wiki_links = []
        special_links = []
        
        for link in content.find_all('a', href=True):
            href = link['href']
            
            if href.startswith('/wiki/'):
                # Проверяем, не служебная ли страница
                if ':' not in href and '#' not in href and 'Main_Page' not in href:
                    wiki_links.append(href)
                    all_links.append(href)
                elif ':' in href:
                    special_links.append(href)
        
        # Уникальные ссылки
        unique_links = set(wiki_links)
        
        # Получаем несколько примеров
        sample_links = list(unique_links)[:10]
        
        result = {
            'url': url,
            'title': title,
            'total_links': len(all_links),
            'wiki_links_count': len(wiki_links),
            'unique_wiki_links': len(unique_links),
            'special_links_count': len(special_links),
            'sample_links': sample_links
        }
        
        return result
        
    except Exception as e:
        return {
            'url': url,
            'title': None,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Анализ количества ссылок в статье Wikipedia')
    parser.add_argument('--url', required=True, help='URL статьи Wikipedia')
    
    args = parser.parse_args()
    
    result = count_wiki_links(args.url)
    
    print("\n" + "="*60)
    print(" РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("="*60)
    
    if 'error' in result:
        print(f" Ошибка: {result['error']}")
        return 1
    
    print(f"\n Статья: {result['title']}")
    print(f" URL: {result['url']}")
    print(f"\n Статистика ссылок:")
    print(f"   • Всего ссылок в теле статьи: {result['total_links']}")
    print(f"   • Ссылок на другие статьи Wikipedia: {result['wiki_links_count']}")
    print(f"   • Уникальных статей: {result['unique_wiki_links']}")
    print(f"   • Служебных ссылок (:, File:, Help:): {result['special_links_count']}")
    
    print(f"\n Примеры первых 10 уникальных статей:")
    for i, link in enumerate(result['sample_links'][:10], 1):
        article_name = link.replace('/wiki/', '').replace('_', ' ')
        print(f"   {i}. {article_name[:60]}...")
    
    # Оценка сложности обхода
    print(f"\n Рекомендации:")
    if result['unique_wiki_links'] < 50:
        print(" Очень хорошая статья для обхода (мало ссылок)")
    elif result['unique_wiki_links'] < 150:
        print(" Хорошая статья для обхода (умеренное количество ссылок)")
    elif result['unique_wiki_links'] < 500:
        print("️ Статья имеет много ссылок, обход может занять время")
    else:
        print(f" Статья имеет очень много ссылок, лучше выбрать другую")
        print(f" Рекомендуем выбрать статью с <200 уникальными ссылками")
    
    return 0


if __name__ == "__main__":
    exit(main())
