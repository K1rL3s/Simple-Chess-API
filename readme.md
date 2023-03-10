# Simple Chess API

#### Просто шахматное API, легко интегрируемое в чат-ботов.

Принцип работы:

1. На сервер приходит GET запрос с историей ходов и новым ходом, который хочет сделать пользователь.
2. Программа обрабатывает его, и если все параметры корректные, то возвращает JSON с ходом движка Stockfish,
   новой историей ходов и FEN-нотацией текущей позиции.
3. С помощью этой нотации можно получить изображение шмахматной доски (<a href="#L73">см. ниже</a>).

Проект написан на **Flask** с применением **waitress** как WSGI. \
Сервер ничего не сохраняет, поэтому держите историю ходов при себе! :)

### Запуск

1. Установить **python** версии **3.10**+
   (Тестировалось на версии **3.10.8**)
2. Установить все библиотеки в файле с помощью `python -m pip install -r ./requirements`\
   *(При запуске на Windows прочтите requirements.txt для корректной установки зависимостей)*
3. Запустить сервер с помощью команды `python main.py`

### Формат запросов-ответов

- Все запросы осуществляются в формате GET.
- "*" - обязательные параметры, "." - опциональные параметры. 
- Общий формат запросов: \
  `http://host:port/api/chess/{action}/?{params}`
- Общий формат ответов:

```json
{
  "status_code": <int>,
  "response": {
    "message": <str>,
    "...": <...>
  }
}
```

### Конкретные случаи

- #### /api/chess/move/?

1. Возможные параметры:

| Параметр       | Формат                                               | Описание                                  |
|----------------|------------------------------------------------------|-------------------------------------------|
| *.`user_move`  | **string**, "cNcN"<br/>c - буква, N - номер          | Ход игрока из позиции `prev_moves`        |
| .`prev_moves`  | **string**, "cNcN;cNcN;..."<br/>c - буква, N - номер | История ходов партии.                     |
| .`orientation` | **string**, "w" or "b"                               | Цвет, которым играет пользователь.        |
| .`threads`     | **int**                                              | Количество потоков для движка.            |
| .`depth`       | **int**                                              | Глубина просчёта ходов.                   |
| .`ram_hash`    | **int**                                              | Количество оперативной памяти для движка. |
| .`skill_level` | **int**                                              | Уровень игры движка.                      |
| .`elo`         | **int**                                              | Количество ЭЛО движка                     |

*(Если игрок играет черными и требуется первый ход от движка,
то необходимо передать `orientation=b` и оставить `user_move` пустым. \
В остальных случаях параметр `user_move` является обязательным)*

2. Успешный ответ сервера:

| Ключ             | Формат                                               | Описание                           |
|------------------|------------------------------------------------------|------------------------------------|
| `stockfish_move` | **string**, "cNcN"<br/>c - буква, N - номер          | Ход движка после хода игрока.      |
| `prev_moves`     | **string**, "cNcN;cNcN;..."<br/>c - буква, N - номер | Новая история ходов партии.        |
| `orientation`    | **string**, "w" or "b"                               | Цвет, которым играет пользователь. |
| `fen`            | **string**, "<...>/<...>/..."                        | Текущая позиция в FEN нотации.     |

<br>

- #### /api/chess/board/?
1. Возможные параметры:

| Параметр       | Формат                        | Описание                           |
|----------------|-------------------------------|------------------------------------|
| *`fen`         | **string**, "<...>/<...>/..." | Позиция, которую нужно изобразить. |
| .`orientation` | **string**, "w" or "b"        | Фигуры какого цвета будут внизу.   |
| .`size`        | **int**                       | Размер изображения.                |

2. Успешный ответ сервера: `png image`.



