# Домашняя работа 1

## Файлы в папке

| Файл | Описание |
|------|----------|
| `README.md` | Документация (текущий файл) |
| `complement.py` | Скрипт с реализацией алгоритмов для задания №2 |
| `count_kmers.py` | Скрипт с реализацией алгоритмов для задания №3 |
| `test.fna` | Последовательности для проверки работы кода для задания №3 |

# Задание 2: Reverse complement и GC состав ДНК

## Описание задачи
Программа принимает на вход нуклеотидную последовательность и выводит:
1. **Reverse complement** (обратную комплементарную последовательность)
2. **GC-состав** (долю нуклеотидов G и C) с тремя знаками после запятой

## Алгоритмы

### Reverse complement
Для получения обратного комплемента:
1. Последовательность переворачивается (reversed)
2. Каждый нуклеотид заменяется на комплементарный:
   - `A` → `T`
   - `T` → `A`
   - `G` → `C`
   - `C` → `G`

### GC-состав
Рассчитывается по формуле:
**GC = (количество G + количество C) / длина последовательности**.
Результат округляется до 3 знаков после запятой.

## Запуск программы

```bash
./complement.py --seq ATGCCGATGG
```

# Задание 3: Работа с конфликтами

Файл count_kmers.py был отправлен в репозиторий, а заетм отредактирован на Github. 
Далее на локальном слепке репозитория были внесены другие изменения: Структура кода изменена так, что теперь он принимает на вход не только название входного файла, но название выходного файла и значение k. При попытке закоммитить:
```bash
git commit -m "Замена k=2"                                   
[main de8b39d] Замена k=2
 Committer: Elisaveta Nikishina <elizavetanikisina@MacBook-Pro-Elizaveta.local>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 1 file changed, 10 insertions(+), 4 deletions(-)
```
При попытке запушить выходит сообщение:
```bash
 homeworks_2026 % git push
To github.com:lnik2204/homeworks_2026.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:lnik2204/homeworks_2026.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
Почему? Потому что на GitHub есть изменения (например, коллега поменял k на 2), которых нет в моем локальном репозитории. Git не позволяет перезаписать чужие изменения. 
Как разрешить конфликт? 
1. Скачать измененеия с Github
```bash
git pull
```
Появляется сообщение о конфликте: 
```bash
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 12 (delta 7), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (12/12), 3.26 KiB | 303.00 KiB/s, done.
From github.com:lnik2204/homeworks_2026
   9949875..56b4ebe  main       -> origin/main
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```
2. Есть две расходящиеся ветки: main - на моем компьютере, origin/main - на Github. Они обе имеют новые коммиты, которые не совпадают. Git не знает, как их объединить, и просит выбрать стратегию.
```bash
git pull --no-rebase
Auto-merging hw1/count_kmers.py
CONFLICT (content): Merge conflict in hw1/count_kmers.py
Automatic merge failed; fix conflicts and then commit the result.
```
3. Смотрим на маркеры конфликта:
```bash
cat hw1/count_kmers.py
```
Выглядит примерно так: 
```bash
<<<<<<< HEAD
Локальные изменения (с аргументами --k и --out)
...
'===='
Изменения с GitHub (только k с 4 на 2)
...
>>>>>>> origin/main
```
4. Разрешение конфликта: объединяем версии
```bash
nano hw1/count_kmers.py
```
```bash
#!/usr/bin/env python3

import argparse      
import json
from collections import Counter 
            
parser = argparse.ArgumentParser()
parser.add_argument('--fa', required=True, help='Входной FASTA файл')
parser.add_argument('--k', type=int, default=4, help='Длина k-мера')
parser.add_argument('--out', default='cnts.json', help='Выходной JSON файл')
args = parser.parse_args()

# Чтение FASTA
seqs = {}
with open(args.fa) as f:
    for line in f:   
        line = line.strip()
        if line.startswith('>'):
            name = line[1:].split()[0]
            seqs[name] = ''
        else:
            seqs[name] += line.upper()
    
# Подсчёт k-меров
result = {}
k = args.k
for name, seq in seqs.items():
<<<<<<< HEAD
    if len(seq) >= k:
        kmers = [seq[i:i+k] for i in range(len(seq)-k+1)]
        result[name] = dict(Counter(kmers))
    else:
        result[name] = {}
=======
    kmers = [seq[i:i+2] for i in range(len(seq)-1)]
    result[name] = dict(Counter(kmers))
>>>>>>> 56b4ebedcc5816c4e4b0d806a325adefa9680646

with open('out.json', 'w') as f:
    f.write('{\n')
    for i, (name, kmers) in enumerate(result.items()):
        kmers_str = json.dumps(kmers, ensure_ascii=False)
        f.write(f'    "{name}": {kmers_str}')
        if i < len(result) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write('}\n')
```
Убираю маркеры конфликта и просто оставляю изменения с аргументами

5. После добавляю объединенный файл, делаю коммит и пуш
```bash
git add hw1/count_kmers.py
git commit -m "Merge"
git push
```
Всё готово!

# Задание 6. Автоматизация через Github Actions
