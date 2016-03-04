__author__ = 'mozat-pc'
import re

def process_tag_source_dic(tag_source):
    for key, text in tag_source.items():
        print key, text
        tag_source[key] = re.sub(r'\W', ' ', text)
    return tag_source
