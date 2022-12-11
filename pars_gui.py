import asyncio
import os

import aiohttp
import jinja2
from lxml import html
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

TEMPLATE_FILE = "template.html"

all_data = []

Form, Window = uic.loadUiType('gui.ui')

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def clean_list(lst: list) -> list:
    '''
    Убирает пустые строки
    '''
    return [value for value in lst if len(value) > 3]


def save_as_pdf(data: list) -> None:
    '''
    Создает HTML-файл с результатами парсинга на основе шаблона jinja2,
    после этого преобразует полученный файл result.html в pdf.
    '''
    if os.name == 'posix':
        import weasyprint

    # Генерируем html-страницу на основе шаблона
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(TEMPLATE_FILE)
    output_text = template.render(data=data)

    # Сохраняем результат в файл result.html
    with open('result.html', 'w', encoding="utf-8") as file:
        file.write(output_text)

    # Конвертируем result.html в result.pdf
    pdf = weasyprint.HTML('result.html').write_pdf()
    with open('result.pdf', 'wb') as file:
        file.write(pdf)


def on_click():

    urls = clean_list(form.textEdit.toPlainText().split('\n'))
    xpaths = clean_list(form.textEdit_2.toPlainText().split('\n'))
    form.label_4.setText('')

    async def get_page_data(session, url, xpaths) -> str:
        async with session.get(url) as resp:
            try:
                resp_text = await resp.text()
                tree = html.fromstring(resp_text)
                data = []
                for xpath in xpaths:
                    raw_data = tree.xpath(xpath)
                    if raw_data != []:
                        text = raw_data[0].text
                        data.append(text)
                data_str = ";".join(data) + '\n'
                all_data.append(data_str)
            except Exception:
                print(f'Для URL - {url} не удалось собрать данные')
            return resp_text

    async def load_site_data():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(get_page_data(session, url, xpaths))
                tasks.append(task)
            await asyncio.gather(*tasks)

    asyncio.run(load_site_data())

    with open('result.txt', 'w', encoding="utf-8") as file:
        for data in all_data:
            form.textEdit_3.setText(''.join(all_data))
            file.write(data)
    if os.name == 'posix':
        save_as_pdf([line.split(';') for line in all_data])
    form.label_4.setText('Сбор данных окончен')


form.pushButton.clicked.connect(on_click)
app.exec_()
