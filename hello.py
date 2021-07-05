# Generated by Haxe 4.1.1
# coding: utf-8
import sys

import math as python_lib_Math
import math as Math
import builtins as python_lib_Builtins
import random as python_lib_Random


class _hx_AnonObject:
    _hx_disable_getattr = False
    def __init__(self, fields):
        self.__dict__ = fields
    def __repr__(self):
        return repr(self.__dict__)
    def __contains__(self, item):
        return item in self.__dict__
    def __getitem__(self, item):
        return self.__dict__[item]
    def __getattr__(self, name):
        if (self._hx_disable_getattr):
            raise AttributeError('field does not exist')
        else:
            return None
    def _hx_hasattr(self,field):
        self._hx_disable_getattr = True
        try:
            getattr(self, field)
            self._hx_disable_getattr = False
            return True
        except AttributeError:
            self._hx_disable_getattr = False
            return False



class Enum:
    _hx_class_name = "Enum"
    __slots__ = ("tag", "index", "params")
    _hx_fields = ["tag", "index", "params"]
    _hx_methods = ["__str__"]

    def __init__(self,tag,index,params):
        self.tag = tag
        self.index = index
        self.params = params

    def __str__(self):
        if (self.params is None):
            return self.tag
        else:
            return self.tag + '(' + (', '.join(str(v) for v in self.params)) + ')'


class RunState(Enum):
    __slots__ = ()
    _hx_class_name = "RunState"
RunState.Running = RunState("Running", 0, ())
RunState.Paused = RunState("Paused", 1, ())
RunState.Stopped = RunState("Stopped", 2, ())


