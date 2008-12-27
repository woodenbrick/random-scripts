#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import optparse
import string
import sys

class CyrillicLatin:
    def __init__(self, mangled_string, latin = True):
        self.latin_chars = u'a b c d e f g h i j k l m n o p q r s t u v x y z 6 4'.split()
        self.cyrillic_chars = u'а б с д е ф г х и ж к л м н о п я р с т у в х y з б ч'.split()
        self.latin_chars.append(' ')
        self.cyrillic_chars.append(' ')
        self.mangled_string = unicode(string.lower(mangled_string))
        self.ignore_startpoint = []
        self.delete_startpoint = []
        self.ignore_endpoint = []
        self.delete_endpoint = []
        self.hold_chars = ['s', 'y', 'c']
        self.hold_chars2 = ['sh', 'ya', 'yo']
        self.special_cases = {'sh' : u'ш', 'sht' : u'щ', 'you' : u'ю', 'ya' : u'я', 'ch' : u'ч'}
        
        
        
        if latin:
            self.convert_to_cyrillic()
        else:
            self.convert_to_latin()

    def ignore_between(self, start, end):
        '''Ignores chars between these, leaves them as is'''
        self.ignore_startpoint.append(start)
        self.ignore_endpoint.append(end)
        
    def delete_between(self, start, end):
        if start and end:
            self.delete_startpoint.append(start)
            self.delete_endpoint.append(end)
  
    def unhold(self):
        self.hold = False
        
    def append_chars(self, chars):
        if chars in self.special_cases:
            self.new_string.append(self.special_cases[chars])
        else:
            index = self.latin_chars.index(chars)
            self.new_string.append(self.cyrillic_chars[index])
    
    def check_holding_chars(self, current_char, temp_chars):
        
        if temp_chars is None:
            return current_char
        
        x = temp_chars + current_char
        if len(x) == 2:
            if x in self.hold_chars2:
                return x
            
            else:
                self.append_chars(temp_chars)
                if current_char in self.hold_chars:
                    return current_char
                else:
                    self.append_chars(current_char)
                    self.unhold()
                    return None
                
        
        elif len(x) == 3:
            if x in self.special_cases:
                self.append_chars(x)
                self.unhold()
                return None
            else:
                self.append_chars(temp_chars)
                if current_char in self.hold_chars:
                    return current_char
                else:
                    self.append_chars(current_char)
                
            
        
    def add_unknown_char(self, char, temp):
        self.append_chars(temp)
        self.new_string.append(char)
        self.unhold()
        return None
        

  
    def convert_to_cyrillic(self):
        self.hold = False
        self.new_string = []
        temp_chars = None
        for ch in self.mangled_string:
            try:
                index = self.latin_chars.index(ch)
                if ch in self.hold_chars:
                    self.hold = True
                    
                if self.hold is True:
                    temp_chars = self.check_holding_chars(ch, temp_chars)
                else:
                    self.new_string.append(self.cyrillic_chars[index])
                    
                    
            except ValueError:
                #the letter isnt in the list of latin letters, so just print as is.
                #this causes the problem of held characters being skipped, needs fix
                temp_chars = self.add_unknown_char(ch, temp_chars)
        return unicode(''.join(self.new_string))



def run():
    parser = optparse.OptionParser()
    parser.add_option('--input-file', '-i')
    parser.add_option('--output-file', '-o')
    parser.add_option('--delete-start', '-d')
    parser.add_option('--delete-end', '-e')
    options, args = parser.parse_args()
    #we require either a string or -i as input
    #if no -o, print to stdout
    if options.input_file is not None:
        convert_string = open(options.input_file, 'r').read()
    elif len(args) > 0:
        convert_string = ' '.join(args)
    else:
        sys.exit('please pass a string as an argument, or a file name with -i')

    convert = CyrillicLatin(convert_string)
    print options.delete_start, options.delete_end
    convert.delete_between(options.delete_start, options.delete_end)
    output = convert.convert_to_cyrillic()
    if options.output_file:
        output = output.encode('UTF-8')
        open(options.output_file, 'w').write(output + '\n')
    else:
        print output
        
def test_run():
    convert = CyrillicLatin('says: zdrasti')
    print convert.convert_to_cyrillic()
    
if __name__ == '__main__':
    run()
