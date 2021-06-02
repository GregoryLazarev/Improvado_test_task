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
        not_found_files = []
        for arg in self._args:
            if not os.path.isfile(arg):
                not_found_files.append(arg)
            elif not re.search(r'\w+\.(csv|xml|json)$', arg):
                wrong_args.append(arg)

        if len(wrong_args) > 0 or len(not_found_files) > 0:
            for wrong_arg in wrong_args:
                print(f'Invalid format of {wrong_arg}')
            for not_found in not_found_files:
                print(f'File {not_found} not found.')
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
                result_dict = dict(zip(headers, row))
                result.append(result_dict)
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

    def choose_strategy(self, file_format):
        if file_format == 'csv':
            self.set_strategy(Read_from_CSV)
        elif file_format == 'json':
            self.set_strategy(Read_from_json)
        elif file_format == 'xml':
            self.set_strategy(Read_from_xml)
        else:
            self.set_strategy(None)

    def read(self, file):
        file_format = file.split('.')[-1]
        self.choose_strategy(file_format)

        if self._strategy != None:
            data = self._strategy.read(self, file)
            return {'file_name': file, 'data': data}
        else:
            print(f'Unknown format {file_format}')


class Data_parser:
    def __init__(self) -> None:
        self.errors = []
        self.raw_data = []
        self.processed_data = []
        self.headers = []
        self.basic_out_file_name = 'basic.tsv'
        self.advanced_out_file_name = 'advanced.tsv'

    def get_data_from_files(self, files):
        headers_from_files = []
        for file in files:
            file_data = reader.read(file)
            self.raw_data.append(file_data)
            headers_from_files.append(list(file_data.get('data')[0].keys()))

        headers = headers_from_files[0]
        for header in headers_from_files:
            headers = list(set(headers) & set(header))
        headers.sort()
        self.headers = headers
        pass

    def parse(self):
        while len(self.raw_data) > 0:
            element = self.raw_data.pop(0)
            file_name = element.get('file_name')
            rows_from_file = element.get('data')
            num_of_rows = len(rows_from_file)
            for i in range(num_of_rows):
                row = []
                row_from_file = rows_from_file.pop(0)
                for header in self.headers:
                    row_element = row_from_file.get(header)
                    if re.match(r'M', header):
                        try:
                            row_element = (int(row_element))
                        except ValueError:
                            self.errors.append(f'Ошибка!\nФайл: {file_name}\nСтрока: {i+1}\nСтолбец: {header}\nНевозможно преобразовать данное значение в целочисленное\n\n')
                            continue
                    row.append(row_element)

                if len(row) == len(self.headers):
                    self.processed_data.append(row)
        self.processed_data.sort()

    def list_to_str(self, in_list, delimiter):
        result = ''
        for element in in_list:
                result += f'{str(element)}{delimiter}'
        return result[:-1]

    def write_to_file(self):
        with open(self.basic_out_file_name, 'w') as out_file:
            out_file.write(self.list_to_str(self.headers, '\t')+'\n')
            for element in self.processed_data:
                out_file.write(self.list_to_str(element, '\t')+'\n')


            # tsw_writer = csv.writer(out_file, delimiter='\t')
            # tsw_writer.writerow(self.headers)
            # tsw_writer.writerows(self.processed_data)

    def print_errors(self):
        for e in self.errors:
            print(e)


parser = Argument_parser()
file_names = parser.get_args()
reader = File_reader()
data_parser = Data_parser()

data_parser.get_data_from_files(file_names)
data_parser.parse()
data_parser.print_errors()
data_parser.write_to_file()
