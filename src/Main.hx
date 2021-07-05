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
        var interp = new Interpreter(program, langDef);
        interp.reset([2, 10]);
        var outbox = interp.run();
        trace(outbox);
    }
}