from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import asyncio
import aiohttp
import pathlib
from lxml import html


here = pathlib.Path(__file__).parent
all_data = []

Form, Window = uic.loadUiType('gui.ui')

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def on_click():

    urls = form.textEdit.toPlainText().split('\n')
    xpaths = form.textEdit_2.toPlainText().split('\n')  
    form.label_4.setText('')

    async def get_page_data(session, url, xpaths) -> str:
        async with session.get(url) as resp:
            try:
                resp_text = await resp.text()
                tree = html.fromstring(resp_text)
                data = []
                for xpath in xpaths:
                    raw_data = tree.xpath(xpath)
                    if raw_data !=[]:
                        text = raw_data[0].text
                        data.append(text)
                data_str = ";".join(data) + '\n'
                all_data.append(data_str)
            except Exception:
                print('Не получилось')
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
    form.label_4.setText('Сбор данных окончен')
    print('Done')


form.pushButton.clicked.connect(on_click)
app.exec_()
