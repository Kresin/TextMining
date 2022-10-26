from transformers import BertTokenizer
import requests
import re
import csv


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


def call_cep_api(cep):
    url = "http://viacep.com.br/ws/" + cep + "/json/"
    body = {}
    response = requests.request(url=url, params=body, method="get")
    print(response.json())


def write_csv():
    f = open('numero_dobro_triplo.csv', 'w', newline='', encoding='utf-8')

    # 2. cria o objeto de gravação
    w = csv.writer(f)

    # 3. grava as linhas
    for i in range(5):
        w.writerow([i, i * 2, i * 3])


def main():
    content = open_file("./data_enderecos.txt")
    for line in content:
        cep = extract_cep_from_text(line)
        if cep:
            call_cep_api(cep[0])


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
