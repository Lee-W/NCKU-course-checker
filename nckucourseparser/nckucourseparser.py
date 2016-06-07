import os
import json
import logging

import pandas as pd
from bs4 import BeautifulSoup


class NckuCourseParser(object):
    PARSE_FORMATS = ['dataframe', 'json']

    def __init__(self, html):
        self.html = html
        self._include_fields, self._exclude_fields = list(), list()

    def parse(self, parse_format='dataframe'):
        if parse_format not in NckuCourseParse.PARSE_FORMATS:
            raise NoSuchFormatError('Current only support json or dataframe')

        soup = BeautifulSoup(self.html)
        self.df = pd.read_html(str(soup.body.table))[0]

        if all(self.df['系所名稱'] == '查無課程資訊'):
            raise NoCourseAvailableError('No course available')

        if self.include_fields:
            self.df = self.df[self.include_fields]
        elif self.exclude_fields:
            self.df.drop(self.exclude_fields, axis=1, inplace=True)

        if parse_format == 'dataframe':
            return self.df
        elif parse_format == 'json':
            return self.df.to_dict(orient='records')

    def export(self, file_name, path='./course_result'):
        self.export_path = path
        self.file_name = file_name

        courses = self.parse('json')
        full_file_name = os.path.join(self.export_path, self.file_name)
        with open(full_file_name, 'w', encoding='utf-8') as export_file:
            json.dump(self.df.to_dict(orient='records'),
                      export_file,
                      ensure_ascii=False,
                      indent=4)

    @property
    def include_fields(self):
        return self._include_fields

    @include_fields.setter
    def include_fields(self, in_f):
        self._exclude_fields = list()

        self._include_fields = in_f

    @property
    def exclude_fields(self):
        return self._exclude_fields

    @exclude_fields.setter
    def exclude_fields(self, ex_f):
        self._include_fields = list()

        self._exclude_fields = ex_f

    @property
    def export_path(self):
        return self._export_path

    @export_path.setter
    def export_path(self, path):
        self._export_path = path
        if not os.path.exists(self.export_path):
            os.makedirs(self.export_path)
            logging.info("Create a directoty {}".format(self.export_path))

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, f_name):
        if os.path.splitext(f_name)[-1] != '.json':
            f_name += '.json'
        self._file_name = f_name


class NoCourseAvailableError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class NoSuchFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


if __name__ == '__main__':
    pass