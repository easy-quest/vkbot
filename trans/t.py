#!/usr/bin/env python
# -*- coding: utf-8 -*-
from translate import Translator

def trans():
    """Переводит текст"""
    translator = Translator(from_lang="Russian",to_lang="English")
    result = translator.translate(input('dfsdf: '))
    print(result)

def main():
    '''моя функция'''
    trans()

if __name__ == '__main__':
    main()
