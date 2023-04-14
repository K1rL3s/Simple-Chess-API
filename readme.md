# Simple Chess API

#### [Простое шахматное API](https://github.com/K1rL3s/Simple-Chess-API), легко интегрируемое в чат-ботов

Принцип работы:

1. На сервер приходит GET запрос с историей ходов и новым ходом, который хочет сделать пользователь.
2. Программа обрабатывает его, и если все параметры корректные, то возвращает JSON с ходом движка Stockfish,
   новой историей ходов и FEN текущей позиции.
3. С помощью этой нотации можно получить изображение шмахматной доски (см. ниже).
4. Все ходы и оценки позиций делает движок [Stockfish](https://stockfishchess.org/).

Проект написан на **Flask** с применением **waitress** как WSGI. \
Сервер ничего не сохраняет, поэтому держите историю ходов при себе! :)

### Запуск

1. Установить **python** версии **3.10**+
   (Тестировалось на версии **3.10.8**)

2. Склонировать репозиторий и перейти в него:

```commandline
git clone https://github.com/K1rL3s/Simple-Chess-API.git
cd ./Simple-Chess-API
```

3. Установить все нужные библиотеки. \
   *При запуске на Windows прочтите requirements.txt для корректной установки зависимостей*

```commandline
pip install -r ./requirements.txt
```

