# -*- coding: utf-8 -*- #
import re
from bs4 import BeautifulSoup as bs
import os
import time

ENC = 'utf-8' #output file encoding

output = ''
slide = 1
title = ''
temp_title = ''
max_slide = 1

LOG = []
ACCEPT_LOG = True
ESC = False

dir = os.path.dirname(__file__)
LOG.append(os.listdir(dir))
try:
    path = dir + '\\' + [x[1] for x in os.walk(dir)][0][0]
    print('Путь найден: {}'.format(path))
except Exception as e:
    LOG.append(e)
    print('Папка не найдена. Вы уверены, что это единственная папка в этой директории?')
    print('Логи записаны в файл logs.\nПо умолчанию: Включено. Отключить можно в строке 16')
    ESC = True
while True:
    if ESC == True:
        break
    try:
        f = open(path + '\\' + 'slide{}.js.Без названия'.format(slide), 'r', encoding='utf-8')
        slide += 1
    except FileNotFoundError:
        max_slide = slide
        LOG.append('Всего файлов импортировано: {}'.format(max_slide-1))
        slide = 1
        break

while slide < max_slide:
    data = ''
    if slide%2 == 0:
        print('{}%'.format(int((slide/(max_slide-1))*100)))
    f = open(path + '\\' + 'slide{}.js.Без названия'.format(slide), 'r', encoding='utf-8')
    for l in f:
        data += l
    f.close()
    line = ''
    soup = bs(data, 'html.parser')
    spans = soup.find_all('span')

    for s in spans:
        line += s.text + ' '
    res = re.search(r'[а-яА-Я:)]\s{1}\d+\s+[А-Яа-я0-9]', line)
    LOG.append('Обработка строки: {}\n {}'.format(slide, res))
    if slide == 1:
        ty = line[0:line.find(':')+ 2].strip()
        r = re.search(r'[а-яА-Я:)]\s+\d+\s+', line[0:-1])
        title = line[0:r.end()]
        print(title)
        r = re.search(r'[а-яА-Я:)]\s+\d\s+', line[0:-1])
        LOG.append(line.replace(line[r.start()+1:r.end()], ': \n', 1) + '\n\n')
        output += line.replace(line[r.start()+1:r.end()], ': \n', 1) + '\n'
        LOG.append('Название файла -- {}'.format(title[0:title.find('Тема ')+ 9].replace('\n', '').strip().replace('  ', ' ').replace('.', '').replace('   ', ' ')))
        slide += 1
    else:
        try:
            r = re.search(r'[а-яА-Я:)]\s+\d+\s+', line[0:res.end()-1])
            line = '\n' + line[0:r.start()+2] + ':\n' + line[res.end()-1:-1].replace('   ', ' ')
            line = '\n' + line[0:r.start() + 2] + ':\n' + line[res.end() - 1:-1].replace('   ', ' ')
        except Exception as e:
            LOG.append(e)
            pass
        try:
            ty = line[0:res.end()-1].strip()
        except:
            ty = line[0:line.find(':')+ 2].strip()
            LOG.append('Не получилось получить временный заголовок с помощью regular expressions.')
        print('---------------------------------------')
        if temp_title != ty:
            temp_title = ty
            LOG.append('Временный заголовок: "{}"'.format(ty))
            print(ty)
        else:
            LOG.append('Временный заголовок: "{}"'.format(ty))
            LOG.append('Повтор заголовка. Идёт замена.')
            line = line.replace(temp_title, '').replace('\n\n\n\n', '\n\n').replace('\n\n\n', '\n\n')
        output += line + '\n'
        LOG.append(line + '\n\n')
        slide += 1

if ACCEPT_LOG == True:
    st = time.strftime("%a, %d %b %Y %H:%M:%S")
    t = open('{}'.format('logs'), 'w', encoding=ENC)
    t.write(st + '\n')
    for li in LOG:
        t.write(str(li) + '\n')
    t.close()

if ESC == False:
    output = output.strip('\n')
    filename = title[0:title.find('Тема ')+ 9].replace('\n', '').strip().replace('  ', ' ').replace('.', '').replace(':', '').replace('   ', ' ')
    print('Файл "{0}.txt" записан.\nКодировка:{1}\nСменить кодировку можно в строке 7'.format(filename, ENC))
    if ACCEPT_LOG == True:
        print('Логи записаны в файл logs.\nПо умолчанию: Включено. Отключить можно в строке 16')
    t = open('{}.txt'.format(filename), 'w', encoding=ENC)
    try:
        t.write(output)
    except UnicodeDecodeError:
        print('---------------------------------------\nОшибка кодировки')
    t.close()
