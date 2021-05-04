# -*- coding: utf-8 -*-

##############
# Constants
##############
W_DEF = 'def'
W_FOR = 'for'

W_INT = 'int'
W_FLOAT = 'float'

W_PRINT = 'print'

##############
# Variables
##############
w_extendable = []
int_var = []
float_var = []
methods = []
var_name = []

############
# Classes
############
class Result:
    def __init__(self):
        """
        Result Success
        """
        pass

class Error:
    def __init__(self, error_name : str, error_msg : str):
        """
        Error
        """
        self.error_name = error_name
        self.error_msg = error_msg
    def getError(self) -> str:
        return f' >> {self.error_name} :\n        {self.error_msg}'

class NormalInstrRepr:
    def __init__(self, instr : str):
        self.instr = instr
    def getInstr(self) -> str:
        return self.instr

class ForRepr:
    def __init__(self, content : str, code_lines : list, start : int):
        self.content = content
        self.start = start

        self.code_lines = []
        temp = []
        num_sep = 1
        for i in range(len(code_lines)):
            if '{' in code_lines[i]:
                num_sep += 1
            elif '}' in code_lines[i]:
                num_sep -= 1
            if num_sep == 0:
                self.end = start + i
                self.code_lines = temp
                break
            temp.append(code_lines[i])
        
        if num_sep == 0:
            self.status = Result()
        else:
            self.status = Error('For Loop Error', 'For Loop Structure Not Found')
            self.code_lines = []
        
        self.update()
    
    def getContent(self) -> str:
        return self.content
    def getStart(self) -> int:
        return self.start
    def getEnd(self) -> int:
        return self.end
    def getStatus(self):
        return self.status
    def getCode(self) -> list:
        return self.code_lines
    def setCode(self, new_code : list):
        self.code_lines = new_code
    def update(self):
        self.code_lines = UpdateRepr.update(self.code_lines)

class MethodRepr:
    def __init__(self, name : str, code_lines : list, start : int):
        self.name = name
        self.start = start

        self.code_lines = []
        temp = []
        num_sep = 1
        for i in range(len(code_lines)):
            if '{' in code_lines[i]:
                num_sep += 1
            elif '}' in code_lines[i]:
                num_sep -= 1
            if num_sep == 0:
                self.end = start + i
                self.code_lines = temp
                break
            temp.append(code_lines[i])
        
        if num_sep == 0:
            self.status = Result()
        else:
            self.status = Error('Method Error', 'Method Structure Not Found')
            self.code_lines = []
        
        self.update()
    
    def getName(self) -> str:
        return self.name
    def getStart(self) -> int:
        return self.start
    def getEnd(self) -> int:
        return self.end
    def getStatus(self):
        return self.status
    def getCode(self) -> list:
        return self.code_lines
    def setCode(self, new_code : list):
        self.code_lines = new_code
    def update(self):
        self.code_lines = UpdateRepr.update(self.code_lines)

class UpdateRepr:
    """
    Update internal repr
    """
    def update(all_code_lines) -> list:
        out_res = []

        index = 0
        while index < len(all_code_lines):
            line = all_code_lines[index]
            already = False

            if hasKeyWord(line, W_FOR) and not already:
                line = line[len(W_FOR):len(line)]
                obj = ForRepr(line.replace('{',''), all_code_lines[index+1:len(all_code_lines)], index+1)
                if type(obj.getStatus()) == Result:
                    out_res.append(obj)
                    index = obj.getEnd()
                else:
                    print(obj.getStatus().getError())
                    break
                already = True
            elif not already and endLineRespected(line):
                line = line[0:-1]
                obj = NormalInstrRepr(line)
                out_res.append(obj)
                already = True
            
            index += 1
        
        return out_res

class IntVar:
    def __init__(self, name : str, value : int = 0):
        self.name = name
        self.value = value
    def setValue(self, value : int = 0):
        self.value = value
    def getValue(self) -> int:
        return self.value
    def getName(self) -> str:
        return self.name

class FloatVar:
    def __init__(self, name : str, value : float = 0.0):
        self.name = name
        self.value = value
    def setValue(self, value : float = 0.0):
        self.value = value
    def getValue(self) -> float:
        return self.value
    def getName(self) -> str:
        return self.name

############
# Methods
############
def hasKeyWord(line : str, keyword : str) -> bool:
    if line[0:len(keyword)] == keyword: 
        return True
    else: 
        return False

def endLineRespected(line : str) -> bool:
    if len(line) > 0:
        if line[-1] in ';^': 
            return True
        else:
            return False
    else:
        return False

def buildCode(all_code_lines : list):
    out_res = []
    bstatus = Result()

    index = 0
    while index < len(all_code_lines):
        line = all_code_lines[index]
        already = False

        if hasKeyWord(line, W_DEF) and not already:
            line = line[len(W_DEF):len(line)]
            obj = MethodRepr(line.replace(' ','').replace('{',''), all_code_lines[index+1:len(all_code_lines)], index+1)
            if type(obj.getStatus()) == Result:
                out_res.append(obj)
                index = obj.getEnd()
            else:
                print(obj.getStatus().getError())
                bstatus = Error('ERROR', 'CODE STRUCTURE ERROR')
                break
            already = True
        elif hasKeyWord(line, W_FOR) and not already:
            line = line[len(W_FOR):len(line)]
            obj = ForRepr(line.replace('{',''), all_code_lines[index+1:len(all_code_lines)], index+1)
            if type(obj.getStatus()) == Result:
                out_res.append(obj)
                index = obj.getEnd()
            else:
                print(obj.getStatus().getError())
                bstatus = Error('ERROR', 'CODE STRUCTURE ERROR')
                break
            already = True
        elif not already and endLineRespected(line):
            line = line[0:-1]
            obj = NormalInstrRepr(line)
            out_res.append(obj)
            already = True
        
        index += 1
    
    return out_res, bstatus

def intManage(line):
    if '=' in line:
        ls = line.split('=')
        name = ls[0].replace(' ','')
        isnamed = name in var_name
        if isnamed:
            return
        else:
            var_name.append(name)
            int_var.append(IntVar(name, int(ls[1])))

def floatManage(line):
    if '=' in line:
        ls = line.split('=')
        name = ls[0].replace(' ','')
        isnamed = name in var_name
        if isnamed:
            return
        else:
            var_name.append(name)
            float_var.append(FloatVar(name, float(ls[1])))

def printManage(line):
    if line[0] == '(':
        if line[len(line)-1] == ')':
            line = line[1:-1]
            if line[0] == '"' and line[len(line)-1] == '"':
                print(line[1:-1])
            elif line[0] == "'" and line[len(line)-1] == "'":
                print(line[1:-1])
            else:
                for i in int_var:
                    if i.getName() == line:
                        print(i.getValue())
                for i in float_var:
                    if i.getName() == line:
                        print(i.getValue())

def scanIf(main_obj):
    if type(main_obj[1]) == Error:
        print('  >>  >> This program has an error')
        main_obj[1].getError()
        return
    else:
        obj = main_obj[0]
        interpret(obj)

def interpret(code_obj):
    for obj in code_obj:
        run_code(obj)

def run_code(obj):
    if type(obj) == NormalInstrRepr:
        line = obj.getInstr().replace('\t','')
        if hasKeyWord(line, W_INT):
            line = line[len(W_INT):len(line)]
            intManage(line)
        elif hasKeyWord(line, W_FLOAT):
            line = line[len(W_FLOAT):len(line)]
            floatManage(line)
        elif hasKeyWord(line, W_PRINT):
            line = line[len(W_PRINT):len(line)]
            printManage(line)
