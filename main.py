from bs4 import BeautifulSoup
from requests.models import Response
import requests
import datetime
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

em1 = '\N{nauseated face}'
em2 = '\N{coffin}'
em3 = '\N{flexed biceps}'
em4 = '\N{face with thermometer}'

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет. Это тестовый бот. Чтобы посмотреть, что он вывыодит напиши любые символы")

@dp.message_handler()
async def get_stats(message: types.Message):
    URL = 'https://www.worldometers.info/coronavirus/country/ukraine/'
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_inners = soup.find_all('div',class_= 'content-inner')
    # updates = soup.find_all ('li',class_= 'news_li')
    new_cases = soup.find_all('strong')[1].get_text(strip = True)
    new_cases = new_cases[:-10].replace(',','')
    new_deaths = soup.find_all('strong')[2].get_text(strip = True)
    new_deaths = new_deaths[:-11]

    cases1 = soup.find_all('div', class_='maincounter-number')[0].get_text(strip = True)
    cases1 = cases1.replace(',','')
    cases2 = soup.find_all('div', class_='maincounter-number')[1].get_text(strip = True)
    cases2 = cases2.replace(',','')
    cases3 = soup.find_all('div', class_='maincounter-number')[2].get_text(strip = True)
    cases3 = cases3.replace(',','')
    cases4 = int(cases1)-int(cases2)-int(cases3)
    # cases4 = int(cases1.replace(',','')) - int(cases2.replace(',','')) - int(cases3.replace(',',''))
    contents = []
    
    for content_inner in content_inners:
        contents.append(
            {
                'cases': cases1,
                'deaths': cases2,
                'recovered': cases3,
                'sick': cases4,
                'cases1': new_cases,
                'cases2': new_deaths
            }
        )
    for content in contents:
        await message.reply (
            f'Статистика Covid19 по Украине'
            f'\n\n{em1} Всего заболевших: {content["cases"]}(+{content["cases1"]} за вчерашние сутки)' 
            f'\n{em2} Умерло: {content["deaths"]}(+{content["cases2"]} за вчерашние сутки)'
            f'\n{em3} Выздоровело: {content["recovered"]}'
            f'\n{em4} Болеет: {content["sick"]}'
        )

if __name__ == '__main__':
    executor(executor.start_polling(dp))