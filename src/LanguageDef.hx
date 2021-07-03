typedef InstructionDef = {
    var arg : String;
    var pops : Int;
}
class LanguageDef {
    public static function getDef(content : String) {
        var insts = new Map<String,InstructionDef>();
        var lines = content.split('\n');
        for (line in lines) {
            var lin = line.split('|');
            if(lin.length < 3) continue;
            var inst:InstructionDef = {arg: lin[2], pops: Std.parseInt(lin[3])};
            insts.set(StringTools.replace(lin[1], "*", ""), inst);
            //insts.push(inst);
            //trace(inst);
        }
        return insts;
    }
}