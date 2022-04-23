import argparse
import xml.etree.ElementTree as ET
import re
import sys

instructions = []
toExecute = ""

VAR_reg = re.compile(r"^(LF|GF|TF)@[a-zA-Z_\-#$&%*!?][a-zA-Z_\-#$&%*!?$0-9]*$")
LABEL_reg = re.compile(r"^[a-zA-Z_\-#$&%*!?][a-zA-Z_\-#$&%*!?$0-9]+$")

GF = {}
LF = {"NONE" : "none"}
TF = {"NONE" : "none"}
LF_list = []
isCreateFrame = False
isLF = False
isFirst = True
label_dict = {}
global_order = -1
stack = []
call_stack = []
canpop = False
linecount = 0
toRead = []
argcounter = 1


def isEmpty(toCheck, frame = 'nothing'):
    if frame == 'GF':
        if type(GF[toCheck]) != bool and type(GF[toCheck]) != int:
            if not GF[toCheck]:
                print('is empty')
                sys.exit(56)
    elif frame == 'TF':
        if type(TF[toCheck]) != bool and type(TF[toCheck]) != int:
            if not TF[toCheck]:
                print('is empty')
                sys.exit(56)
    elif frame == 'LF':
        if type(LF[toCheck]) != bool and type(LF[toCheck]) != int:
            if not LF[toCheck]:
                print('is empty')
                sys.exit(56)
    else:
        if type(toCheck) != bool and type(toCheck) != int:
            if not toCheck:
                print('is empty')
                sys.exit(56)

def char_isEmpty(toCheck, frame = 'noothing'):
    if frame == 'GF':
        if type(GF[toCheck]) != bool and type(GF[toCheck]) != int:
            if GF[toCheck]== '#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪':
                print('string is empty')
                sys.exit(58)
    elif frame == 'TF':
        if type(TF[toCheck]) != bool and type(TF[toCheck]) != int:
            if TF[toCheck] == '#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪':
                print('string is empty')
                sys.exit(58)
    elif frame == 'LF':
        if type(LF[toCheck]) != bool and type(LF[toCheck]) != int:
            if LF[toCheck] == '#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪':
                print('string is empty')
                sys.exit(58)
    else:
        if type(toCheck) != bool and type(toCheck) != int:
            if toCheck == '#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪':
                print('string is empty')
                sys.exit(58)

def stack_isEpmty(toCheck, frame = 'nothing'):
    if frame == 'GF':
        if type(GF[toCheck]) != bool and type(GF[toCheck]) != int:
            if not GF[toCheck]:
                print('pushing empty to stack')
                sys.exit(56)
    elif frame == 'TF':
        if type(TF[toCheck]) != bool and type(TF[toCheck]) != int:
            if not TF[toCheck]:
                print('pushing empty to stack')
                sys.exit(56)
    elif frame == 'LF':
        if type(LF[toCheck]) != bool and type(LF[toCheck]) != int:
            if not LF[toCheck]:
                print('pushing empty to stack')
                sys.exit(56)
    else:
        if type(toCheck) != bool and type(toCheck) != int:
            if not toCheck:
                print('pushing empty to stack')
                sys.exit(56)

def change_before_write(toChange):
    if type(toChange) == str:
        toChange = toChange.replace('#¶!©y←5§iðo<ì♪!©y←5§inil', '')
        toChange = toChange.replace('#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪', '')
    if type(toChange) == bool:
        toChange = str(toChange)
        toReturn = re.sub('True', 'true', toChange)
        toReturn = re.sub('False', 'false', toReturn)
        return toReturn
    else:
        return toChange
    

def replace(match):
    return chr(int(match.group(1)))

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# CHECKS
def split_if_at(toSplit):
    tmp = toSplit.split('@')
    if '@' not in toSplit:
        tmp.append('nothing useful')
    return tmp

def check_symbol(toCheck):
    if toCheck[1]:
        toCheck[1] = str(toCheck[1])
        if re.match(r'^int$', toCheck[1]):
            if str(toCheck[2]):
                toCheck[2] = str(toCheck[2])
                if re.match(r'^[+-]?[0-9]+$', toCheck[2]):
                    toCheck[2] = int(toCheck[2])
                    return 1
        elif re.match(r'^bool$', toCheck[1]):
            if str(toCheck[2]):
                toCheck[2] = str(toCheck[2])
                if re.match(r'^(true|false)$', toCheck[2].lower()):
                    if toCheck[2].lower() == 'true':
                        toCheck[2] = True
                    elif toCheck[2].lower() == 'false':
                        toCheck[2] = False
                    else:
                        toCheck[2] = bool(toCheck[2])
                    return 1
        elif re.match(r'^nil$', toCheck[1]):
            if toCheck[2]:
                toCheck[2] = str(toCheck[2])
                if re.match(r'^nil$', toCheck[2]):
                    toCheck[2] = '#¶!©y←5§iðo<ì♪!©y←5§inil'
                    return 1
        elif re.match(r'^string$', toCheck[1]):
            if toCheck[2]:
                toCheck[2] = str(toCheck[2])
                if re.match(r'^(((\\[0-9][0-9][0-9])+)|([^#\\\\\s])+)*$', toCheck[2]):
                    text = toCheck[2]
                    regex = re.compile(r"\\(\d{1,3})")
                    toCheck[2] = regex.sub(replace, text)
            else:
                toCheck[2] = "#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪"
            return 1
        elif re.match(r'^var$', toCheck[1]):
            if toCheck[2]:
                toCheck[2] = str(toCheck[2])
                if re.match(r'(^(LF|GF|TF)@[a-zA-Z_\-#$&%*!?][a-zA-Z_\-#$&%*!?$0-9]*$)', toCheck[2]):
                    return 1
    return 0

