temp1 = 'case "{}":\n\t{}();\n'
temp2 = 'function {}(){}\n'

f = open('res/langdef.txt')
ld = f.read().splitlines()
f.close()
lang_def = []
doc1 = open('doc1.txt', 'w')
doc2 = open('doc2.txt', 'w')
for line in ld:
    s = line.split('|')
    if len(s) == 2:
        continue
    op = s[1]
    if op[-1] == '*':
        op = op[:-1]
    if op in ['--', 'mark', 'lits']:
        continue
    #print(temp1.format(op, op))
    doc1.write(temp1.format(op, op))
    doc2.write(temp2.format(op, '{\n\t//\n}'))