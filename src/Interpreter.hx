import Parse.Instruction;
import LanguageDef;

typedef InterpreterState = {
    var stack : Array<Int>;
    var inbox : Array<Int>;
    var outbox : Array<Int>;
    var callStack : Array<Int>;
    var registers : Array<Int>;
    var cycle : Int;
    var registerUse : Int;
    var maxStackSize : Int;
}

enum RunState {
    Running;
    Paused;
    Stopped;
}

class Interpreter {
    public var state : InterpreterState;
    public var pastStates : Array<InterpreterState>;
    public var program : Array<Instruction>;
    public var runState : RunState;
    public var cycleMod : Int = 10;
    var langDef : Map<String,InstructionDef>;
    var ip = 0;

    public function new(program : Array<Instruction>, langDef : Map<String,InstructionDef>) {
        this.program = program;
        pastStates = new Array<InterpreterState>();
        state = {
            stack: new Array<Int>(),
            inbox: new Array<Int>(),
            outbox: new Array<Int>(),
            callStack: new Array<Int>(),
            registers: [for (_ in 0...8) 0],
            cycle: 0,
            registerUse: 0,
            maxStackSize: 0
        }
        pastStates.push(state);
        this.langDef = langDef;
    }
    function error(msg : String) {
        var op = program[state.registers[7]];
        runState = RunState.Stopped;
        trace(msg + " on line " + (op.ln + 1));
    }
    public function reset(inbox : Array<Int> = null) {
        flash(pastStates[0]);
        if(inbox != null){
            state.inbox = inbox;
        }
    }
    public function flash(state : InterpreterState) {
        this.state = state;
        pastStates.resize(1);
        runState = RunState.Paused;
    }
    public function run() {
        runState = RunState.Running;
        while(runState == RunState.Running){
            cycle();
        }
        return state.outbox;
    }
    public function stop() {
        runState = RunState.Stopped;
    }
    public function prevState() {
        //
    }
    function bin(f:(Int,Int)->Int) {
        var b = state.stack.pop();
        var a = state.stack.pop();
        state.stack.push(f(a,b));
        clamp();
    }
    function clamp(){
        var val = state.stack[state.stack.length - 1];
        if (val > 9999) val = 9999;
        if (val < -9999) val = -9999;
        state.stack[state.stack.length - 1] = val;
    }
    public function cycle() {
        ip = state.registers[7];
        if (ip >= program.length){
            stop();
        }
        if(runState == RunState.Stopped){return;}
        var inst = program[ip];
        var op = inst.opcode;
        var val = inst.val;
        if (langDef[op].pops > state.stack.length){
            error("Cannot execute instruction '" + op + "': Stack must have " + langDef[op].pops + " values, it has " + state.stack.length);
            return;
        }
        switch op {
            case "in":
                inb();
            case "out":
                out();
            case "dupe":
                dupe();
            case "swp":
                swp();
            case "del":
                del();
            case "zero":
                zero();
            case "rand":
                rand();
            case "inc":
                inc();
            case "dec":
                dec();
            case "add":
                add();
            case "sub":
                sub();
            case "mul":
                mul();
            case "div":
                div();
            case "mod":
                mod();
            case "jmp":
                jmp(val);
            case "jez":
                jez(val);
            case "jlz":
                jlz(val);
            case "jgz":
                jgz(val);
            case "jnz":
                jnz(val);
            case "srt":
                srt(val);
            case "ret":
                if (state.callStack.length == 0){
                    error("Tried to return from a subroutine but callstack empty");
                }
                else{
                    ret();
                }
            case "load":
                load(val);
            case "save":
                save(val);
            case "lit":
                lit(val);
            case "out_all":
                out_all();
            case "print":
                print();
            case "dump":
                dump();
            case "brk":
                brk();
            default: trace("Opcode '" + op + "' not implimented");
        }
        if (ip == state.registers[7]){
            state.registers[7]++;
        }
        else{
            state.registers[7] = ip;
        }
    }
    function inb(){
        if (state.inbox.length == 0){
            runState = RunState.Stopped;
        }
        else {
            state.stack.push(state.inbox.pop());
        }
    }
    function out(){
        state.outbox.push(state.stack.pop());
    }
    function dupe(){
        state.stack.push(state.stack[state.stack.length-1]);
    }
    function swp(){
        var a = state.stack.pop();
        var b = state.stack.pop();
        state.stack.push(a);
        state.stack.push(b);
    }
    function del(){
        state.stack.pop();
    }
    function zero(){
        state.stack.push(0);
    }
    function rand(){
        var val = Math.random() * 2 - 1;
        val *= 10000;
        state.stack.push(0); // not currently implimented
    }
    function inc(){
        state.stack[state.stack.length-1]++;
        clamp();
    }
    function dec(){
        state.stack[state.stack.length-1]--;
        clamp();
    }
    function add(){
        bin((a,b)->a+b);
    }
    function sub(){
        bin((a,b)->a-b);
    }
    function mul(){
        bin((a,b)->a*b);
    }
    function div(){
        bin((a,b)->Math.floor(a/b));
    }
    function mod(){
        // crudely getting Python/Haskell modulo functionality
        bin((a,b)->{
            var aneg = a < 0;
            var bneg = b < 0;
            if (aneg) a = -a;
            if (bneg) b = -b;
            var val = a % b;
            if (aneg) val = b - val;
            if (bneg) val = -val;
            return val;
        });
    }
    function jmp(val : Int){
        ip = val;
    }
    function jez(val : Int){
        if(state.stack[state.stack.length - 1] == 0) {ip = val;}
    }
    function jlz(val : Int){
        if(state.stack[state.stack.length - 1] < 0) {ip = val;}
    }
    function jgz(val : Int){
        if(state.stack[state.stack.length - 1] > 0) {ip = val;}
    }
    function jnz(val : Int){
        if(state.stack[state.stack.length - 1] != 0) {ip = val;}
    }
    function srt(val : Int){
        state.callStack.push(ip);
        ip = val;
    }
    function ret(){
        ip = state.callStack.pop();
    }
    function load(val : Int){
        state.stack.push(state.registers[val]);
        state.registerUse++;
    }
    function save(val : Int){
        state.registers[val] = state.stack.pop();
        state.registerUse++;
    }
    function brk() {
        runState = RunState.Paused;
    }
    function lit(val : Int){
        state.stack.push(val);
    }
    function out_all(){
        while(state.stack.length > 0){
            out();
        }
    }
    function print(){
        trace(state.stack[state.stack.length - 1]);
    }
    function dump(){
        trace("Inbox:     " + state.inbox.toString());
        trace("Stack:     " + state.stack.toString());
        trace("Outbox:    " + state.outbox.toString());
        trace("Registers: " + state.registers.toString());
    }
}