class Interpreter:
    _hx_class_name = "Interpreter"
    __slots__ = ("state", "pastStates", "program", "runState", "cycleMod", "langDef", "ip")
    _hx_fields = ["state", "pastStates", "program", "runState", "cycleMod", "langDef", "ip"]
    _hx_methods = ["error", "reset", "flash", "run", "stop", "prevState", "bin", "clamp", "cycle", "inb", "out", "dupe", "swp", "del", "zero", "rand", "inc", "dec", "add", "sub", "mul", "div", "mod", "jmp", "jez", "jlz", "jgz", "jnz", "srt", "ret", "load", "save", "brk", "lit", "out_all", "print", "dump"]

    def __init__(self,program,langDef):
        self.langDef = None
        self.runState = None
        self.ip = 0
        self.cycleMod = 10
        self.program = program
        self.pastStates = list()
        tmp = list()
        tmp1 = list()
        tmp2 = list()
        tmp3 = list()
        _g = []
        _g.append(0)
        _g.append(0)
        _g.append(0)
        _g.append(0)
        _g.append(0)
        _g.append(0)
        _g.append(0)
        _g.append(0)
        self.state = _hx_AnonObject({'stack': tmp, 'inbox': tmp1, 'outbox': tmp2, 'callStack': tmp3, 'registers': _g, 'cycle': 0, 'registerUse': 0, 'maxStackSize': 0})
        _this = self.pastStates
        x = self.state
        _this.append(x)
        self.langDef = langDef

    def error(self,msg):
        op = python_internal_ArrayImpl._get(self.program, python_internal_ArrayImpl._get(self.state.registers, 7))
        self.runState = RunState.Stopped
        print(str(((("null" if msg is None else msg) + " on line ") + str(((op.ln + 1))))))

    def reset(self,inbox = None):
        self.flash((self.pastStates[0] if 0 < len(self.pastStates) else None))
        if (inbox is not None):
            self.state.inbox = inbox

    def flash(self,state):
        self.state = state
        _this = self.pastStates
        l = len(_this)
        if (l < 1):
            idx = 0
            v = None
            l1 = len(_this)
            while (l1 < idx):
                _this.append(None)
                l1 = (l1 + 1)
            if (l1 == idx):
                _this.append(v)
            else:
                _this[idx] = v
        elif (l > 1):
            pos = 1
            _hx_len = (l - 1)
            if (pos < 0):
                pos = (len(_this) + pos)
            if (pos < 0):
                pos = 0
            res = _this[pos:(pos + _hx_len)]
            del _this[pos:(pos + _hx_len)]
        self.runState = RunState.Paused

    def run(self):
        self.runState = RunState.Running
        while (self.runState == RunState.Running):
            self.cycle()
        return self.state.outbox

    def stop(self):
        self.runState = RunState.Stopped

    def prevState(self):
        pass

    def bin(self,f):
        _this = self.state.stack
        b = (None if ((len(_this) == 0)) else _this.pop())
        _this = self.state.stack
        a = (None if ((len(_this) == 0)) else _this.pop())
        _this = self.state.stack
        x = f(a,b)
        _this.append(x)
        self.clamp()

    def clamp(self):
        val = python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1))
        if (val > 9999):
            val = 9999
        if (val < -9999):
            val = -9999
        python_internal_ArrayImpl._set(self.state.stack, (len(self.state.stack) - 1), val)

    def cycle(self):
        self.ip = python_internal_ArrayImpl._get(self.state.registers, 7)
        if (self.ip >= len(self.program)):
            self.stop()
        if (self.runState == RunState.Stopped):
            return
        inst = python_internal_ArrayImpl._get(self.program, self.ip)
        op = inst.opcode
        val = inst.val
        if (self.langDef.h.get(op,None).pops > len(self.state.stack)):
            self.error(((((("Cannot execute instruction '" + ("null" if op is None else op)) + "': Stack must have ") + str(self.langDef.h.get(op,None).pops)) + " values, it has ") + str(len(self.state.stack))))
            return
        op1 = op
        _hx_local_0 = len(op1)
        if (_hx_local_0 == 4):
            if (op1 == "dump"):
                self.dump()
            elif (op1 == "dupe"):
                self.dupe()
            elif (op1 == "load"):
                self.load(val)
            elif (op1 == "rand"):
                self.rand()
            elif (op1 == "save"):
                self.save(val)
            elif (op1 == "zero"):
                self.zero()
            else:
                print(str((("Opcode '" + ("null" if op is None else op)) + "' not implimented")))
        elif (_hx_local_0 == 5):
            if (op1 == "print"):
                self.print()
            else:
                print(str((("Opcode '" + ("null" if op is None else op)) + "' not implimented")))
        elif (_hx_local_0 == 3):
            if (op1 == "add"):
                self.add()
            elif (op1 == "brk"):
                self.brk()
            elif (op1 == "dec"):
                self.dec()
            elif (op1 == "del"):
                self._hx_del()
            elif (op1 == "div"):
                self.div()
            elif (op1 == "inc"):
                self.inc()
            elif (op1 == "jez"):
                self.jez(val)
            elif (op1 == "jgz"):
                self.jgz(val)
            elif (op1 == "jlz"):
                self.jlz(val)
            elif (op1 == "jmp"):
                self.jmp(val)
            elif (op1 == "jnz"):
                self.jnz(val)
            elif (op1 == "lit"):
                self.lit(val)
            elif (op1 == "mod"):
                self.mod()
            elif (op1 == "mul"):
                self.mul()
            elif (op1 == "out"):
                self.out()
            elif (op1 == "ret"):
                if (len(self.state.callStack) == 0):
                    self.error("Tried to return from a subroutine but callstack empty")
                else:
                    self.ret()
            elif (op1 == "srt"):
                self.srt(val)
            elif (op1 == "sub"):
                self.sub()
            elif (op1 == "swp"):
                self.swp()
            else:
                print(str((("Opcode '" + ("null" if op is None else op)) + "' not implimented")))
        elif (_hx_local_0 == 7):
            if (op1 == "out_all"):
                self.out_all()
            else:
                print(str((("Opcode '" + ("null" if op is None else op)) + "' not implimented")))
        elif (_hx_local_0 == 2):
            if (op1 == "in"):
                self.inb()
            else:
                print(str((("Opcode '" + ("null" if op is None else op)) + "' not implimented")))
        else:
            print(str((("Opcode '" + ("null" if op is None else op)) + "' not implimented")))
        if (self.ip == python_internal_ArrayImpl._get(self.state.registers, 7)):
            _hx_local_1 = self.state.registers
            _hx_local_2 = 7
            _hx_local_3 = (_hx_local_1[_hx_local_2] if _hx_local_2 >= 0 and _hx_local_2 < len(_hx_local_1) else None)
            python_internal_ArrayImpl._set(_hx_local_1, _hx_local_2, (_hx_local_3 + 1))
            _hx_local_3
        else:
            python_internal_ArrayImpl._set(self.state.registers, 7, self.ip)

    def inb(self):
        if (len(self.state.inbox) == 0):
            self.runState = RunState.Stopped
        else:
            _this = self.state.stack
            _this1 = self.state.inbox
            x = (None if ((len(_this1) == 0)) else _this1.pop())
            _this.append(x)

    def out(self):
        _this = self.state.outbox
        _this1 = self.state.stack
        x = (None if ((len(_this1) == 0)) else _this1.pop())
        _this.append(x)

    def dupe(self):
        _this = self.state.stack
        x = python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1))
        _this.append(x)

    def swp(self):
        _this = self.state.stack
        a = (None if ((len(_this) == 0)) else _this.pop())
        _this = self.state.stack
        b = (None if ((len(_this) == 0)) else _this.pop())
        _this = self.state.stack
        _this.append(a)
        _this = self.state.stack
        _this.append(b)

    def _hx_del(self):
        _this = self.state.stack
        if (len(_this) != 0):
            _this.pop()

    def zero(self):
        _this = self.state.stack
        _this.append(0)

    def rand(self):
        val = ((python_lib_Random.random() * 2) - 1)
        val = (val * 10000)
        _this = self.state.stack
        _this.append(0)

    def inc(self):
        _hx_local_0 = self.state.stack
        _hx_local_1 = (len(self.state.stack) - 1)
        _hx_local_2 = (_hx_local_0[_hx_local_1] if _hx_local_1 >= 0 and _hx_local_1 < len(_hx_local_0) else None)
        python_internal_ArrayImpl._set(_hx_local_0, _hx_local_1, (_hx_local_2 + 1))
        _hx_local_2
        self.clamp()

    def dec(self):
        _hx_local_0 = self.state.stack
        _hx_local_1 = (len(self.state.stack) - 1)
        _hx_local_2 = (_hx_local_0[_hx_local_1] if _hx_local_1 >= 0 and _hx_local_1 < len(_hx_local_0) else None)
        python_internal_ArrayImpl._set(_hx_local_0, _hx_local_1, (_hx_local_2 - 1))
        _hx_local_2
        self.clamp()

    def add(self):
        def _hx_local_0(a,b):
            return (a + b)
        self.bin(_hx_local_0)

    def sub(self):
        def _hx_local_0(a,b):
            return (a - b)
        self.bin(_hx_local_0)

    def mul(self):
        def _hx_local_0(a,b):
            return (a * b)
        self.bin(_hx_local_0)

    def div(self):
        def _hx_local_0(a,b):
            return Math.floor((a / b))
        self.bin(_hx_local_0)

    def mod(self):
        def _hx_local_0(a,b):
            aneg = (a < 0)
            bneg = (b < 0)
            if aneg:
                a = -a
            if bneg:
                b = -b
            val = HxOverrides.mod(a, b)
            if aneg:
                val = (b - val)
            if bneg:
                val = -val
            return val
        self.bin(_hx_local_0)

    def jmp(self,val):
        self.ip = val

    def jez(self,val):
        if (python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1)) == 0):
            self.ip = val

    def jlz(self,val):
        if (python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1)) < 0):
            self.ip = val

    def jgz(self,val):
        if (python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1)) > 0):
            self.ip = val

    def jnz(self,val):
        if (python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1)) != 0):
            self.ip = val

    def srt(self,val):
        _this = self.state.callStack
        x = self.ip
        _this.append(x)
        self.ip = val

    def ret(self):
        _this = self.state.callStack
        self.ip = (None if ((len(_this) == 0)) else _this.pop())

    def load(self,val):
        _this = self.state.stack
        x = python_internal_ArrayImpl._get(self.state.registers, val)
        _this.append(x)
        _hx_local_0 = self.state
        _hx_local_1 = _hx_local_0.registerUse
        _hx_local_0.registerUse = (_hx_local_1 + 1)
        _hx_local_1

    def save(self,val):
        _this = self.state.stack
        python_internal_ArrayImpl._set(self.state.registers, val, (None if ((len(_this) == 0)) else _this.pop()))
        _hx_local_0 = self.state
        _hx_local_1 = _hx_local_0.registerUse
        _hx_local_0.registerUse = (_hx_local_1 + 1)
        _hx_local_1

    def brk(self):
        self.runState = RunState.Paused

    def lit(self,val):
        _this = self.state.stack
        _this.append(val)

    def out_all(self):
        while (len(self.state.stack) > 0):
            self.out()

    def print(self):
        print(str(python_internal_ArrayImpl._get(self.state.stack, (len(self.state.stack) - 1))))

    def dump(self):
        _this = self.state.inbox
        print(str(("Inbox:     " + HxOverrides.stringOrNull(((("[" + HxOverrides.stringOrNull(",".join([python_Boot.toString1(x1,'') for x1 in _this]))) + "]"))))))
        _this = self.state.stack
        print(str(("Stack:     " + HxOverrides.stringOrNull(((("[" + HxOverrides.stringOrNull(",".join([python_Boot.toString1(x1,'') for x1 in _this]))) + "]"))))))
        _this = self.state.outbox
        print(str(("Outbox:    " + HxOverrides.stringOrNull(((("[" + HxOverrides.stringOrNull(",".join([python_Boot.toString1(x1,'') for x1 in _this]))) + "]"))))))
        _this = self.state.registers
        print(str(("Registers: " + HxOverrides.stringOrNull(((("[" + HxOverrides.stringOrNull(",".join([python_Boot.toString1(x1,'') for x1 in _this]))) + "]"))))))