def check_in_frame(toCheck, frame):
    if frame == 'GF':
        if toCheck not in GF:
            print('Var not in GF')
            sys.exit(54)
    elif frame == 'TF':
        if not isCreateFrame:
            print('TF does not exist')
            sys.exit(55)
        if toCheck not in TF:
            print('Var not in TF')
            sys.exit(54)
    else:
        if not isLF:
            print('LF does not exist')
            sys.exit(55)
        if toCheck not in LF:
            print('Var not in LF')
            sys.exit(54)

def check_if_zero(toCheck, frame='other'):
    if frame == 'GF':
        if GF[toCheck] == 0:
            print('DIVISION BY ZERO')
            sys.exit(57)
    elif frame == 'TF':
        if TF[toCheck] == 0:
            print('DIVISION BY ZERO')
            sys.exit(57)
    elif frame == 'LF':
        if LF[toCheck] == 0:
            print('DIVISION BY ZERO')
            sys.exit(57)
    else:
        if toCheck == 0:
            print('DIVISION BY ZERO')
            sys.exit(57)

def check_boolean(toCheck, frame = 'other'):
    if frame == 'GF':
        if type(GF[toCheck]) != bool and type(GF[toCheck]) != int:
            if not GF[toCheck]:
                print('No value in GF['+toCheck+']')
                sys.exit(56)
        if GF[toCheck] != True and GF[toCheck] != False:
            print('NOT BOOLEAN')
            sys.exit(53)
        if type(GF[toCheck]) == int:
            print('NOT BOOLEAN')
            sys.exit(53)
    elif frame == 'TF':
        if type(TF[toCheck]) != bool and type(TF[toCheck]) != int:
            if not TF[toCheck]:
                print('No value in TF['+toCheck+']')
                sys.exit(56)
        if TF[toCheck] != True and TF[toCheck] != False:
            print('NOT BOOLEAN')
            sys.exit(53)
        if type(TF[toCheck]) == int:
            print('NOT BOOLEAN')
            sys.exit(53)
    elif frame == 'LF':
        if type(LF[toCheck]) != bool and type(LF[toCheck]) != int:
            if not LF[toCheck]:
                print('No value in LF['+toCheck+']')
                sys.exit(56)
        if LF[toCheck] != True and LF[toCheck] != False:
            print('NOT BOOLEAN')
            sys.exit(53)
        if type(LF[toCheck]) == int:
            print('NOT BOOLEAN')
            sys.exit(53)
    else:
        if type(toCheck) != bool:
            if not toCheck:
                print('No value in bool')
                sys.exit(56)
            print('NOT BOOLEAN')
            sys.exit(53)
        if type(toCheck) == int:
            if not toCheck:
                    print('No value in bool')
                    sys.exit(56)
            print('NOT BOOLEAN')
            sys.exit(53)

def check_int(toCheck, frame = 'other'):
    if frame == 'GF':
        if type(GF[toCheck]) != bool and type(GF[toCheck]) != int:
            if not GF[toCheck]:
                print('No value in GF['+toCheck+']')
                sys.exit(56)
        if type(GF[toCheck]) != int:
            print('NOT INT')
            sys.exit(53)
    elif frame == 'TF':
        if type(TF[toCheck]) != bool and type(TF[toCheck]) != int:
            if not TF[toCheck]:
                print('No value in TF['+toCheck+']')
                sys.exit(56)
        if type(TF[toCheck]) != int:
            print('NOT INT')
            sys.exit(53)
    elif frame == 'LF':
        if type(LF[toCheck]) != bool and type(LF[toCheck]) != int:
            if not LF[toCheck]:
                print('No value in LF['+toCheck+']')
                sys.exit(56)
        if type(LF[toCheck]) != int:
            print('NOT INT')
            sys.exit(53)
    else:
        if type(toCheck) != bool and type(toCheck) != int:
            if not toCheck:
                print('No value in int')
                sys.exit(56)
        if type(toCheck) != int:
            print('NOT INT')
            sys.exit(53)

def check_str(toCheck, frame = 'other'):
    if frame == 'GF':
        if type(GF[toCheck]) != bool and type(GF[toCheck]) != int:
            if not GF[toCheck]:
                print('No value in GF['+toCheck+']')
                sys.exit(56)
        if type(GF[toCheck]) != str:
            print('NOT STR')
            sys.exit(53)
        check_nil(GF[toCheck])
    elif frame == 'TF':
        if type(TF[toCheck]) != bool and type(TF[toCheck]) != int:
            if not TF[toCheck]:
                print('No value in TF['+toCheck+']')
                sys.exit(56)
        if type(TF[toCheck]) != str:
            print('NOT STR')
            sys.exit(53)
        check_nil(TF[toCheck])
    elif frame == 'LF':
        if type(LF[toCheck]) != bool and type(LF[toCheck]) != int:
            if not LF[toCheck]:
                print('No value in LF['+toCheck+']')
                sys.exit(56)
        if type(LF[toCheck]) != str:
            print('NOT STR')
            sys.exit(53)
        check_nil(LF[toCheck])
    else:
        if type(toCheck) != bool and type(toCheck) != int:
            if not toCheck:
                print('No value in str')
                sys.exit(56)
        if type(toCheck) != str:
            print('NOT STR')
            sys.exit(53)
        check_nil(toCheck)

def check_type(toCheck1, toCheck2):
    if type(toCheck1) != type(toCheck2):
        if not str(toCheck1) or not str(toCheck2):
                print('No values')
                sys.exit(56)
        print('not same types')
        sys.exit(53)

def check_nil(toCheck):
    if toCheck == '#¶!©y←5§iðo<ì♪!©y←5§inil':
        if not str(toCheck):
                print('No value')
                sys.exit(56)
        print("is nil")
        sys.exit(53)

def is_nil(toCheck):
    if toCheck == '#¶!©y←5§iðo<ì♪!©y←5§inil':
        return True
    else:
        return False

def get_order_of_label(label):
    for i in instructions:
        if label in label_dict:
            return label_dict[label]
        else:
            if i.name == 'LABEL':
                if i.args[0][2] == label:
                    label_dict[label] = i.order
                    return i.order
    return -1

