import Interpreter.InterpreterStatus;
import Parse.Instruction;
import LanguageDef.InstructionDef;

typedef PuzzleSummary = {
    var inputs : Array<Array<Int>>;
    var outputs : Array<Array<Int>>;
    var bestSize : Int;
    var bestStackSize : Int;
    var bestCycles : Int;
    var bestRegUse : Int;
    var rands : Array<Array<Instruction>>;
}

class Puzzle {
    var preludes : Array<Array<Instruction>>;
    var rands : Array<Array<Instruction>>;
    var impls : Array<Array<Instruction>>;
    var answers : Map<Int,Array<Int>>;
    var langDef : Map<String,InstructionDef>;
    var name = "";
    var desc = "";
    public function new(langDef : Map<String,InstructionDef>) {
        this.langDef = langDef;
        preludes = new Array<Array<Instruction>>();
        rands = new Array<Array<Instruction>>();
        impls = new Array<Array<Instruction>>();
        answers = new Map<Int,Array<Int>>();
    }
    public function load(src : String) {
        var mode = "none";
        var prog = new Array<String>();
        for (line in src.split("\n")) {
            if (StringTools.startsWith(line, "#")){
                var src = prog.join("\n");
                prog.resize(0);
                if (mode == "pre"){
                    preludes.push(Parse.parse(src, langDef));
                }
                else if (mode == "rand"){
                    rands.push(Parse.parse(src, langDef));
                }
                else if (mode == "impl"){
                    impls.push(Parse.parse(src, langDef));
                }
                else if (mode == "name"){
                    name += src;
                }
                else if (mode == "desc"){
                    desc += src;
                }
                line = line.substr(1);
                var words = line.split(" ");
                mode = StringTools.trim(words.shift());
                line = words.join(" ");
            }
            prog.push(line);
        }
        trace("Name: " + name);
        trace("Description: " + desc);
        var summary : PuzzleSummary;
        var interp = new Interpreter(langDef);
        summary.inputs = [];
        // for (impl in impls) {
        //     var agg = new Array<InterpreterStatus>();
        //     for (pre in preludes) {
        //         interp.setProgram(pre);
        //         var outbox = interp.run();
        //         agg.push(interp.getStatus());
        //         trace(outbox);
        //     }
        // }
        // trace("preludes");
        // for (pre in preludes) {
        //     trace("\t" + pre.toString());
        // }
        // trace("rands");
        // for (rand in rands) {
        //     trace("\t" + rand.toString());
        // }
        // trace("impls");
        // for (impl in impls) {
        //     trace("\t" + impl.toString());
        // }
    }
    public function validate(program : Array<Instruction>) {
        //
    }
}