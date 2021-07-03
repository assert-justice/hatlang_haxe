import Interpreter.RunState;
import Parse.Instruction;
import LanguageDef.InstructionDef;

class Main {
    static public function main():Void {
        var langDef : Map<String,InstructionDef>;
        var program : Array<Instruction>;
        #if sys
        var langDefStr = sys.io.File.getContent("res/langdef.txt");
        langDef = LanguageDef.getDef(langDefStr);
        var src = sys.io.File.getContent("res/scripts/test.hat");
        program = Parse.parse(src, langDef);
        #end
        // for (inst in program) {
        //     trace(inst);
        // }
        var interp = new Interpreter(program, langDef);
        interp.runState = RunState.Running;
        while (interp.runState == RunState.Running){
            interp.cycle();
        }
    }
}