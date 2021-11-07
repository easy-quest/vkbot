#!/usr/bin/env python
# -*- coding: utf-8 -*-
from translate import Translator

def trans():
    """Переводит текст"""
    translator = Translator(from_lang="English",to_lang="Russian")
    result = translator.translate(input('Введите текс перевода: '))
    print(result)