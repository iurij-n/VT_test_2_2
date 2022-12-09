## Задание 2.2

#### Стэк:
- python
- asyncio, aiohttp
- PyQt5

Desktop-приложение, реализующие следующие функции:
 - форма ввода URL-адресов
 - форма ввода списка xpath для поиска данных на странице
 - подключение по TCP и отправка HTTP GET-запроса по каждому адресу
 - получение HTML-контента и парсинг
 - вывод результатов по каждому запросу

Приложение имеет графическией итерфейс. В верхнее окно списком вводятся URL. Во второе окно вводится список xPath. Поиск информации осуществляется по всем путям на каждой странице.
Для каждого URL в списке создается отдельная задача, после этого все задачи запускаются на выполнение одновременно. Результат парсинга выводится в нижнем окне интерфейса и сохраняются в файле `result.txt`.

Данные для проверки работы программы:
- Список URL
https://www.chay.info/catalog/chay/angliyskiy_sadovnik.html
https://www.chay.info/catalog/kofe/turetskiy_myed.html
https://www.chay.info/catalog/kofe/martsipan.html
https://www.chay.info/catalog/kofe/lesnoy_orekh.html
https://www.chay.info/catalog/kofe/belgiyskie_vafli.html
https://www.chay.info/catalog/kofe/chokolato_latte_makkiato_.html

- Список xPath
//*[@id="product_name"]
//*[@id="product_price_current"]

#### Инструкция по запуску

- Клонировать репозиторий
```
git clone https://github.com/iurij-n/VT_test_2_2.git
```
- Создать виртуальное окружение
```
python -m venv venv
```
- Активировать виртуальное окружение
для Windows
```
source venv/Scripts/actevate
```
для Linux
```
source venv/bin/actevate
```
- Установить зависимости
```
pip install -r requrements.txt
```
- Запустить приложение
```
python pars_gui.py
```
