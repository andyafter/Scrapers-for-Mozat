# -*- coding: utf-8 -*-
__author__ = 'mozat-pc'
import xml
import re

class TextHelper():
    def remove_tags(self, text):
        return ''.join(xml.etree.ElementTree.fromstring(text).itertext()).encode('ascii','ignore')


def lower_case_data(data):
    assert type(data) == str
    data = re.sub(r'\W', ' ', data)
    data = re.sub(r'\s+', ' ', data)
    data = data.lower().strip()
    return data

if __name__ == '__main__':
    textHelper = TextHelper()