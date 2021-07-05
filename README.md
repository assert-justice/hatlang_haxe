# Hatlang
A reference for the language in Hatstack.

## About
Hatlang is a low level assembly-like language. It is designed to get players and students thinking about low level computer operations particularly the stack.
In the game it is written with a visual scripting system. One of the design goals of the visual scripting system is prohibiting syntax errors. A given script may not fulfill the requirements but it is still a valid program. This has a few ramifications for the design of the language.

What is detailed here is the text version of the language where syntax errors are of course possible. The language is quite simple and so syntax errors are straightforward to recognize and report.

## The Interpreter
The Hatstack interpreter is a stack based virtual machine. Almost all of its instructions interact with the stack in one way or another.

### Labels

Some instructions refer to labels. Labels mark particular parts of the progrogram. For example you could create a label called `loop` like so:

```
mark loop
```

Now another instruction can refer to that part of the code. You can use the `jmp` instruction to jump to it for example.

Every program starts with one label defined called `top`. This refers to the top of the program at instruction `0`.

Subroutines are a special case. Instead of using a `jmp` you can use `srt` to jump to a subroutine. Then you can use `ret` to return from a subroutine.

For example you could define a subroutine to double the value on top of the stack like so:

```
-- program to double everything in the inbox
in
srt double -- call the subroutine 'double'
out
jmp top

mark double
dupe
add
ret -- returns from the subroutine having doubled whatever was on the stack
```

Then you could call `double` anywhere.

### Registers

It also has eight registers (labeled `a`, `b`, `c`, `d`, `e`, `f`, `g`, and `ip`) that you can save values to and load values from. The last register `ip` is special. That's where the instruction pointer is stored. You can save a value there to set the instruction pointer to an arbitrary value, a potentially very powerful technique. 

### Modules

Various additional modules are available such as a hard drive and display. These are "wired" into the registers.

## The Language
The following are all of the instructions and psudo instructions for Hatlang.
### Reading the table
- Name: The name of the instruction. When an instruction needs further explanation there will be an asterisk and a corrisponding note in the notes section.

- Argument: The argument the instruction takes, if any. 

    - Options are none (no argument), label (a label created with mark), reg (a register as explained above), val (a literal value), or vals (a collection of space seperated values)

- Pops: How many values the instruction pops from the stack.

- Pushes: How many values the instruction pushes to the stack.

- Description: A short description.

### The Instructions

|Name|Argument|Pops|Pushes|Description|
|---|---|---|---|---|
|Stack manipulation
|in|none|0|1|Gets a value from the inbox and pushes it to the stack.
|out|none|1|0|Pops a value from the stack and puts it to the outbox.
|dupe|none|1|2|Duplicates the value at the top of the stack and pushes it.
|swp|none|2|2|Swaps the positions of the top two elements in the stack.
|del|none|1|0|Pops and deletes the top item from the stack.
|zero|none|0|1|Pushes a zero to the stack.
|rand*|none|0|1|Pushes a random number from -999 to 999 inclusive to the stack.
|Arithmatic
|inc|none|1|1|Increments the value at the top of the stack.
|dec|none|1|1|Decrements the value at the top of the stack.
|add|none|2|1|Pops two items from the stack, adds them, and pushes the result.
|sub|none|2|1|Pops two items from the stack, subtracts the first from the second, and pushes the result.
|mul|none|2|1|Pops two items from the stack, adds them, and pushes the result.
|div*|none|2|1|Pops two items from the stack, divides the second by the first, and pushes the result.
|mod*|none|2|1|Pops two items from the stack, divides the second by the first, and pushes the remainder.
|Control Flow
|jmp|label|0|0|Unconditionally jump to a label.
|jez|label|0|0|If the top value of the stack is zero jump to the label.
|jlz|label|0|0|Jump if less than zero.
|jgz|label|0|0|Jump if greater than zero.
|jnz|label|0|0|Jump if not zero.
|srt|label|0|0|Jump to subroutine.
|ret|label|0|0|Return from subroutine.
|Register Manipulation
|load|reg|0|1|Get the value from the given register and push it.
|save|reg|1|0|Pop a value from the stack and save it to the given register.
|Psudo-Instructions
|mark|label|0|0|Used to create labels.
|--*|none|0|0|Create a comment.
|Misc
|brk|none|0|0|Pause execution at the instruction
|lit|val|0|1|Push a literal value to the stack.
|lits*|vals|0|n|Push several literal values to the stack.
|out_all*|none|0|0|For each item on the stack pop it and outbox it.
|print|none|0|0|Print the value on the top of the stack to the console.
|dump|none|0|0|Print the state of the interpreter to the console.

### Notes

`rand`: The random command complicates grading solutions somewhat. For fairness the official grade is given by the Hatstack backend which validates all programs with a set seed.

`div`: The division command in Hatstack always floors the result. So for example `4/5` equals `0`. You might expect `-4/5` to equal zero as well but it actually evaluates to `-1`.

`mod`: The modulo command is a true modulo operator, not a remainder. So `1%5` equals `1`. `-1%5` equals `4`.

`--`: Comments in hatlang are started with a double minus sign. They can appear anywhere in a line and the parser will remove anything in the line after them.

`lits`: This command is special in that it is pretty much the only example of "syntactic sugar" in the language. The parser turns this instruction into a series of `lit` instructions.

`out_all`: As stated above this command outboxes the entire stack. It is listed as popping `0` elements because if the stack is empty it will pop nothing. It will never pop more values than the stack holds and cannot produce a stack error.

## Example Programs

## Puzzles

Hatlang is designed for a puzzle game and so benefits from a special syntax for creating puzzles. Let's look at a simple example puzzle.

```
-- add test
#desc
You can do math now! For every two numbers in the inbox add them and outbox the result.

#pre
lits 5 10
out_all

#expect 15

#pre
lits 5 10 20 14
out_all

#expect 34 15

#pre
rand
rand
rand
rand
out_all

#impl
in
in
add
out
jmp top

#impl
in
dupe
in
swp
add
out
save a
jmp top
```

There are several sections labeled with `#` signs.
- `#desc` : A description for the puzzle to be displayed to the user.
- `#pre` : A prelude. A hatlang program who's outbox is used as an inbox for the user's program.
- `#expect` : An optional section after a prelude with the expected outputs of a sucessful test.
- `#impl` : A hatlang program known to work correctly. There can be several such implimentations. A user's program is graded against each one.
