# -*- coding: utf-8 -*-

from src.core_src import buildCode, runCode, int_var, float_var

file = open('test.txt','r',encoding='utf-8')
code_in = file.readlines()
file.close()
wanted_code = []
for i in code_in:
    wanted_code.append(i.replace('\n',''))
builded = buildCode(wanted_code)
runCode(builded)