def jump_fnc(toCheck):
    tmp = get_order_of_label(toCheck)
    if tmp == -1:
        print('label not defined')
        sys.exit(52)
    else:
        return tmp

class CHECK_NONE:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if self.args:
            print('check non error')
            sys.exit(32)

class CHECK_LABEL:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 1:
            if self.args[0][1] and self.args[0][2]:
                if re.match(r'^label$',self.args[0][1]) and re.match(LABEL_reg, self.args[0][2]):
                    return
        print('check label error')
        sys.exit(32)

class CHECK_VAR:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 1:
            if self.args[0][1] and self.args[0][2]:
                if re.match(VAR_reg, self.args[0][2]) and re.match(r'^var$',self.args[0][1]):
                    return
        print('check var error')
        sys.exit(32)
            
class CHECK_SYMB:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 1:
            if check_symbol(self.args[0]):
                return
        print('check symb error')
        sys.exit(32)

class CHECK_VAR_TYPE:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 2:
            if self.args[0][1] and self.args[0][2] and self.args[1][1] and self.args[1][2]:
                if re.match(VAR_reg, self.args[0][2]) and re.match(r'^var$',self.args[0][1]) and re.match(r'^type$', self.args[1][1]) and re.match(r'^(int|string|bool)$', self.args[1][2]):
                    return
        print('check var type error')
        sys.exit(32)

class CHECK_VAR_SYMB:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 2:
            if self.args[0][1] and self.args[0][2]:
                if re.match(VAR_reg, self.args[0][2]) and re.match(r'^var$',self.args[0][1]) and check_symbol(self.args[1]):
                    return
        print('check var symb error')
        sys.exit(32)

class CHECK_VAR_SYMB_SYMB:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 3:
            if self.args[0][1] and self.args[0][2]:
                if re.match(VAR_reg, self.args[0][2]) and re.match(r'^var$',self.args[0][1]) and check_symbol(self.args[1]) and check_symbol(self.args[2]):
                    return
        print('check var symb symb error')
        sys.exit(32)

class CHECK_LABEL_SYMB_SYMB:
    def __init__(self, args):
        self.args = args
        self.check()
    def check(self):
        if len(self.args) == 3:
            if self.args[0][1] and self.args[0][2]:
                if re.match(LABEL_reg, self.args[0][2]) and re.match(r'^label$',self.args[0][1]) and check_symbol(self.args[1]) and check_symbol(self.args[2]):
                    return
        print('check label symb symb error')
        sys.exit(32)

# FUNCTIONS
class CREATEFRAME:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_NONE(self.args)
        global isCreateFrame
        global canpop
        TF.clear()
        isCreateFrame = True
        canpop = False

class PUSHFRAME:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_NONE(self.args)
        global isCreateFrame
        global canpop
        global isLF
        isLF = True
        if isCreateFrame == True:
            global LF
            global TF
            global isFirst
            if isFirst:
                LF.clear()
                isFirst = False
            else:
                LF_list.append(LF)
            LF = TF.copy()
            TF.clear()
        else:
            print("ERROR, no CREATEFAME before PUSHFRAME")
            sys.exit(55)
        isCreateFrame = False
        canpop = True

class POPFRAME:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_NONE(self.args)
        global LF
        global LF_list
        global TF
        global isLF
        global isCreateFrame
        global canpop
        if LF_list and isLF:
            TF.clear()
            TF = LF.copy()
            LF = LF_list[0].copy()
            LF_list.pop()
        elif isLF:
            TF.clear()
            TF = LF.copy()
            isLF = False
        else:
            print("POPFRAME ERROR")
            sys.exit(55)
        if not canpop:
            print("POPFRAME ERROR")
            sys.exit(55)
        isCreateFrame = True

class RETURN:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_NONE(self.args)
        global inst
        if not call_stack:
            sys.exit(56)
        inst = call_stack.pop()
        

class BREAK:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_NONE(self.args)
        eprint("GF: {}".format(GF))
        eprint("TF: {}".format(TF))
        eprint("LF: {}".format(LF))
        eprint("LF STACK: {}".format(LF_list))
        eprint("LABEL DICT: {}".format(label_dict))
        eprint("CALL STACK: {}".format(call_stack))

class DEFVAR:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR(self.args)
        tmp = split_if_at(self.args[0][2])
        if tmp[0] == 'TF':
            try:
                if TF['NONE'] == 'none':
                    print('no TF')
            except:
                pass
            else:
                sys.exit(55)

        if tmp[0] == 'LF':
            try:
                if LF['NONE'] == 'none':
                    print('no LF')
            except:
                pass
            else:
                sys.exit(55)

        exec('if tmp[1] in ' + tmp[0] + ':\n\tprint("redefinition of variable")\n\tsys.exit(52)\n'+ tmp[0] + '[tmp[1]] = ""')


class POPS:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR(self.args)
        if not stack:
            print('stack is empty')
            sys.exit(56)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        exec(tmp[0] + '[tmp[1]] = stack.pop()')

