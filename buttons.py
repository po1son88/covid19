from bs4 import BeautifulSoup
from requests.models import Response
import requests
import datetime
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

em1 = '\N{nauseated face}'
em2 = '\N{coffin}'
em3 = '\N{flexed biceps}'
em4 = '\N{face with thermometer}'
em5 = '\N{bomb}'

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Статистика по Украине")
    keyboard.add(button_1)
    button_2 = types.KeyboardButton(text="Статистика по Запорожью")
    keyboard.add(button_2)
    await message.answer( f' {em5} Статистика COVID19 {em5}', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Статистика по Украине")
async def get_stats(message: types.Message):
    URL = 'https://www.worldometers.info/coronavirus/country/ukraine/'
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_inners = soup.find_all('div',class_= 'content-inner')
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
        await message.answer (
            # f'Статистика Covid19 по Украине'
            f'\n\n{em1} Всего заболевших: {content["cases"]}(+{content["cases1"]} за вчерашние сутки)' 
            f'\n{em2} Умерло: {content["deaths"]}(+{content["cases2"]} за вчерашние сутки)'
            f'\n{em3} Выздоровело: {content["recovered"]}'
            f'\n{em4} Болеет: {content["sick"]}'
        )

@dp.message_handler(lambda message: message.text == "Статистика по Запорожью")
async def get_stats(message: types.Message):
    URL = 'https://index.minfin.com.ua/reference/coronavirus/ukraine/zaporozhskaya/'
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_inners = soup.find_all('table', class_='line main-table')

    total_infections = soup.find('strong', class_='gold').get_text(strip = True)
    percent_total_infections = soup.find('td', class_='borderbottom black').get_text(strip = True)
    deaths_cases = soup.find('strong', class_='red').get_text(strip = True)
    percent_deaths_cases = soup.find_all('td', class_='gold')[0].get_text(strip = True)
    recovered_cases = soup.find('strong', class_='green').get_text(strip = True)
    percent_recovered_cases = soup.find_all('td', class_='gold')[1].get_text(strip = True)
    sick_now = soup.find('strong', class_='blue').get_text(strip = True)
    percent_sick_now = soup.find('td', class_='borderbottom gold').get_text(strip = True)

    contents = []
    
    for content_inner in content_inners:
        contents.append(
            {
                'cases': total_infections,
                'cases_percent': percent_total_infections,
                'deaths': deaths_cases,
                'deaths_percent': percent_deaths_cases,
                'recovered': recovered_cases,
                'recovered_percent': percent_recovered_cases,
                'sick': sick_now,
                'percent_sick': percent_sick_now
            }
        )
    for content in contents:
        await message.answer (
            f' Всего заражений: {content["cases"]} - {content["cases_percent"]}'
            f'\nСмертельные случаи: {content["deaths"]} - {content["deaths_percent"]}'
            f'\nВыздоровевшие: {content["recovered"]} - {content["recovered_percent"]}'
            f'\nСейчас болеют: {content["sick"]} - {content["percent_sick"]}'
        )    

if __name__ == '__main__':
    executor(executor.start_polling(dp))