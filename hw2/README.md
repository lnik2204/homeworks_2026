# Домашняя работа 2

## Файлы в папке

| Файл | Описание |
|------|----------|
| `README.md` | Документация (текущий файл) |
| `wikipedia_articles.py` | Веб-кроулер на Wikipedia |
| `draw_wiki.py` | Cкрипт для отрисовки |
| `analyze_links.py` | Cкрипт для подсчета количества ссылок статьи |
| `get_domains.py` | Cкрипт для получения списка белков через REST API ENCODE |

## Основные команды 
```bash
python3 wikipedia_articles.py --url "https://en.wikipedia.org/wiki/Capybara" --depth 5 # запускаем скрипт на любой статье
python3 draw_wiki.py --json "Capybara.json" --output bioinformatics_graph.png # визуализация
python3 analyze_links.py --url "https://en.wikipedia.org/wiki/Capybara" # подсчет количества ссылок
python3 get_domains.py # получение списка белков
```
# Задание 1: Веб-кроулер на Wikipedia

## Описание задачи
Веб-кроулер hw2/wikipedia_articles.py, который принимает точку входа-URL статьи в Wikipedia (аргумент --url), глубину (аргумент --depth). Кроулер начинает работу в исходной статье на Wikipedia, извлекает из её тела все внутренние ссылки на другие статьи Wikipedia, затем переходит по этим ссылкам до заданной глубины (в моем случае - 5), при этом избегая повторного посещения одних и тех же страниц. Результат - граф связей (в формате JSON) в файле start_article.json (start_article – название, title исходной страницы, с которой начинался кроулинг). С помощью библиотеки networkX далее отрисовывается граф связей, который был получен из JSON для статьи про капибар на Wikipedia и depth=5. Скрипт для отрисовки в hw2/draw_wiki.py

Также пришлось написать отдельный скрипт для проверки количества ссылок статьи (analyze_links.py), так как изначально выбранная статья про биоинформатику обрабатывалась очень долго. С глубиной 5 скрипт работал полторы недели и выдал файл JSON, но, к сожалению, граф построить не удалось. Так как для статьи Capybara, всего страниц в JSON: 1359979, узлов в графе: 860286, узлов в визуализации: 899128, ребер в визуализации: 438148. 

# Задание 3: REST API в ENCODE

### Используемые API и эндпоинты

#### 1. ENCODE API
- **Базовый URL:** `https://www.encodeproject.org/search/`
- **Используемые параметры:**
  - `type=Experiment` — тип объекта
  - `assay_title=DNase-seq` / `TF ChIP-seq` — тип эксперимента
  - `biosample_ontology.classification=cell line` — тип образца
  - `status=released` — только опубликованные данные
  - `format=json` — формат ответа

#### 2. UniProt API
- **Базовый URL:** `https://rest.uniprot.org/uniprotkb/search`
- **Используемые параметры:**
  - `query=gene_exact:{gene} AND organism_id:9606` — точное название гена, организм человек
  - `fields=accession,gene_names` — запрашиваемые поля
  - `format=json` — формат ответа
  - `size=1` — один результат

#### 3. InterPro API (для Pfam доменов)
- **Базовый URL:** `https://www.ebi.ac.uk/interpro/api`
- **Используемые эндпоинты:**
  1. `GET /protein/uniprot/{uniprot_id}/entry/pfam` — получение Pfam записей для белка
  2. `GET /entry/pfam/{accession}` — детали конкретного Pfam домена (через entries_url)

```bash
Statistics:
   - Top cell line: K562
   - TF proteins found: 23
   - Mapped to UniProt: 23
   - Proteins with domains: 19
   - Total Pfam domains found: 31
```
