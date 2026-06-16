These are the kind of stuff I want the language to support:

- Everything statement with ;

- Expressions:
  - identifier = boolExp | Expression | True | False | Number;
  - Expression = expression +-\*/ Expression;
  - Expression = expression ^ expression;
  - boolExp = True | False | Expression < > == >= <= Expression;
  - boolExp = boolExp || boolExp | boolExp && boolExp | !boolExp

- Flow:
  - If (boolExp) {}
    else {};

  - while (boolExp) {};
  
  - These are probably implemented using goto statements in the intermediate code

- Comments like `// Test`
- Print command, to debug

- Also to add: Lists, Random Generators, standard library
- This language will be interpreted by the python program,


#heading("What possible sets of tokens will i accept: ")
(I keep forgetting which comment to use, so we will have them all!)
- Comments: "\/\/[anything]\*" or "--[anything]" or "\#[anything]"
- String: '  "[anything]\*"          '
- Assignment: "="
- Add/Sub/Mul/Div/Pow/Mod: "+" | "-" | "\*" | "/" | "^" | "%"
- If: "if"
- Else: "else"
- LB: "("
- RB: ")"
- While: "while"
- SBL: "["
- SBR: "\]"
- True: "True"
- False: "False"
- Or|And: "|" | "&"
- Inequality: "<", ">", "<=", ">=" -- Also binary operators
- Equality: "=="
- Not: "!"
- Not equality: "!="
- Semicolon: ";"
- Numeric: "-?[0..9]\+[\\.[0..9]\*]?" - I do want all numbers to be complex tho
- identifier: "[a-z][a-z|\_|0..9|@]"

How to detect if we have one of those tokens?
- Cannot just split by whitespaces
  - As it won't support compact expressions, like `2+3=5` or `id1=2` or ```java if(True)```
- Cannot start reading token till one matches
  - As it would be detected as identifiers immediately.
- Elimination strategy:
  - Scan the tokens, and exclude all not possible tokens, till only one possible token + identifier. Or scan while its letters, as we have no multiple character non letter words.

- So instead, we scan the letters, till we get a non letter character. If it matches anything above, that will be made into a token. Else it is an identifier of some kind.
- For strings and comments however, we will ignore all this process, and make them into a single token. Comments will make the line completely ignored.



#heading("Parsing grammar")
#set text(size: 14pt)
$
bold("Statement_List") -> {bold("Statement")"*"} \
bold("Statement") -> cases(
  bold("Statement_List") & "| decider = {, nonconsumed", 
  "if" bold("Expression") bold("Statement_List") & "| decider = if",
  "while" bold("Expression") bold("Statement_List") & "| decider = while",
  italic("identifier") bold("assignmentExpression")";" & "| decider = "italic("identifier"),
)\
bold("assignmentExpression") -> ("=" | "+=" | "-=" | "*=" | "/=" | "^=" | "%=" | "|=" | "&=") bold("Expression")\
$- 
The expression block \
$
bold("Expression") &-> bold("Equality")\
bold("Equality") &-> bold("Comparison") (("!= | ==") bold("Comparison"))"*"\

// comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
// term           → factor ( ( "-" | "+" ) factor )* ;
// factor         → unary ( ( "/" | "*" ) unary )* ;
// unary          → ( "!" | "-" ) unary
//                | primary ;
// primary        → NUMBER | STRING | "true" | "false" | "nil"
//                | "(" expression ")" ;
// 
// Write these commented ones in the above format
bold("Comparison") &-> bold("Term") (("< | > | <= | >=") bold("Term"))"*"\
bold("Term") &-> bold("Factor") (("- | +") bold("Factor"))"*"\
bold("Factor") &-> bold("Unary") (("/ | *") bold("Unary"))"*"\
bold("Unary") &-> (("! | -") bold("Unary")) | bold("Primary")\
bold("Primary") &-> cases(
  "True" | "False" | bold("Number") | bold("String") | bold("Identifier") | "(" bold("Expression") ")"
)\


$