class LanguageDef:
    _hx_class_name = "LanguageDef"
    __slots__ = ()
    _hx_statics = ["getDef"]

    @staticmethod
    def getDef(content):
        insts = haxe_ds_StringMap()
        lines = content.split("\n")
        _g = 0
        while (_g < len(lines)):
            line = (lines[_g] if _g >= 0 and _g < len(lines) else None)
            _g = (_g + 1)
            lin = line.split("|")
            if (len(lin) < 3):
                continue
            inst = _hx_AnonObject({'arg': (lin[2] if 2 < len(lin) else None), 'pops': Std.parseInt((lin[3] if 3 < len(lin) else None))})
            key = StringTools.replace((lin[1] if 1 < len(lin) else None),"*","")
            insts.h[key] = inst
        return insts


class Main:
    _hx_class_name = "Main"
    __slots__ = ()
    _hx_statics = ["main"]

    @staticmethod
    def main():
        langDefStr = sys_io_File.getContent("res/langdef.txt")
        langDef = LanguageDef.getDef(langDefStr)
        src = sys_io_File.getContent("res/scripts/test.hat")
        program = Parse.parse(src,langDef)
        interp = Interpreter(program,langDef)
        interp.reset([2, 10])
        outbox = interp.run()
        print(str(outbox))


