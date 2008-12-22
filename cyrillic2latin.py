#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import string

class CyrillicLatin:
    def __init__(self, mangled_string, latin = True):
        self.latin_chars = u'a b c d e f g h i j k l m n o p q r s t u v x z 6 4'.split()
        self.cyrillic_chars = u'а б с д е ф г х и ж к л м н о п я р с т у в я в х з б ч'.split()
        self.mangled_string = unicode(string.lower(mangled_string))
        self.ignore_startpoint = []
        self.delete_startpoint = []
        self.ignore_endpoint = []
        self.delete_endpoint = []
        
        if latin:
            self.convert_to_cyrillic()
        else:
            self.convert_to_latin()

    def ignore_between(self, start, end):
        '''Ignores chars between these, leaves them as is'''
        self.ignore_startpoint.append(start)
        self.ignore_endpoint.append(end)
        
    def delete_between(self, start, end):
        self.delete_startpoint.append(start)
        self.delete_endpoint.append(end)
  
  
    def should_we_hold(self):
        self.hold_chars = ['s', 'y', 'c']
        self.hold_chars2 = ['sh', 'ya', 'yo']
        self.special_cases = {'sh' : u'ш', 'sht' : u'щ', 'you' : u'ю', 'ya' : u'я', 'ch' : u'ч'}
        
        
    def convert_to_cyrillic(self, file_name = None):
        for ch in self.mangled_string:
            index = self.latin_chars.index(ch)
            print self.cyrillic_chars[index]

if __name__ == '__main__':
    convert_string = """momicheta shte beshe momicheta"""
    convert = CyrillicLatin(convert_string)
    convert.delete_between('[', ']')
    print(convert.convert_to_cyrillic())