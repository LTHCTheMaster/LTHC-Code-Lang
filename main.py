# -*- coding: utf-8 -*-

from src.core_src import buildCode, scanIf, int_var, float_var

wanted_code = ['int a = 9;','float b = -31.17;','print("Hello World!");',"print('Perfect');",'print(a);','print(b);']
builded = buildCode(wanted_code)
scanIf(builded)
