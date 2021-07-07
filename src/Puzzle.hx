import Parse.Instruction;
import LanguageDef.InstructionDef;

class Puzzle {
    var preludes : Array<Array<Instruction>>;
    var impls : Array<Array<Instruction>>;
    var answers : Map<Int,Array<Int>>;
    var name = "";
    var desc = "";
    public function new() {
        preludes = new Array<Array<Instruction>>();
        impls = new Array<Array<Instruction>>();
        answers = new Map<Int,Array<Int>>();
    }
    public function load(src : String, langDef : Map<String,InstructionDef>) {
        var mode = "none";
        var pre = new Array<String>();
        var impl = new Array<String>();
        for (line in src.split("\n")) {
            //if (StringTools.startsWith(line, "--")) continue;
            if (StringTools.startsWith(line, "#")){
                var idx = line.indexOf(" ");
                var start = line.substr(1);
                var end = "";
                if(idx != -1){
                    start = line.substr(1, idx - 1);
                    end = StringTools.trim(line.substr(idx));
                }
                mode = start;
                line = end;
                if (mode == "pre"){
                    if (pre.length > 0){
                        preludes.push(Parse.parse(pre.join("\n"), langDef));
                        pre.resize(0);
                    }
                }
                else if (mode == "impl"){
                    if (impl.length > 0){
                        impls.push(Parse.parse(impl.join("\n"), langDef));
                        impl.resize(0);
                    }
                }
            }
            switch mode {
                case "name":
                    if(name.length > 0) name += "\n";
                    name += line;
                case "desc":
                    if(desc.length > 0) desc += "\n";
                    desc += line;
                case "pre":
                    pre.push(line);
                case "impl":
                    impl.push(line);
            }
        }
        preludes.push(Parse.parse(pre.join("\n"), langDef));
        impls.push(Parse.parse(impl.join("\n"), langDef));
        trace("Name: " + name);
        trace("Description: " + desc);
        trace("preludes");
        for (pre in preludes) {
            trace("\t" + pre.toString());
        }
        trace("impls");
        for (impl in impls) {
            trace("\t" + impl.toString());
        }
    }
    public function validate(program : Array<Instruction>) {
        //
    }
}