class Parse:
    _hx_class_name = "Parse"
    __slots__ = ()
    _hx_statics = ["parse"]

    @staticmethod
    def parse(src,langDef):
        hasError = False
        errorMsg = ""
        tokens = list()
        registers = ["a", "b", "c", "d", "e", "f", "g", "ip"]
        def _hx_local_0(msg,ln):
            nonlocal hasError
            nonlocal errorMsg
            hasError = True
            errorMsg = ((("null" if msg is None else msg) + " on line ") + str(((ln + 1))))
            print(str(errorMsg))
        error = _hx_local_0
        def _hx_local_1(opcode,ln,val = None,lit = None):
            if (val is None):
                val = 0
            if (lit is None):
                lit = ""
            inst = _hx_AnonObject({'opcode': opcode, 'val': val, 'ln': ln})
            token = _hx_AnonObject({'inst': inst, 'lit': lit})
            tokens.append(token)
        addToken = _hx_local_1
        def _hx_local_2(lit,ln):
            num = Std.parseInt(lit)
            if (num is None):
                error((("'" + ("null" if lit is None else lit)) + "' must be a number literal"),ln)
            else:
                addToken("lit",ln,num)
        addLit = _hx_local_2
        labels = haxe_ds_StringMap()
        labels.h["top"] = 0
        lines = src.split("\n")
        _g = 0
        _g1 = len(lines)
        while (_g < _g1):
            ln = _g
            _g = (_g + 1)
            line = (lines[ln] if ln >= 0 and ln < len(lines) else None)
            startIndex = None
            comment = (line.find("--") if ((startIndex is None)) else HxString.indexOfImpl(line,"--",startIndex))
            if (comment != -1):
                line = HxString.substr(line,0,comment)
            line = StringTools.trim(line)
            if (len(line) == 0):
                continue
            s = line.split(" ")
            op = (s[0] if 0 < len(s) else None)
            if (not (op in langDef.h)):
                error((("Instruction '" + ("null" if op is None else op)) + "' is not recognized"),ln)
            elif (langDef.h.get(op,None).arg == "none"):
                addToken(op,ln)
            elif (len(s) == 1):
                error((((("Opcode '" + ("null" if op is None else op)) + "' requires a ") + HxOverrides.stringOrNull(langDef.h.get(op,None).arg)) + " argument"),ln)
            elif (op == "mark"):
                labels.h[(s[1] if 1 < len(s) else None)] = len(tokens)
            elif (langDef.h.get(op,None).arg == "reg"):
                reg = python_internal_ArrayImpl.indexOf(registers,(s[1] if 1 < len(s) else None),None)
                if (reg == -1):
                    error((HxOverrides.stringOrNull((s[1] if 1 < len(s) else None)) + " is not a valid register name"),ln)
                else:
                    addToken(op,ln,reg)
            elif (langDef.h.get(op,None).arg == "label"):
                addToken(op,ln,0,(s[1] if 1 < len(s) else None))
            elif (langDef.h.get(op,None).arg == "val"):
                addLit((s[1] if 1 < len(s) else None),ln)
            elif (langDef.h.get(op,None).arg == "vals"):
                _g2 = 1
                _g3 = len(s)
                while (_g2 < _g3):
                    i = _g2
                    _g2 = (_g2 + 1)
                    addLit((s[i] if i >= 0 and i < len(s) else None),ln)
        _g = 0
        while (_g < len(tokens)):
            token = (tokens[_g] if _g >= 0 and _g < len(tokens) else None)
            _g = (_g + 1)
            op = token.inst.opcode
            if (langDef.h.get(op,None).arg == "label"):
                if (token.lit in labels.h):
                    tmp = labels.h.get(token.lit,None)
                    token.inst.val = tmp
                else:
                    error((("Label '" + HxOverrides.stringOrNull(token.lit)) + "' is not defined"),token.inst.ln)
        if hasError:
            return []
        def _hx_local_5():
            def _hx_local_4(token):
                return token.inst
            return list(map(_hx_local_4,tokens))
        return _hx_local_5()


