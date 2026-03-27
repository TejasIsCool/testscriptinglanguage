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
- Comments: "\/\/[anything]\*"
- String: '  "[anything]\*"          '
- Equals: "="
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
- Not: "!"
- Semicolon: ";"
- Numeric: "-?[0..9]\+[\\.[0..9]\*]?"
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
