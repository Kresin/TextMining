from transformers import BertTokenizer
import requests
import re
import csv
import json
from collections import namedtuple


def open_file(path):
    file = open(path, encoding="utf8")
    lines = file.readlines()
    return lines


def extract_cep_from_text(text):
    cep = re.findall("[0-9]{5}-[0-9]{3}", text)
    if not cep:
        return re.findall("[0-9]{8}", text)
    else:
        return cep


def call_cep_api(cep, lista):
    url = "http://viacep.com.br/ws/" + cep + "/json/"
    body = {}
    response = requests.request(url=url, params=body, method="get")
    x = response.json()
    for i in x:
        if (i == 'cep'):
            # print("encontrado cep")
            lista.append(x);
        if (i == 'erro'):
            print("cep com erro: " + cep)

    # print(x)

def write_csv(lista):
    fieldnames = [*lista[0]]
    with open('dados_enderecos.csv', 'w', encoding='UTF8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lista)

def main():
    content = open_file("./data_enderecos.txt")
    f = open('./endereco.csv', 'w', newline='', encoding='utf-8')
    lista = []

    for line in content:
        cep = extract_cep_from_text(line)
        if cep:
            call_cep_api(cep[0], lista)

    write_csv(lista)

def tokeninze(itens):
    PRE_TRAINED_MODEL_NAME = 'neuralmind/bert-base-portuguese-cased'
    tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

    for item in itens:
        tokens = tokenizer.tokenize(item)
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        print(f' Sentence: {item}')
        print(f' Tokens: {tokens}')
        print(f'Token IDs: {token_ids}')


main()
