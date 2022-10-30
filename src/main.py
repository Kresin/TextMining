import requests
import re
import csv

first_execution = True


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


def extract_house_number_from_text(text):
    number = ""
    found_number = False
    for char in text:
        if found_number is True and char.isnumeric() is False:
            break
        if char.isnumeric():
            number += char
            found_number = True
    return number


def extract_uf_from_text(text):
    uf = re.findall("\s[A-Z]{2}\s", text)
    return uf


def call_cep_api(cep):
    url = "http://viacep.com.br/ws/" + cep + "/json/"
    body = {}
    response = requests.request(url=url, params=body, method="get")
    print(response.json())
    return response.json()


def write_csv(json_data, line):
    with open('../files/enderecos.csv', 'a', newline='', encoding='utf-8') as file:
        # 2. cria o objeto de gravação
        file_writer = csv.writer(file)

        global first_execution
        if first_execution:
            file_writer.writerow(["logradouro", "número", "complemento", "bairro", "cidade", "uf", "cep"])
            first_execution = False

        # 3. grava as linhas
        if json_data is not None and "erro" not in json_data.keys():
            file_writer.writerow(
                [json_data["logradouro"], extract_house_number_from_text(line), json_data["complemento"],
                 json_data["bairro"],
                 json_data["localidade"], json_data["uf"], json_data["cep"]])
        else:
            found_comma = False
            city_whitespace = 0
            found_second_whitespace = False
            whitespace_total = 0
            bairro_whitespaces = 0
            rua = ""
            bairro = ""
            city = ""
            for char in line:
                # Obtendo o logradouro
                if char != "," and found_comma is False:
                    rua += char
                else:
                    # Fim do logradouro
                    found_comma = True
                    # Obtendo o bairro
                    if found_comma is True and char.isnumeric() is False and whitespace_total >= 3:
                        # Validação para bairro com nome composto. Ex: Vitor Konder
                        if char == " ":
                            bairro_whitespaces += 1
                        if bairro_whitespaces == 2:
                            # Fim do bairro
                            found_second_whitespace = True
                        else:
                            bairro += char
                    if char == " " and found_second_whitespace is False:
                        whitespace_total += 1
                        # O que sobrou é a cidade
                    elif found_second_whitespace is True:
                        if char == " ":
                            city_whitespace += 1
                        if city_whitespace == 2:
                            break
                        else:
                            city += char

            file_writer.writerow(
                [rua, extract_house_number_from_text(line), "", bairro, city, extract_uf_from_text(line)[0],
                 extract_cep_from_text(line)[0]])


def main():
    content = open_file("../files/data_enderecos.txt")
    for line in content:
        cep = extract_cep_from_text(line)
        if cep:
            json_data = call_cep_api(cep[0])
            write_csv(json_data, line)


main()