4. Установить шахматный движок для работы с библиотекой **stockfish**
   ([docs](https://pypi.org/project/stockfish/)) ([stockfish](https://stockfishchess.org/download/))

5. Создать и заполнить файл `.env` в корневой папке:

```env
STOCKFISH_ENGINE_PATH=<path-to-engine-exe>
API_AUTH_KEY=<token> (без авторизации - оставить пустым)
SECRET_KEY=<csrf-token>
```

6. Запустить сервер:

```commandline
python ./main.py
```

### Формат запросов-ответов

- Все запросы осуществляются в формате GET.
- "*" - обязательные параметры, "." - опциональные параметры.
- **"cN"** -> c - буква, N - номер.
- В описании ключей ответа сервера речь идёт о словаре "response".
- Общий формат запросов: \
  `http://host:port/api/chess/{action}/?{params}`
- Общий формат ответов:

```json
{
    "status_code": <int>,
    "message": <str>,
    "response": {
        "...": <...>
    }
}
```

## Конкретные случаи

### /api/chess/move/?

1. Возможные параметры:

| Параметр       | Формат                                 | Описание                                   |
|----------------|----------------------------------------|--------------------------------------------|
| *.`user_move`  | **string**, "cNcN"                     | Ход игрока из позиции `prev_moves`         |
| .`prev_moves`  | **string**, "cNcN;cNcN;..."            | История ходов партии.                      |
| .`orientation` | **string**, "w", "white", "b", "black" | Цвет, которым играет пользователь.         |
| .`min_time`    | **int**                                | Минимальное время на подумать движку, мс.  |
| .`max_time`    | **int**                                | Максимальное время на подумать движку, мс. |
| .`threads`     | **int**                                | Количество потоков для движка.             |
| .`depth`       | **int**                                | Глубина просчёта ходов.                    |
| .`ram_hash`    | **int**                                | Количество оперативной памяти для движка.  |
| .`skill_level` | **int**                                | Уровень игры движка.                       |
| .`elo`         | **int**                                | Количество ЭЛО движка                      |

*(Если игрок играет черными и требуется первый ход от движка,
то необходимо передать `orientation=b` и оставить `user_move` пустым. \
В остальных случаях параметр `user_move` является обязательным)*

2. Успешный ответ сервера:

| Ключ             | Формат                                                                   | Описание                                                             |
|------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------|
| `stockfish_move` | **string** / **null** "cNcN"                                             | Ход движка после хода игрока.                                        |
| `prev_moves`     | **string**, "cNcN;cNcN;..."                                              | Новая история ходов партии.                                          |
| `orientation`    | **string**, "w" или "b"                                                  | Цвет, которым играет пользователь.                                   |
| `fen`            | **string**, "<...>/<...>/..."                                            | Текущая позиция в FEN.                                               |
| `end_type`       | **string** / **null**, "checkmate", "stalemate", "insufficient_material" | Как закончилась игра (!= null только тогда, когди игра закончилась). |
| `check`          | **string** / **null**, "cN"                                              | На какой клетке стоит король под шахом.                              |

<br>

### /api/chess/board/?

1. Возможные параметры:

| Параметр       | Формат                                                          | Описание                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|----------------|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *`fen`         | **string**, "<...>/<...>/..."                                   | Позиция, которую нужно изобразить.                                                                                                                                                                                                                                                                                                                                                                                                                            |
| .`orientation` | **string**, "w", "white", "b", "black"                          | Фигуры какого цвета будут внизу.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| .`size`        | **int**                                                         | Размер изображения.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| .`colors`      | **string**, "key-value;key-value;..."                           | Цвета клеток, рамки с координатами и символов. Возможные ключи:<br>``square light`` (белые клетки),<br>``square dark`` (черные клетка),<br>``square light lastmove`` (белая клетка последний ход),<br>``square dark lastmove`` (черная клетка последний ход),<br>``margin`` (фон координат),<br>``coord`` (числа и буквы).<br><br>Значения должны выглядеть как ``ffce9e`` (RGB) или ``15781B80`` (RGBA)<br>(в случае с GET запросом - без решётки в начале). |
| .`last_move`   | **string**, "cNcN"                                              | Подсветка клеток последнего хода.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| .`coords`      | **string**, "t", "true", "1", "f", "false", "1"<br>Тру или Фэлс | Рисовать ли рамку с координатами, по умолчанию "t".                                                                                                                                                                                                                                                                                                                                                                                                           |
| .`check`       | **string**, "cN"                                                | Размер изображения.                                                                                                                                                                                                                                                                                                                                                                                                                                           |

2. Успешный ответ сервера: `png image`.

<br>

### /api/chess/position/?

1. Возможные параметры:

| Параметр       | Формат                                                          | Описание                                                                    |
|----------------|-----------------------------------------------------------------|-----------------------------------------------------------------------------|
| *.`fen`        | **string**, "<...>/<...>/..."                                   | Позиция, которую нужно оценить.                                             |
| *.`prev_moves` | **string**, "cNcN;cNcN;..."                                     | История ходов, которую нужно оценить.                                       |
| .`with_engine` | **string**, "t", "true", "1", "f", "false", "1"<br>Тру или Фэлс | Использовать ли движок для анализа позиции в сантипешках, по умолчанию "t". |

*(Необходим только один из параметров; fen приоритетнее)*

2. Успешный ответ сервера:

| Ключ       | Формат                                                              | Описание                                  |
|------------|---------------------------------------------------------------------|-------------------------------------------|
| `is_end`   | **bool**                                                            | Закончилась ли игра.                      |
| `who_win`  | **string** / **null**, "w", "b"                                     | Кто победил.                              |
| `end_type` | **string**, "checkmate", "stalemate", "insufficient_material", "cp" | Как закончилась игра ("cp" - centipawns). |
| `value`    | **int**                                                             | В чью пользу позиция в сантипешках.       |
| `wdl`      | **array[int]** / **null**                                           | Оценка win/draw/loss.                     |
| `fen`      | **string**, "<...>/<...>/..."                                       | Текущая позиция в FEN.                    |

<br>

## Информационные запросы

### /api/chess/docs/

Возвращает HTML страницу с этим readme.md файлом.

<br>

### /api/chess/limits/

Возвращает JSON с минимумом, дефолтом и максимумом для числовых параметров генерации хода и рисования доски.

```json
{
    "status_code": 200,
    "message": "OK",
    "response": {
        "param_name": {
            "min": <int>,
            "default": <int>,
            "max": <int>
        }
    }
}
```

<br>

## Трудности, сложности и проблемы
1. Хотелось бы сделать получение хода от движка с помощью FEN-позиции, но Stockfish.is_fen_valid() возвращает False, если мат на доске \
   (ещё и крашится без ошибки, если ему поставить невозможную позицию).
2. Хотелось сделать эндпоинт "is_legal", но клиенту проще обрабатывать 400-ую ошибку на своей стороне.
3. На рабочем ноутбуке движок открывается за 200мс, на сервере 0.8-5 секунд.
4. Начальник просит реализовать очереди движков с помощью RabbitMQ (kombu, celery).
