import sys
import json
import os
import traceback


class JSONHandler:
    
    __slots__ = ['_text', '_tag_length', 'is_json']
    
    def __init__(self, json_text):
        self._text = json_text
        self._tag_length = dict()
        self.is_json = self._correct_form()
    
    def _correct_form(self):
        if type(self._text) != list or len(self._text) == 0:
            return False
        
        is_dicts = all(map(lambda subpackage: isinstance(subpackage, dict), self._text))
        if not is_dicts:
            return False
        
        title = self._text[0]
        tag = set(title.keys())
        print(tag)
        
        for contain in self._text:
            for key in tag:
                cur_len = len(contain[key])
                
                print(self._tag_length[key])
                if cur_len > self._tag_length[key]:
                    self._tag_length[key] = cur_len
        
        #for contain in self._tag_length:
        #TODO
        
        return True




def pretty_print(self):
    if not self.is_json:
        return
        
        separator = '|'
        separator_len = sum(self._tag_length.values()) + len(self._tag_length.values()) * 5 + 1
        print('-' * separator_len)
        
        tags = list(self._tag_length.keys())
        for current_tag in tags:
            print(separator + current_tag.center(self._tag_length[current_tag] + 4), end = '')
        print(separator)
        for d in self.json_text:
            for column in tags:
                if isinstance(d[column], float) or isinstance(d[column], int):
                    print(separator + ' ' * (2 + self._tag_length[column] - len(str(d[column]))) + str(d[column]) + ' ' * 2)
                else:
                    print(separator + ' ' * 2 + str(d[column]) + ' ' * (self._tag_length[column] - len(str(d[column])) + 2))
        print('-' * separator_len)

if __name__ == '__main__':
    filename = sys.argv[1]
    
    encoding_list = ['utf-8', 'utf-16', 'cp1251']
    
    try:
        with open(filename, 'rb') as file:
            flow_bytes = file.read()
    except FileNotFoundError:
        print(traceback.format_exc())
    #TODO
    
    for encode in encoding_list:
        try:
            flow_symbol = flow_bytes.decode(encode)
            break
        except UnicodeDecodeError:
            continue

    try:
        packet = json.loads(flow_symbol)
        handler = JSONHandler(packet)
    except json.decoder.JSONDecodeError:
        #packet = [line.strip().split('\t') for line in flow_symbol.split('\n') if line]
            #handler = TSVHandler()
        #except Exception:
        print(traceback.format_exc())


