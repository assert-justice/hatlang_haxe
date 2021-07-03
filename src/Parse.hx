import LanguageDef;
typedef Token = {
    var inst : Instruction;
    var lit : String;
}
typedef Instruction = {
    var opcode : String;
    var val : Int;
    var ln : Int;
}
// typedef ParseStatus = {
//     var hasError : Bool;
//     var errorMsg : String;
// }
class Parse {
    public static function parse(src:String, langDef:Map<String,InstructionDef>) {
        var hasError = false;
        var errorMsg = "";
        var tokens = new Array<Token>();
        //var insts = new Array<Instruction>();
        var registers = ["a","b","c","d","e","f","g","ip"];
        function error(msg : String, ln : Int) {
            hasError = true;
            errorMsg = msg + " on line " + (ln + 1);
            trace(errorMsg);
        }
        function addToken(opcode, ln, val = 0, lit = "") {
            var inst : Instruction = {opcode: opcode, val: val, ln: ln};
            var token : Token = {inst: inst, lit: lit};
            tokens.push(token);
        }
        var labels = new Map<String,Int>();
        labels.set("top", 0);
        var lines = src.split('\n');
        for (ln in 0...lines.length) {
            var line = lines[ln];
            var comment = line.indexOf("-");
            if (comment != -1){
                line = line.substr(0, comment);
            }
            line = StringTools.trim(line);
            if (line.length == 0) continue;
            var s = line.split(" ");
            var op = s[0];
            if(!langDef.exists(op)){
                error("Instruction '" + op + "' is not recognized", ln);
            }
            else if (langDef[op].arg == "none"){
                addToken(op, ln);
            }
            else if(s.length == 1){
                error("Opcode '" + op + "' requires a " + langDef[op].arg + " argument", ln);
            }
            else if (op == "mark"){
                labels.set(s[1], tokens.length);
            }
            else if(langDef[op].arg == "reg"){
                var reg = registers.indexOf(s[1]);
                if (reg == -1){
                    error(s[1] + " is not a valid register name", ln);
                }
                else{
                    addToken(op, ln, reg);
                }
            }
            else if (langDef[op].arg == "label"){
                addToken(op, ln, 0, s[1]);
            }
            else if (langDef[op].arg == "val"){
                var val = Std.parseInt(s[1]);
                if(val == null){
                    error("'" + s[1] + "' must be a number literal", ln);
                }
                else{
                    addToken(op, ln, val);
                }
            }
            else if (langDef[op].arg == "vals"){
                for (i in 1...s.length) {
                    var val = Std.parseInt(s[i]);
                    if(val == null){
                        error("'" + s[i] + "' must be a number literal", ln);
                        break;
                    }
                    else{
                        addToken("lit", ln, val);
                    }
                }
            }
        }
        //if(hasError){return [];}
        // resolve labels
        for (token in tokens) {
            var op = token.inst.opcode;
            if(langDef[op].arg == "label"){
                if(labels.exists(token.lit)){
                    token.inst.val = labels[token.lit];
                }
                else{
                    error("Label '" + token.lit + "' is not defined", token.inst.ln);
                }
            }
        }
        if(hasError){return [];}
        return tokens.map(token -> token.inst);
    }
}