class Std:
    _hx_class_name = "Std"
    __slots__ = ()
    _hx_statics = ["parseInt"]

    @staticmethod
    def parseInt(x):
        if (x is None):
            return None
        try:
            return int(x)
        except BaseException as _g:
            base = 10
            _hx_len = len(x)
            foundCount = 0
            sign = 0
            firstDigitIndex = 0
            lastDigitIndex = -1
            previous = 0
            _g = 0
            _g1 = _hx_len
            while (_g < _g1):
                i = _g
                _g = (_g + 1)
                c = (-1 if ((i >= len(x))) else ord(x[i]))
                if (((c > 8) and ((c < 14))) or ((c == 32))):
                    if (foundCount > 0):
                        return None
                    continue
                else:
                    c1 = c
                    if (c1 == 43):
                        if (foundCount == 0):
                            sign = 1
                        elif (not (((48 <= c) and ((c <= 57))))):
                            if (not (((base == 16) and ((((97 <= c) and ((c <= 122))) or (((65 <= c) and ((c <= 90))))))))):
                                break
                    elif (c1 == 45):
                        if (foundCount == 0):
                            sign = -1
                        elif (not (((48 <= c) and ((c <= 57))))):
                            if (not (((base == 16) and ((((97 <= c) and ((c <= 122))) or (((65 <= c) and ((c <= 90))))))))):
                                break
                    elif (c1 == 48):
                        if (not (((foundCount == 0) or (((foundCount == 1) and ((sign != 0))))))):
                            if (not (((48 <= c) and ((c <= 57))))):
                                if (not (((base == 16) and ((((97 <= c) and ((c <= 122))) or (((65 <= c) and ((c <= 90))))))))):
                                    break
                    elif ((c1 == 120) or ((c1 == 88))):
                        if ((previous == 48) and ((((foundCount == 1) and ((sign == 0))) or (((foundCount == 2) and ((sign != 0))))))):
                            base = 16
                        elif (not (((48 <= c) and ((c <= 57))))):
                            if (not (((base == 16) and ((((97 <= c) and ((c <= 122))) or (((65 <= c) and ((c <= 90))))))))):
                                break
                    elif (not (((48 <= c) and ((c <= 57))))):
                        if (not (((base == 16) and ((((97 <= c) and ((c <= 122))) or (((65 <= c) and ((c <= 90))))))))):
                            break
                if (((foundCount == 0) and ((sign == 0))) or (((foundCount == 1) and ((sign != 0))))):
                    firstDigitIndex = i
                foundCount = (foundCount + 1)
                lastDigitIndex = i
                previous = c
            if (firstDigitIndex <= lastDigitIndex):
                digits = HxString.substring(x,firstDigitIndex,(lastDigitIndex + 1))
                try:
                    return (((-1 if ((sign == -1)) else 1)) * int(digits,base))
                except BaseException as _g:
                    return None
            return None


class StringTools:
    _hx_class_name = "StringTools"
    __slots__ = ()
    _hx_statics = ["isSpace", "ltrim", "rtrim", "trim", "replace"]

    @staticmethod
    def isSpace(s,pos):
        if (((len(s) == 0) or ((pos < 0))) or ((pos >= len(s)))):
            return False
        c = HxString.charCodeAt(s,pos)
        if (not (((c > 8) and ((c < 14))))):
            return (c == 32)
        else:
            return True

    @staticmethod
    def ltrim(s):
        l = len(s)
        r = 0
        while ((r < l) and StringTools.isSpace(s,r)):
            r = (r + 1)
        if (r > 0):
            return HxString.substr(s,r,(l - r))
        else:
            return s

    @staticmethod
    def rtrim(s):
        l = len(s)
        r = 0
        while ((r < l) and StringTools.isSpace(s,((l - r) - 1))):
            r = (r + 1)
        if (r > 0):
            return HxString.substr(s,0,(l - r))
        else:
            return s

    @staticmethod
    def trim(s):
        return StringTools.ltrim(StringTools.rtrim(s))

    @staticmethod
    def replace(s,sub,by):
        _this = (list(s) if ((sub == "")) else s.split(sub))
        return by.join([python_Boot.toString1(x1,'') for x1 in _this])


