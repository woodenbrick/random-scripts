#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import string

class CyrillicLatin:
    def __init__(self, mangled_string, latin = True):
        self.latin_chars = u'a b c d e f g h i j k l m n o p q r s t u v x z 6 4'.split()
        self.cyrillic_chars = u'а б с д е ф г х и ж к л м н о п я р с т у в я в х з б ч'.split()
        self.hold_chars = ['s', 'y', 'c']
        self.hold_chars2 = ['sh', 'ya', 'yo']
        self.special_cases = {'sh' : u'ш', 'sht' : u'щ', 'you' : u'ю', 'ya' : u'я', 'ch' : u'ч'}
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
  
    def convert_to_cyrillic(self, file_name = None):
        new_string = []
        previous_chars = []
        ignore = False
        delete = False
        hold_chars = []
        hold = False
        for ch in self.mangled_string:            
            if ch in self.ignore_startpoint:
                ignore = True
                new_string.append(ch)
                continue
                
            if ch in self.delete_startpoint:
                delete = True
                continue
            
            if ch in self.ignore_endpoint:
                ignore = False
                new_string.append(ch)
                continue
            
            if ch in self.delete_endpoint:
                delete = False
                continue
            
            if ignore is True:
                new_string.append(ch)
                continue
            
            if delete is True:
                continue
            
            
            if ch in string.whitespace:
                new_string.append(ch)
            else:
                try:
                    i = self.latin_chars.index(ch)
                    if hold is True:
                        hold_chars.append(ch)
                        if hold_chars in 
                    new_string.append(self.cyrillic_chars[i])
                    previous_chars.append(ch)
                except:
                    new_string.append('?')
        new_string = unicode(''.join(new_string))
        
        if file_name is None:
            return new_string
        
        else:
            output = open(file_name, 'w')
            output.write(new_string)
            
            

if __name__ == '__main__':
    convert_string = """
[05/12/2008 21:28:43] Boryana Kitina says: margoto shte vzima dve momcheta
[05/12/2008 21:28:51] Boryana Kitina says: i te q pitali shte ima li svobodni momicheta
[05/12/2008 21:28:55] Boryana Kitina says: a pak muri
[05/12/2008 21:29:05] Boryana Kitina says: shte sa napolovina momicheta napolovina momcheta
"""
    convert = CyrillicLatin(convert_string)
    convert.delete_between('[', ']')
    print(convert.convert_to_cyrillic())