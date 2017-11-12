# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# page = requests.get("http://submanga.com/Sankarea/completa")
# soup = BeautifulSoup(page.content, 'html.parser')
# text = soup.find_all('td', {'class': 's'})
# print(text)
# for tag in soup.findAll('a', href=True):
#     print(tag['href'])


import urllib.request
from re import findall


def get_imagenes_capitulo(url_imagenes, directorio):
    url_imagen = url_imagenes
    response = urllib.request.urlopen(url_imagen)
    html = response.read()
    htmlStr = html.decode()
    imagen = findall('src=[\'"]?([^\'" >]+)', htmlStr)
    imagen_url = imagen[6].split('/')
    del imagen_url[-1]
    imagen_base = '/'.join(str(e) for e in imagen_url)
    cant = 1
    for x in range(100):
        imagen_final = imagen_base + '/' + str(cant) + '.jpg'
        directorio_capitulo = directorio + '/' + str(cant) + '.jpg'
        print("DIrectorio", directorio_capitulo)
        try:
            urllib.request.urlretrieve(imagen_final, directorio_capitulo)
            cant += 1
            print(imagen_final)
        except:
            print("#" * 20, "IMAGEN NO EXISTE, ERROR", "#" * 20)
            break


def get_url_capitulo(url_completa, nombre_manga):
    url_manga = url_completa
    print("TIPO DE URL: ", type(url_manga))
    response = urllib.request.urlopen(url_manga)
    html = response.read()
    htmlStr = html.decode()
    pdata = findall('href=[\'"]?([^\'" >]+)', htmlStr)

    for item in pdata:
        # print("#"*20, "ITEM", "#"*20)
        # print(item)
        url_lista = item.split('/')


        if len(url_lista) > 5:
            directorio_actual = os.getcwd()
            print(directorio_actual)
            print(url_lista)
            print(str(url_lista[4]))
            directorio_capitulo = (str(directorio_actual) + '/' +
                                   nombre_manga+ '/' + str(url_lista[4]))

            if not os.path.exists(directorio_capitulo):
                os.makedirs(directorio_capitulo)
            else:
                continue

            page = requests.get(item)
            soup = BeautifulSoup(page.content, 'html.parser')
            text = soup.find_all('a', {'id': 'l'})
            text_url = str(text).split('href=')

            try:
                url_imagenes = text_url[1]
            except:
                url_imagenes = None
            if url_imagenes:
                url_imagenes = url_imagenes.split(' ')
                print('#' * 50)
                print(type(url_imagenes[0]))
                imagen_url = url_imagenes[0].strip('\'"')
                print(imagen_url, "Path")
                get_imagenes_capitulo(imagen_url, str(directorio_capitulo))


if __name__ == "__main__":

    url_completa = input("Ingrese la url del manga : ")
    nombre_manga = input("Ingrese nombre del manga : ")
    get_url_capitulo(str(url_completa), str(nombre_manga))

# get_url_capitulo("http://submanga.com/Sankarea/completa", "Sankarea")