class haxe_IMap:
    _hx_class_name = "haxe.IMap"
    __slots__ = ()


class haxe_ds_StringMap:
    _hx_class_name = "haxe.ds.StringMap"
    __slots__ = ("h",)
    _hx_fields = ["h"]

    def __init__(self):
        self.h = dict()



class haxe_iterators_ArrayIterator:
    _hx_class_name = "haxe.iterators.ArrayIterator"
    __slots__ = ("array", "current")
    _hx_fields = ["array", "current"]
    _hx_methods = ["hasNext", "next"]

    def __init__(self,array):
        self.current = 0
        self.array = array

    def hasNext(self):
        return (self.current < len(self.array))

    def next(self):
        def _hx_local_3():
            def _hx_local_2():
                _hx_local_0 = self
                _hx_local_1 = _hx_local_0.current
                _hx_local_0.current = (_hx_local_1 + 1)
                return _hx_local_1
            return python_internal_ArrayImpl._get(self.array, _hx_local_2())
        return _hx_local_3()



class python_Boot:
    _hx_class_name = "python.Boot"
    __slots__ = ()
    _hx_statics = ["keywords", "toString1", "fields", "simpleField", "getInstanceFields", "getSuperClass", "getClassFields", "prefixLength", "unhandleKeywords"]

    @staticmethod
    def toString1(o,s):
        if (o is None):
            return "null"
        if isinstance(o,str):
            return o
        if (s is None):
            s = ""
        if (len(s) >= 5):
            return "<...>"
        if isinstance(o,bool):
            if o:
                return "true"
            else:
                return "false"
        if (isinstance(o,int) and (not isinstance(o,bool))):
            return str(o)
        if isinstance(o,float):
            try:
                if (o == int(o)):
                    return str(Math.floor((o + 0.5)))
                else:
                    return str(o)
            except BaseException as _g:
                return str(o)
        if isinstance(o,list):
            o1 = o
            l = len(o1)
            st = "["
            s = (("null" if s is None else s) + "\t")
            _g = 0
            _g1 = l
            while (_g < _g1):
                i = _g
                _g = (_g + 1)
                prefix = ""
                if (i > 0):
                    prefix = ","
                st = (("null" if st is None else st) + HxOverrides.stringOrNull(((("null" if prefix is None else prefix) + HxOverrides.stringOrNull(python_Boot.toString1((o1[i] if i >= 0 and i < len(o1) else None),s))))))
            st = (("null" if st is None else st) + "]")
            return st
        try:
            if hasattr(o,"toString"):
                return o.toString()
        except BaseException as _g:
            pass
        if hasattr(o,"__class__"):
            if isinstance(o,_hx_AnonObject):
                toStr = None
                try:
                    fields = python_Boot.fields(o)
                    _g = []
                    _g1 = 0
                    while (_g1 < len(fields)):
                        f = (fields[_g1] if _g1 >= 0 and _g1 < len(fields) else None)
                        _g1 = (_g1 + 1)
                        x = ((("" + ("null" if f is None else f)) + " : ") + HxOverrides.stringOrNull(python_Boot.toString1(python_Boot.simpleField(o,f),(("null" if s is None else s) + "\t"))))
                        _g.append(x)
                    fieldsStr = _g
                    toStr = (("{ " + HxOverrides.stringOrNull(", ".join([x1 for x1 in fieldsStr]))) + " }")
                except BaseException as _g:
                    return "{ ... }"
                if (toStr is None):
                    return "{ ... }"
                else:
                    return toStr
            if isinstance(o,Enum):
                o1 = o
                l = len(o1.params)
                hasParams = (l > 0)
                if hasParams:
                    paramsStr = ""
                    _g = 0
                    _g1 = l
                    while (_g < _g1):
                        i = _g
                        _g = (_g + 1)
                        prefix = ""
                        if (i > 0):
                            prefix = ","
                        paramsStr = (("null" if paramsStr is None else paramsStr) + HxOverrides.stringOrNull(((("null" if prefix is None else prefix) + HxOverrides.stringOrNull(python_Boot.toString1(o1.params[i],s))))))
                    return (((HxOverrides.stringOrNull(o1.tag) + "(") + ("null" if paramsStr is None else paramsStr)) + ")")
                else:
                    return o1.tag
            if hasattr(o,"_hx_class_name"):
                if (o.__class__.__name__ != "type"):
                    fields = python_Boot.getInstanceFields(o)
                    _g = []
                    _g1 = 0
                    while (_g1 < len(fields)):
                        f = (fields[_g1] if _g1 >= 0 and _g1 < len(fields) else None)
                        _g1 = (_g1 + 1)
                        x = ((("" + ("null" if f is None else f)) + " : ") + HxOverrides.stringOrNull(python_Boot.toString1(python_Boot.simpleField(o,f),(("null" if s is None else s) + "\t"))))
                        _g.append(x)
                    fieldsStr = _g
                    toStr = (((HxOverrides.stringOrNull(o._hx_class_name) + "( ") + HxOverrides.stringOrNull(", ".join([x1 for x1 in fieldsStr]))) + " )")
                    return toStr
                else:
                    fields = python_Boot.getClassFields(o)
                    _g = []
                    _g1 = 0
                    while (_g1 < len(fields)):
                        f = (fields[_g1] if _g1 >= 0 and _g1 < len(fields) else None)
                        _g1 = (_g1 + 1)
                        x = ((("" + ("null" if f is None else f)) + " : ") + HxOverrides.stringOrNull(python_Boot.toString1(python_Boot.simpleField(o,f),(("null" if s is None else s) + "\t"))))
                        _g.append(x)
                    fieldsStr = _g
                    toStr = (((("#" + HxOverrides.stringOrNull(o._hx_class_name)) + "( ") + HxOverrides.stringOrNull(", ".join([x1 for x1 in fieldsStr]))) + " )")
                    return toStr
            if (o == str):
                return "#String"
            if (o == list):
                return "#Array"
            if callable(o):
                return "function"
            try:
                if hasattr(o,"__repr__"):
                    return o.__repr__()
            except BaseException as _g:
                pass
            if hasattr(o,"__str__"):
                return o.__str__([])
            if hasattr(o,"__name__"):
                return o.__name__
            return "???"
        else:
            return str(o)

    @staticmethod
    def fields(o):
        a = []
        if (o is not None):
            if hasattr(o,"_hx_fields"):
                fields = o._hx_fields
                if (fields is not None):
                    return list(fields)
            if isinstance(o,_hx_AnonObject):
                d = o.__dict__
                keys = d.keys()
                handler = python_Boot.unhandleKeywords
                for k in keys:
                    if (k != '_hx_disable_getattr'):
                        a.append(handler(k))
            elif hasattr(o,"__dict__"):
                d = o.__dict__
                keys1 = d.keys()
                for k in keys1:
                    a.append(k)
        return a

    @staticmethod
    def simpleField(o,field):
        if (field is None):
            return None
        field1 = (("_hx_" + field) if ((field in python_Boot.keywords)) else (("_hx_" + field) if (((((len(field) > 2) and ((ord(field[0]) == 95))) and ((ord(field[1]) == 95))) and ((ord(field[(len(field) - 1)]) != 95)))) else field))
        if hasattr(o,field1):
            return getattr(o,field1)
        else:
            return None

    @staticmethod
    def getInstanceFields(c):
        f = (list(c._hx_fields) if (hasattr(c,"_hx_fields")) else [])
        if hasattr(c,"_hx_methods"):
            f = (f + c._hx_methods)
        sc = python_Boot.getSuperClass(c)
        if (sc is None):
            return f
        else:
            scArr = python_Boot.getInstanceFields(sc)
            scMap = set(scArr)
            _g = 0
            while (_g < len(f)):
                f1 = (f[_g] if _g >= 0 and _g < len(f) else None)
                _g = (_g + 1)
                if (not (f1 in scMap)):
                    scArr.append(f1)
            return scArr

    @staticmethod
    def getSuperClass(c):
        if (c is None):
            return None
        try:
            if hasattr(c,"_hx_super"):
                return c._hx_super
            return None
        except BaseException as _g:
            pass
        return None

    @staticmethod
    def getClassFields(c):
        if hasattr(c,"_hx_statics"):
            x = c._hx_statics
            return list(x)
        else:
            return []

    @staticmethod
    def unhandleKeywords(name):
        if (HxString.substr(name,0,python_Boot.prefixLength) == "_hx_"):
            real = HxString.substr(name,python_Boot.prefixLength,None)
            if (real in python_Boot.keywords):
                return real
        return name