class ADD:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_int(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(tmp3[1], tmp3[0])
                exec(tmp[0] + '[tmp[1]] = ' + tmp2[0] + '[tmp2[1]] + ' + tmp3[0] +'[tmp3[1]]')
            else:
                if self.args[2][1] == 'int':
                    check_int(self.args[2][2])
                    exec(tmp[0] + '[tmp[1]] = ' + tmp2[0] + '[tmp2[1]] + self.args[2][2]')
                else:
                    sys.exit(53)
        else:
            if self.args[2][1] == 'var':
                if self.args[1][1] == 'int':
                    check_int(self.args[1][2])
                    tmp3 = split_if_at(self.args[2][2])
                    check_in_frame(tmp3[1], tmp3[0])
                    check_int(tmp3[1], tmp3[0])
                    exec(tmp[0] + '[tmp[1]] = self.args[1][2] + ' + tmp3[0] +'[tmp3[1]]')
                else:
                    sys.exit(53)
            else:
                if self.args[1][1] == 'int' and self.args[2][1] == 'int':
                    check_int(self.args[1][2])
                    check_int(self.args[2][2])
                    exec(tmp[0] + '[tmp[1]] = self.args[1][2] + self.args[2][2]')
                else:
                    sys.exit(53)
        
class SUB:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_int(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(tmp3[1], tmp3[0])
                exec(tmp[0] + '[tmp[1]] = ' + tmp2[0] + '[tmp2[1]] - ' + tmp3[0] +'[tmp3[1]]')
            else:
                if self.args[2][1] == 'int':
                    check_int(self.args[2][2])
                    exec(tmp[0] + '[tmp[1]] = ' + tmp2[0] + '[tmp2[1]] - self.args[2][2]')
                else:
                    sys.exit(53)
        else:
            if self.args[2][1] == 'var':
                if self.args[1][1] == 'int':
                    check_int(self.args[1][2])
                    tmp3 = split_if_at(self.args[2][2])
                    check_in_frame(tmp3[1], tmp3[0])
                    check_int(tmp3[1], tmp3[0])
                    exec(tmp[0] + '[tmp[1]] = self.args[1][2] - ' + tmp3[0] +'[tmp3[1]]')
                else:
                    sys.exit(53)
            else:
                if self.args[1][1] == 'int' and self.args[2][1] == 'int':
                    check_int(self.args[1][2])
                    check_int(self.args[2][2])
                    exec(tmp[0] + '[tmp[1]] = self.args[1][2] - self.args[2][2]')
                else:
                    sys.exit(53)
        

class MUL:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_int(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(tmp3[1], tmp3[0])
                exec(tmp[0] + '[tmp[1]] = ' + tmp2[0] + '[tmp2[1]] * ' + tmp3[0] +'[tmp3[1]]')
            else:
                if self.args[2][1] == 'int':
                    check_int(self.args[2][2])
                    exec(tmp[0] + '[tmp[1]] = ' + tmp2[0] + '[tmp2[1]] * self.args[2][2]')
                else:
                    sys.exit(53)
        else:
            if self.args[2][1] == 'var':
                if self.args[1][1] == 'int':
                    check_int(self.args[1][2])
                    tmp3 = split_if_at(self.args[2][2])
                    check_in_frame(tmp3[1], tmp3[0])
                    check_int(tmp3[1], tmp3[0])
                    exec(tmp[0] + '[tmp[1]] = self.args[1][2] * ' + tmp3[0] +'[tmp3[1]]')
                else:
                    sys.exit(53)
            else:
                if self.args[1][1] == 'int' and self.args[2][1] == 'int':
                    check_int(self.args[1][2])
                    check_int(self.args[2][2])
                    exec(tmp[0] + '[tmp[1]] = self.args[1][2] * self.args[2][2]')
                else:
                    sys.exit(53)
        

class IDIV:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_int(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(tmp3[1], tmp3[0])
                check_if_zero(tmp2[1], tmp2[0])
                GF[tmp[1]] = int(GF[tmp2[1]] / GF[tmp3[1]])
            else:
                if self.args[2][1] == 'int':
                    check_int(self.args[2][2])
                    check_if_zero(self.args[2][2])
                    GF[tmp[1]] = int(GF[tmp2[1]] / self.args[2][2])
                else:
                    sys.exit(53)
        else:
            if self.args[2][1] == 'var':
                if self.args[1][1] == 'int':
                    check_int(self.args[1][2])
                    tmp3 = split_if_at(self.args[2][2])
                    check_in_frame(tmp3[1], tmp3[0])
                    check_int(tmp3[1], tmp3[0])
                    check_if_zero(tmp3[1], tmp3[0])
                    GF[tmp[1]] = int(self.args[1][2] / GF[tmp3[1]])
                else:
                    sys.exit(53)
            else:
                if self.args[1][1] == 'int' and self.args[2][1] == 'int':
                    check_int(self.args[1][2])
                    check_int(self.args[2][2])
                    check_if_zero(self.args[2][2])
                    GF[tmp[1]] = int(self.args[1][2] / self.args[2][2])
                else:
                    sys.exit(53)
        

class LT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('check_type(' + tmp2[0] + '[tmp2[1]], ' + tmp3[0] +'[tmp3[1]])')
                exec('check_nil(' + tmp2[0] + '[tmp2[1]])')
                exec('check_nil(' + tmp3[0] + '[tmp3[1]])')
                exec('if ' +tmp2[0] + '[tmp2[1]] < ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                exec('check_type(' + tmp2[0] + '[tmp2[1]], self.args[2][2])')
                exec('check_nil(' + tmp2[0] + '[tmp2[1]])')
                check_nil(self.args[2][2])
                exec('if ' +tmp2[0] + '[tmp2[1]] < self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('check_type(self.args[1][2], ' + tmp3[0] +'[tmp3[1]])')
                check_nil(self.args[1][2])
                exec('check_nil(' + tmp3[0] + '[tmp3[1]])')
                exec('if self.args[1][2] < ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                check_type(self.args[1][2], self.args[2][2])
                check_nil(self.args[1][2])
                check_nil(self.args[2][2])
                exec('if self.args[1][2] < self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
                
            

class GT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('check_type(' + tmp2[0] + '[tmp2[1]], ' + tmp3[0] +'[tmp3[1]])')
                exec('check_nil(' + tmp2[0] + '[tmp2[1]])')
                exec('check_nil(' + tmp3[0] + '[tmp3[1]])')
                exec('if ' +tmp2[0] + '[tmp2[1]] > ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                exec('check_type(' + tmp2[0] + '[tmp2[1]], self.args[2][2])')
                exec('check_nil(' + tmp2[0] + '[tmp2[1]])')
                check_nil(self.args[2][2])
                exec('if ' +tmp2[0] + '[tmp2[1]] > self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('check_type(self.args[1][2], ' + tmp3[0] +'[tmp3[1]])')
                check_nil(self.args[1][2])
                exec('check_nil(' + tmp3[0] + '[tmp3[1]])')
                exec('if self.args[1][2] > ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                check_type(self.args[1][2], self.args[2][2])
                check_nil(self.args[1][2])
                check_nil(self.args[2][2])
                exec('if self.args[1][2] > self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')


class EQ:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('if ' + tmp2[0] + '[tmp2[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and ' + tmp3[0] +'[tmp3[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(' + tmp2[0] + '[tmp2[1]], ' + tmp3[0] +'[tmp3[1]])')
                exec('if ' + tmp2[0] + '[tmp2[1]] == ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                exec('if ' + tmp2[0] + '[tmp2[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and self.args[2][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(' + tmp2[0] + '[tmp2[1]], self.args[2][2])')
                exec('if ' +tmp2[0] + '[tmp2[1]] == self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('if self.args[1][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and ' + tmp3[0] +'[tmp3[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(self.args[1][2], ' + tmp3[0] +'[tmp3[1]])')
                exec('if self.args[1][2] == ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                if self.args[1][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and self.args[2][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil":
                    check_type(self.args[1][2], self.args[2][2])
                exec('if self.args[1][2] == self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        

class AND:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('check_boolean(' + tmp2[0] + '[tmp2[1]])')
                exec('check_boolean(' + tmp3[0] + '[tmp3[1]])')
                exec('if ' +tmp2[0] + '[tmp2[1]] and ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                exec('check_boolean(' + tmp2[0] + '[tmp2[1]])')
                check_boolean(self.args[2][2])
                exec('if ' +tmp2[0] + '[tmp2[1]] and self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_boolean(self.args[1][2])
                exec('check_boolean(' + tmp3[0] + '[tmp3[1]])')
                exec('if self.args[1][2] and ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                check_boolean(self.args[1][2])
                check_boolean(self.args[2][2])
                exec('if self.args[1][2] and self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')

class OR:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('check_boolean(' + tmp2[0] + '[tmp2[1]])')
                exec('check_boolean(' + tmp3[0] + '[tmp3[1]])')
                exec('if ' +tmp2[0] + '[tmp2[1]] or ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                exec('check_boolean(' + tmp2[0] + '[tmp2[1]])')
                check_boolean(self.args[2][2])
                exec('if ' +tmp2[0] + '[tmp2[1]] or self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_boolean(self.args[1][2])
                exec('check_boolean(' + tmp3[0] + '[tmp3[1]])')
                exec('if self.args[1][2] or ' + tmp3[0] + '[tmp3[1]]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
            else:
                check_boolean(self.args[1][2])
                check_boolean(self.args[2][2])
                exec('if self.args[1][2] or self.args[2][2]:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')

class STRI2INT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_str(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(tmp3[1], tmp3[0])
                exec('tmpstr = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpint = ' + tmp3[0] + '[tmp3[1]]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = ord(tmpstr[tmpint])')
            else:
                check_int(self.args[2][2])
                exec('tmpstr = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpint = self.args[2][2]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = ord(tmpstr[tmpint])')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_str(self.args[1][2])
                check_int(tmp3[1], tmp3[0])
                exec('tmpstr = self.args[1][2]')
                exec('tmpint = ' + tmp3[0] + '[tmp3[1]]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = ord(tmpstr[tmpint])')
            else:
                check_str(self.args[1][2])
                check_int(self.args[2][2])
                exec('tmpstr = self.args[1][2]')
                exec('tmpint = self.args[2][2]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = ord(tmpstr[tmpint])')

class CONCAT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_str(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_str(tmp3[1], tmp3[0])
                exec('tmpstr1 = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpstr2 = ' + tmp3[0] + '[tmp3[1]]')
                exec(tmp[0] + '[tmp[1]] = tmpstr1 + tmpstr2')
            else:
                check_str(self.args[2][2])
                exec('tmpstr1 = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpstr2 = self.args[2][2]')
                exec(tmp[0] + '[tmp[1]] = tmpstr1 + tmpstr2')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_str(self.args[1][2])
                check_str(tmp3[1], tmp3[0])
                exec('tmpstr1 = self.args[1][2]')
                exec('tmpstr2 = ' + tmp3[0] + '[tmp3[1]]')
                exec(tmp[0] + '[tmp[1]] = tmpstr1 + tmpstr2')
            else:
                check_str(self.args[1][2])
                check_str(self.args[2][2])
                exec('tmpstr1 = self.args[1][2]')
                exec('tmpstr2 = self.args[2][2]')
                exec(tmp[0] + '[tmp[1]] = tmpstr1 + tmpstr2')

class GETCHAR:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_str(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(tmp3[1], tmp3[0])
                exec('tmpstr = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpint = ' + tmp3[0] + '[tmp3[1]]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = tmpstr[tmpint]')
            else:
                check_int(self.args[2][2])
                exec('tmpstr = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpint = self.args[2][2]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = tmpstr[tmpint]')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_str(self.args[1][2])
                check_int(tmp3[1], tmp3[0])
                exec('tmpstr = self.args[1][2]')
                exec('tmpint = ' + tmp3[0] + '[tmp3[1]]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = tmpstr[tmpint]')
            else:
                check_str(self.args[1][2])
                check_int(self.args[2][2])
                exec('tmpstr = self.args[1][2]')
                exec('tmpint = self.args[2][2]')
                exec('if tmpint < 0 or tmpint >= len(tmpstr):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec(tmp[0] + '[tmp[1]] = tmpstr[tmpint]')

class SETCHAR:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        check_str(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_int(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_str(tmp3[1], tmp3[0])
                char_isEmpty(tmp3[1], tmp3[0])
                exec('tmpint = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpstr = ' + tmp3[0] + '[tmp3[1]]')
                exec('str = list(' + tmp[0] + '[tmp[1]])')
                exec('if tmpint < 0 or tmpint >= len(str):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec('if tmpstr:\n\tstr[tmpint] = tmpstr[0]\nelse:\n\tstr[tmpint] = ""')
                exec(tmp[0] + '[tmp[1]] = \"\".join(str)')
            else:
                check_str(self.args[2][2])
                char_isEmpty(self.args[2][2])
                exec('tmpint = ' + tmp2[0] + '[tmp2[1]]')
                exec('tmpstr = self.args[2][2]')
                exec('str = list(' + tmp[0] + '[tmp[1]])')
                exec('if tmpint < 0 or tmpint >= len(str):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec('if tmpstr:\n\tstr[tmpint] = tmpstr[0]\nelse:\n\tstr[tmpint] = ""')
                exec(tmp[0] + '[tmp[1]] = \"\".join(str)')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                check_int(self.args[1][2])
                check_str(tmp3[1], tmp3[0])
                char_isEmpty(tmp3[1], tmp3[0])
                exec('tmpint = self.args[1][2]')
                exec('tmpstr = ' + tmp3[0] + '[tmp3[1]]')
                exec('str = list(' + tmp[0] + '[tmp[1]])')
                exec('if tmpint < 0 or tmpint >= len(str):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec('if tmpstr:\n\tstr[tmpint] = tmpstr[0]\nelse:\n\tstr[tmpint] = ""')
                exec(tmp[0] + '[tmp[1]] = \"\".join(str)')
            else:
                check_int(self.args[1][2])
                check_str(self.args[2][2])
                char_isEmpty(self.args[2][2])
                exec('tmpint = self.args[1][2]')
                exec('tmpstr = self.args[2][2]')
                exec('str = list(' + tmp[0] + '[tmp[1]])')
                exec('if tmpint < 0 or tmpint >= len(str):\n\tprint(\'out of bound\')\n\tsys.exit(58)')
                exec('if tmpstr:\n\tstr[tmpint] = tmpstr[0]\nelse:\n\tstr[tmpint] = ""')
                exec(tmp[0] + '[tmp[1]] = \"\".join(str)')


class INT2CHAR:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_int(tmp2[1],tmp2[0])
            exec('tmpint = ' + tmp2[0] + '[tmp2[1]]')
            exec('if tmpint < 0 or tmpint > 255:\n\tprint(\'out of bound\')\n\tsys.exit(58)')
            exec(tmp[0] + '[tmp[1]] = chr(tmpint)')
        else:
            check_int(self.args[1][2])
            exec('tmpint = self.args[1][2]')
            exec('if tmpint < 0 or tmpint > 255:\n\tprint(\'out of bound\')\n\tsys.exit(58)')
            exec(tmp[0] + '[tmp[1]] = chr(tmpint)')
            

class MOVE:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            isEmpty(tmp2[1], tmp2[0])
            exec(tmp[0] + '[tmp[1]] = '+ tmp2[0] + '[tmp2[1]]')
        else:
            isEmpty(self.args[1][2])
            exec(tmp[0] + '[tmp[1]] = self.args[1][2]')

class STRLEN:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_str(tmp2[1], tmp2[0])
            exec(tmp[0] + '[tmp[1]] = len(change_before_write('+ tmp2[0] + '[tmp2[1]]))')
        else:
            check_str(self.args[1][2])
            exec(tmp[0] + '[tmp[1]] = len(change_before_write(self.args[1][2]))')

class NOT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_boolean(tmp2[1], tmp2[0])
            exec('if ' +tmp2[0] + '[tmp2[1]] == False:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')
        else:
            check_boolean(self.args[1][2])
            exec('if self.args[1][2] == False:\n\t' + tmp[0] + '[tmp[1]] = True\nelse:\n\t' + tmp[0] + '[tmp[1]] = False')

class TYPE:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_SYMB(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            exec('tmptype = type(' + tmp2[0] + '[tmp2[1]])\nif tmptype == int:\n\t' + tmp[0] + '[tmp[1]] = \"int\"\nelif tmptype == bool:\n\t' + tmp[0] + '[tmp[1]] = \"bool\"\nelif not '+tmp2[0]+'[tmp2[1]]:\n\t' + tmp[0] + '[tmp[1]] = \"#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪\"\nelif ' + tmp2[0] + '[tmp2[1]] == \"#¶!©y←5§iðo<ì♪!©y←5§inil\":\n\t' + tmp[0] + '[tmp[1]] = \"nil\"\nelse:\n\t' + tmp[0] + '[tmp[1]] = \"string\"')
        else:
            exec('tmptype = type(self.args[1][2])\nif tmptype == int:\n\t' + tmp[0] + '[tmp[1]] = \"int\"\nelif tmptype == bool:\n\t' + tmp[0] + '[tmp[1]] = \"bool\"\nelif not self.args[1][2]:\n\t' + tmp[0] + '[tmp[1]] = \"#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪\"\nelif self.args[1][2] == \"#¶!©y←5§iðo<ì♪!©y←5§inil\":\n\t' + tmp[0] + '[tmp[1]] = \"nil\"\nelse:\n\t' + tmp[0] + '[tmp[1]] = \"string\"')
            

class LABEL:
    def __init__(self, args):
        self.args = args
        self.toInstruct()
    def toInstruct(self):
        CHECK_LABEL(self.args.args)
        if self.args.args[0][2] not in label_dict:
            label_dict[self.args.args[0][2]] = self.args.order
        else:
            print('redefinition of label')
            sys.exit(52)

class JUMP:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_LABEL(self.args)
        global inst
        inst = jump_fnc(self.args[0][2])

class CALL:
    def __init__(self, args):
        self.args = args
        self.toInstruct()
    def toInstruct(self):
        CHECK_LABEL(self.args.args)
        global inst
        call_stack.append(self.args.order)
        inst = jump_fnc(self.args.args[0][2])

class JUMPIFEQ:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_LABEL_SYMB_SYMB(self.args)
        jump_fnc(self.args[0][2])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('if ' + tmp2[0] + '[tmp2[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and ' + tmp3[0] +'[tmp3[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(' + tmp2[0] + '[tmp2[1]], ' + tmp3[0] +'[tmp3[1]])')
                exec('global inst\nif ' +tmp2[0] + '[tmp2[1]] == ' + tmp3[0] + '[tmp3[1]]:\n\tinst = jump_fnc(self.args[0][2])')
            else:
                exec('if ' + tmp2[0] + '[tmp2[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and self.args[2][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(' + tmp2[0] + '[tmp2[1]], self.args[2][2])')
                exec('global inst\nif ' +tmp2[0] + '[tmp2[1]] == self.args[2][2]:\n\tinst = jump_fnc(self.args[0][2])')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('if self.args[1][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and ' + tmp3[0] +'[tmp3[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(self.args[1][2], ' + tmp3[0] +'[tmp3[1]])')
                exec('global inst\nif self.args[1][2] == ' + tmp3[0] + '[tmp3[1]]:\n\tinst = jump_fnc(self.args[0][2])')
            else:
                if self.args[1][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and self.args[2][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil":
                    check_type(self.args[1][2], self.args[2][2])
                exec('global inst\nif self.args[1][2] == self.args[2][2]:\n\tinst = jump_fnc(self.args[0][2])')

class JUMPIFNEQ:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_LABEL_SYMB_SYMB(self.args)
        jump_fnc(self.args[0][2])
        if self.args[1][1] == 'var':
            tmp2 = split_if_at(self.args[1][2])
            check_in_frame(tmp2[1], tmp2[0])
            check_in_frame(tmp2[1], tmp2[0])
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('if ' + tmp2[0] + '[tmp2[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and ' + tmp3[0] +'[tmp3[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(' + tmp2[0] + '[tmp2[1]], ' + tmp3[0] +'[tmp3[1]])')
                exec('global inst\nif ' +tmp2[0] + '[tmp2[1]] != ' + tmp3[0] + '[tmp3[1]]:\n\tinst = jump_fnc(self.args[0][2])')
            else:
                exec('if ' + tmp2[0] + '[tmp2[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and self.args[2][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(' + tmp2[0] + '[tmp2[1]], self.args[2][2])')
                exec('global inst\nif ' +tmp2[0] + '[tmp2[1]] != self.args[2][2]:\n\tinst = jump_fnc(self.args[0][2])')
        else:
            if self.args[2][1] == 'var':
                tmp3 = split_if_at(self.args[2][2])
                check_in_frame(tmp3[1], tmp3[0])
                exec('if self.args[1][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and ' + tmp3[0] +'[tmp3[1]] != "#¶!©y←5§iðo<ì♪!©y←5§inil":\n\tcheck_type(self.args[1][2], ' + tmp3[0] +'[tmp3[1]])')
                exec('global inst\nif self.args[1][2] != ' + tmp3[0] + '[tmp3[1]]:\n\tinst = jump_fnc(self.args[0][2])')
            else:
                if self.args[1][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil" and self.args[2][2] != "#¶!©y←5§iðo<ì♪!©y←5§inil":
                    check_type(self.args[1][2], self.args[2][2])
                exec('global inst\nif self.args[1][2] != self.args[2][2]:\n\tinst = jump_fnc(self.args[0][2])')

class PUSHS:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_SYMB(self.args)
        if self.args[0][1] == 'var':
            tmp = split_if_at(self.args[0][2])
            check_in_frame(tmp[1], tmp[0])
            stack_isEpmty(tmp[1], tmp[0])
            stack.append(tmp[1])
        else:
            stack_isEpmty(self.args[0][2])
            stack.append(self.args[0][2])

class WRITE:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_SYMB(self.args)
        if self.args[0][1] == 'var':
            tmp = split_if_at(self.args[0][2])
            check_in_frame(tmp[1], tmp[0])
            isEmpty(tmp[1], tmp[0])
            exec('toWrite = change_before_write('+ tmp[0] + '[tmp[1]])\nprint(toWrite, end=\'\')')
        elif self.args[0][1] == 'nil':
            if self.args[0][2] == '#¶!©y←5§iðo<ì♪!©y←5§inil':
                print("", end='')
            else:
                print('nil is not nil')
                sys.exit(53)
        else:
            isEmpty(self.args[0][2])
            toWrite = change_before_write(self.args[0][2])
            print(toWrite, end='')

class EXIT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_SYMB(self.args)
        if self.args[0][1] == 'var':
            tmp = split_if_at(self.args[0][2])
            check_in_frame(tmp[1], tmp[0])
            exec('check_int('+tmp[0]+'[tmp[1]])')
            exec('if '+tmp[0]+'[tmp[1]] < 0 or '+tmp[0]+'[tmp[1]] > 49:\n\tprint("exit value out of range")\n\tsys.exit(57)')
            exec('sys.exit('+tmp[0]+'[tmp[1]])')
        else:
            check_int(self.args[0][2])
            if self.args[0][2] < 0 or self.args[0][2] > 49:
                sys.exit(57)
            sys.exit(self.args[0][2])

class DPRINT:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_SYMB(self.args)
        if self.args[0][1] == 'var':
            tmp = split_if_at(self.args[0][2])
            check_in_frame(tmp[1], tmp[0])
            isEmpty(tmp[1], tmp[0])
            exec('toWrite = change_before_write('+ tmp[0] + '[tmp[1]])\neprint(toWrite, end=\'\')')
        elif self.args[0][1] == 'nil':
            if self.args[0][2] == '#¶!©y←5§iðo<ì♪!©y←5§inil':
                eprint([], end='')
            else:
                print('nil is not nil')
                sys.exit(53)
        else:
            isEmpty(self.args[0][2])
            toWrite = change_before_write(self.args[0][2])
            eprint(toWrite, end='')

class READ:
    def __init__(self, args):
        self.args = args.args
        self.toInstruct()
    def toInstruct(self):
        CHECK_VAR_TYPE(self.args)
        tmp = split_if_at(self.args[0][2])
        check_in_frame(tmp[1], tmp[0])
        global toRead
        global linecount
        read = ""
        if not toRead:
            read = input()
        else:
            if linecount < len(toRead):
                read = toRead[linecount]
            else:
                read = '#¶!©y←5§iðo<ì♪!©y←5§inil'
        if self.args[1][2] == 'string':
            if not read:
                read = "#¶!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪!©Y←5§IÐO<Ì♪"
            exec(tmp[0] + '[tmp[1]] = str(read)')
        elif self.args[1][2] == 'int':
            try:
                exec(tmp[0] + '[tmp[1]] = int(read)')
            except:
                read = "#¶!©y←5§iðo<ì♪!©y←5§inil"
                exec(tmp[0] + '[tmp[1]] = str(read)')
        elif self.args[1][2] == 'bool':
            try:
                if not str(read):
                    read = "#¶!©y←5§iðo<ì♪!©y←5§inil"
            except:
                pass
            if read != '#¶!©y←5§iðo<ì♪!©y←5§inil':
                if read.lower() != 'true':
                    exec(tmp[0] + '[tmp[1]] = False')
                else:
                    exec(tmp[0] + '[tmp[1]] = True')
            else:
                read = '#¶!©y←5§iðo<ì♪!©y←5§inil'
                exec(tmp[0] + '[tmp[1]] = str(read)')
        linecount +=1



class Interpret:
    def __init__(self, instruction):
        self.inst = instruction
    def interpret(self):
        self.inst_dict = {
            "CREATEFRAME": CREATEFRAME,
            "PUSHFRAME": PUSHFRAME,
            "POPFRAME": POPFRAME,
            "RETURN": RETURN,
            "BREAK": BREAK,
            "DEFVAR": DEFVAR,
            "POPS": POPS,
            "ADD": ADD,
            "SUB": SUB,
            "MUL": MUL,
            "IDIV": IDIV,
            "LT": LT,
            "GT": GT,
            "EQ": EQ,
            "AND": AND,
            "OR": OR,
            "STRI2INT": STRI2INT,
            "CONCAT": CONCAT,
            "GETCHAR": GETCHAR,
            "SETCHAR": SETCHAR,
            "INT2CHAR": INT2CHAR, 
            "MOVE": MOVE,
            "STRLEN": STRLEN,
            "NOT": NOT,
            "TYPE": TYPE,
            "READ": READ,
            "LABEL": LABEL,
            "JUMP": JUMP,
            "CALL": CALL,
            "JUMPIFEQ": JUMPIFEQ,
            "JUMPIFNEQ": JUMPIFNEQ,
            "PUSHS": PUSHS,
            "WRITE": WRITE,
            "EXIT": EXIT,
            "DPRINT": DPRINT,          
        }
        if self.inst.name in self.inst_dict:
            self.inst_dict[self.inst.name](self.inst)        
        else:
            exit(32)

class Instruction:
    def __init__(self, XMLinst):
        self.name = XMLinst.attrib['opcode'].upper()
        try:
            self.actual_order = int(XMLinst.attrib['order'])
        except:
            sys.exit(32)
        self.args = []
        self.arg = []
        if self.actual_order < 1:
            sys.exit(32)
        global instructions
        for i in instructions:
            if self.actual_order == i.actual_order:
                sys.exit(32)
    def inst_args_add(self, XMLarg):
        self.arg.append(XMLarg.tag)
        self.arg.append(XMLarg.attrib['type'])
        self.arg.append(XMLarg.text)
        self.args.append(self.arg)
        self.arg = []
    def inst_args_sort(self):
        self.args.sort(key=lambda x:x[0])
    def return_order(self):
        return self.actual_order
    def set_order(self):
        global global_order
        global_order += 1
        self.order = global_order
    def arg_check(self):
        global argcounter
        for j in self.args:
            argcheck = "arg" + str(argcounter)
            if j[0] != argcheck:
                print('argument parse error')
                sys.exit(32)
            argcounter += 1
        

# argpare
parser = argparse.ArgumentParser(description='Parse arguments')
parser.add_argument('--source', required= False, help='source XML file')
parser.add_argument('--input', required= False, help='input file')

args = parser.parse_args()


if args.source == None and args.input == None:
    print('bad arguments')
    sys.exit(10)
# xml load
try:
    if(args.source) != None:
        tree = ET.parse(args.source)
    else:
        tree = ET.parse(sys.stdin)
    root = tree.getroot()
except:
    exit(31)

try:
    if args.input != None:
        openfile = open(args.input, 'r')
        for line in openfile:
            toRead.append(line.strip())
        openfile.close()
except:
    exit(31)

# xml check
if(root.tag != 'program' or len(root.attrib) > 3 or root.attrib.get('language') != 'IPPcode21'):
    print('Root error')
    sys.exit(32)
for child in root:
    if child.tag != 'instruction':
        print('Error: child is not instruction')
        sys.exit(32)
    childlist = list(child.attrib.keys())
    if not('order' in childlist) or not ('opcode' in childlist):
        sys.exit(32)
    for subelem in child:
        if not(re.match(r"^arg(1|2|3)$", subelem.tag)):
            print("Error: wrong number of argumetns")
            sys.exit(32)

# xml2inst
for instruction in root:
    inst = Instruction(instruction)
    if instruction.tag == 'instruction':
        for sub in instruction:
            inst.inst_args_add(sub)
        inst.inst_args_sort()
    instructions.append(inst)
    instructions.sort(key=Instruction.return_order)
    if inst.actual_order in instructions:
        sys.exit(32)

for i in range (len (instructions)):
        instructions[i].set_order()
        instructions[i].arg_check()
        argcounter = 1


# interpet
inst = 0
while inst < len(instructions):
    interpret = Interpret(instructions[inst])
    interpret.interpret()
    inst += 1