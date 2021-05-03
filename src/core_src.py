# -*- coding: utf-8 -*-

##############
# Constants
##############
W_DEF = 'def'
W_FOR = 'for'

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
            print('Expected \';\' at the end of a normal instruction line')
            return False
    else:
        return True

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