class python_internal_ArrayImpl:
    _hx_class_name = "python.internal.ArrayImpl"
    __slots__ = ()
    _hx_statics = ["indexOf", "_get", "_set"]

    @staticmethod
    def indexOf(a,x,fromIndex = None):
        _hx_len = len(a)
        l = (0 if ((fromIndex is None)) else ((_hx_len + fromIndex) if ((fromIndex < 0)) else fromIndex))
        if (l < 0):
            l = 0
        _g = l
        _g1 = _hx_len
        while (_g < _g1):
            i = _g
            _g = (_g + 1)
            if HxOverrides.eq(a[i],x):
                return i
        return -1

    @staticmethod
    def _get(x,idx):
        if ((idx > -1) and ((idx < len(x)))):
            return x[idx]
        else:
            return None

    @staticmethod
    def _set(x,idx,v):
        l = len(x)
        while (l < idx):
            x.append(None)
            l = (l + 1)
        if (l == idx):
            x.append(v)
        else:
            x[idx] = v
        return v


class HxOverrides:
    _hx_class_name = "HxOverrides"
    __slots__ = ()
    _hx_statics = ["eq", "stringOrNull", "modf", "mod"]

    @staticmethod
    def eq(a,b):
        if (isinstance(a,list) or isinstance(b,list)):
            return a is b
        return (a == b)

    @staticmethod
    def stringOrNull(s):
        if (s is None):
            return "null"
        else:
            return s

    @staticmethod
    def modf(a,b):
        if (b == 0.0):
            return float('nan')
        elif (a < 0):
            if (b < 0):
                return -(-a % (-b))
            else:
                return -(-a % b)
        elif (b < 0):
            return a % (-b)
        else:
            return a % b

    @staticmethod
    def mod(a,b):
        if (a < 0):
            if (b < 0):
                return -(-a % (-b))
            else:
                return -(-a % b)
        elif (b < 0):
            return a % (-b)
        else:
            return a % b


