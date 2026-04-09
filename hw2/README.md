# Домашняя работа 2

## Файлы в папке

| Файл | Описание |
|------|----------|
| `README.md` | Документация (текущий файл) |
| `wikipedia_articles.py` | Веб-кроулер на Wikipedia |
| `draw_wiki.py` | Cкрипт для отрисовки |
| `analyze_links.py` | Cкрипт для подсчета количестви ссылок статьи |


## Основные команды 
```bash
python3 wikipedia_articles.py --url "https://en.wikipedia.org/wiki/Bioinformatics" --depth 5 # запускаем скрипт на любой статье
python3 draw_wiki.py --json "Bioinformatics.json" --output bioinformatics_graph.png # визуализация
python3 analyze_links.py --url "https://en.wikipedia.org/wiki/Bioinformatics" # подсчет количества ссылок
```
# Задание 1: Веб-кроулер на Wikipedia

## Описание задачи
Веб-кроулер hw2/wikipedia_articles.py, который принимает точку входа-URL статьи в Wikipedia (аргумент --url), глубину (аргумент --depth). Кроулер начинает работу в исходной статье на Wikipedia, извлекает из её тела все внутренние ссылки на другие статьи Wikipedia, затем переходит по этим ссылкам до заданной глубины (в моем случае - 5), при этом избегая повторного посещения одних и тех же страниц. Результат - граф связей (в формате JSON) в файле start_article.json (start_article – название, title исходной страницы, с которой начинался кроулинг). С помощью библиотеки networkX далее отрисовывается граф связей, который
был получен из JSON для моей любимой статьи на Wikipedia и depth=5. Скрипт для отрисовки в hw2/draw_wiki.py

Также пришлось написать отдельный скрипт для проверки количества ссылок статьи (analyze_links.py), так как изначально выбранная статья обрабатывалась очень долго.
# Задание 3: REST API в ENCODE

'''bash
Statistics:
   - Top cell line: K562
   - TF proteins found: 23
   - Mapped to UniProt: 23
   - Proteins with domains: 19
   - Total Pfam domains found: 31
'''
# Задание 5: Telegram-уведомления для Github Actions
