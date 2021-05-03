# -*- coding: utf-8 -*-

from src.core_src import buildCode, interpret, int_var, float_var

wanted_code = ['int a = 9;','float b = -31.17;']
builded = buildCode(wanted_code)
interpret(builded)

print(int_var[0].getName() + " " +str(int_var[0].getValue()))
print(float_var[0].getName() + " " + str(float_var[0].getValue()))