class python_internal_MethodClosure:
    _hx_class_name = "python.internal.MethodClosure"
    __slots__ = ("obj", "func")
    _hx_fields = ["obj", "func"]
    _hx_methods = ["__call__"]

    def __init__(self,obj,func):
        self.obj = obj
        self.func = func

    def __call__(self,*args):
        return self.func(self.obj,*args)



class HxString:
    _hx_class_name = "HxString"
    __slots__ = ()
    _hx_statics = ["charCodeAt", "indexOfImpl", "substring", "substr"]

    @staticmethod
    def charCodeAt(s,index):
        if ((((s is None) or ((len(s) == 0))) or ((index < 0))) or ((index >= len(s)))):
            return None
        else:
            return ord(s[index])

    @staticmethod
    def indexOfImpl(s,_hx_str,startIndex):
        if (_hx_str == ""):
            length = len(s)
            if (startIndex < 0):
                startIndex = (length + startIndex)
                if (startIndex < 0):
                    startIndex = 0
            if (startIndex > length):
                return length
            else:
                return startIndex
        return s.find(_hx_str, startIndex)

    @staticmethod
    def substring(s,startIndex,endIndex = None):
        if (startIndex < 0):
            startIndex = 0
        if (endIndex is None):
            return s[startIndex:]
        else:
            if (endIndex < 0):
                endIndex = 0
            if (endIndex < startIndex):
                return s[endIndex:startIndex]
            else:
                return s[startIndex:endIndex]

    @staticmethod
    def substr(s,startIndex,_hx_len = None):
        if (_hx_len is None):
            return s[startIndex:]
        else:
            if (_hx_len == 0):
                return ""
            if (startIndex < 0):
                startIndex = (len(s) + startIndex)
                if (startIndex < 0):
                    startIndex = 0
            return s[startIndex:(startIndex + _hx_len)]


class sys_io_File:
    _hx_class_name = "sys.io.File"
    __slots__ = ()
    _hx_statics = ["getContent"]

    @staticmethod
    def getContent(path):
        f = python_lib_Builtins.open(path,"r",-1,"utf-8",None,"")
        content = f.read(-1)
        f.close()
        return content

Math.NEGATIVE_INFINITY = float("-inf")
Math.POSITIVE_INFINITY = float("inf")
Math.NaN = float("nan")
Math.PI = python_lib_Math.pi

python_Boot.keywords = set(["and", "del", "from", "not", "with", "as", "elif", "global", "or", "yield", "assert", "else", "if", "pass", "None", "break", "except", "import", "raise", "True", "class", "exec", "in", "return", "False", "continue", "finally", "is", "try", "def", "for", "lambda", "while"])
python_Boot.prefixLength = len("_hx_")

Main.main()
