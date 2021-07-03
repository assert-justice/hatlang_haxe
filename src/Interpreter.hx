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
        pastStates.resize(0);
        runState = RunState.Paused;
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
    }
    public function cycle() {
        var ip = state.registers[7];
        if (ip >= program.length){
            stop();
        }
        if(runState == RunState.Stopped){return;}
        var inst = program[ip];
        var op = inst.opcode;
        var val = inst.val;
        trace(op);
        if (langDef[op].pops > state.stack.length){
            error("Cannot execute instruction '" + op + "': Stack must have " + langDef[op].pops + " values, it has " + state.stack.length);
            return;
        }
        switch op {
            case "in":
                if (state.inbox.length == 0){
                    runState = RunState.Stopped;
                }
                else {
                    state.stack.push(state.inbox.pop());
                }
            case "out":
                state.outbox.push(state.stack.pop());
            case "dupe": 
                state.stack.push(state.stack[state.stack.length-1]);
            case "del": 
                state.stack.pop();
            case "zero": 
                state.stack.push(0);
            // case "rand": 
            //     state.stack.push(0);
            case "inc": 
                state.stack[state.stack.length-1]++;
            case "dec": 
                state.stack[state.stack.length-1]--;
            case "add": 
                bin((a,b)->a+b);
            case "sub": 
                bin((a,b)->a-b);
            case "mul": 
                bin((a,b)->a*b);
            // case "div": 
            //     bin((a,b)->(a/b);
            case "mod": 
                bin((a,b)->a%b);
            case "lit":
                state.stack.push(val);
            case "print":
                trace(state.stack);   
            default:
                trace("Opcode '" + op + "' not implimented");
        }
        if (ip == state.registers[7]){
            state.registers[7]++;
        }
    }
}