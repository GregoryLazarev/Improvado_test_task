import argparse
import re
from abc import ABC, abstractmethod
import csv
import json
import os
from typing import List
import xml.etree.ElementTree as ET

class Argument_parser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', nargs='+')
        args = parser.parse_args()
        self._args = args.file


    def validate_args(self):
        wrong_args = []
        for arg in self._args:
            if not re.search(r'\w+\.(csv|xml|json)$', arg):
                wrong_args.append(arg)

        if len(wrong_args) > 0:
            for wrong_arg in wrong_args:
                print(f'Invalid format of {wrong_arg}')
            os._exit(1)

        
    def get_args(self):
        self.validate_args()
        return self._args


class ReaderStrategy(ABC):
    @abstractmethod
    def read(self, file) -> List:
        pass


class Read_from_CSV(ReaderStrategy):
    def read(self, file) -> List:
        result = []
        with open(file) as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            headers = next(data)
            for row in data:
                d = dict(zip(headers, row))
                result.append(d)
        return result


class Read_from_json(ReaderStrategy):
    def read(self, file) -> List:
        result = []
        with open(file) as json_file:
            data = json.load(json_file)
            result = data.get('fields')
        return result


class Read_from_xml(ReaderStrategy):
    def read(self, file) -> List:
        result = []
        tree = ET.parse(file)
        root = tree.getroot()

        for objects in root:
            data = {}
            for object in objects:
                key = (object.attrib.get('name'))
                value = (object[0].text)
                data.update({key: value})
            result.append(data)
        return result


class File_reader:
    def set_strategy(self, strategy: ReaderStrategy):
        self._strategy = strategy

    def read(self, file):
        file_format = file.split('.')[-1]

        # Выбор стратегии в зависимости от формата входного файла
        if file_format == 'csv':
            self.set_strategy(Read_from_CSV)
        elif file_format == 'json':
            self.set_strategy(Read_from_json)
        elif file_format == 'xml':
            self.set_strategy(Read_from_xml)
        else:
            self.set_strategy(None)

        # Если нет нужного обработчика формата, вывести ошибку.
        if self._strategy != None:
            return self._strategy.read(self, file)
        else:
            print(f'Unknown format {file_format}')


class Validator:
    def __init__(self) -> None:
        self.errors = []

    def Validate(self, data, file_name):
        pass


CSV_F = 'csv_data_1.csv'
JSON_F = 'json_data.json'
XML_F = 'xml_data.xml'
# reader = File_reader()
# r = reader.read(XML_F)
# print(r)
parser = Argument_parser()
parser.get_args()
# try:
#     print(int('v'))
# except ValueError:
#     print('Введена буква')
