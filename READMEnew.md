# DETAILED CLASS & FUNCTION SPECIFICATION
## C ↔ Python Converter

---

## PART 1: TOKEN & LEXER

### token.py

**Class: Token**
- Purpose: Represent single token from source code
- Attributes:
  - `type` (str): Token category (TOK_INT, TOK_ID, TOK_PLUS, etc)
  - `value` (str): Token content ("int", "x", "+", "hello", etc)
  - `line` (int): Line number where token appears (1-indexed)
  - `col` (int): Column number where token appears (1-indexed)
- Methods:
  - `__init__(type, value, line, col)`: Initialize token
  - `__repr__()`: String representation for debugging

---

### keywords.py

Already have. But functions you'll use:

**Functions:**
- `is_c_keyword(word: str) -> bool`: Check if word is C keyword
- `is_python_keyword(word: str) -> bool`: Check if word is Python keyword
- `is_keyword(word: str, language: str) -> bool`: Check for specific language
- `get_token_type(word: str, language: str) -> str`: Return token type for keyword

**Dicts (predefined):**
- `C_KEYWORDS`: dict mapping C keywords to token types
- `PYTHON_KEYWORDS`: dict mapping Python keywords to token types
- `TOKEN_TO_KEYWORD_C`: reverse map (token type → C keyword)
- `TOKEN_TO_KEYWORD_PY`: reverse map (token type → Python keyword)

---

### lexer.py

**Class: CLexer**
- Purpose: Convert C source code into tokens
- Attributes:
  - `code` (str): Input C source code
  - `pos` (int): Current position in code
  - `line` (int): Current line number (1-indexed)
  - `col` (int): Current column number (1-indexed)
  - `tokens` (list): Accumulated tokens

- Methods:
  - `__init__(code: str)`: Initialize lexer with C code
  - `tokenize() -> list[Token]`: **Main method** - return all tokens
  
  - **Helper: Navigation**
    - `_current_char() -> str`: Get char at pos
    - `_peek_char() -> str`: Look ahead without advancing
    - `_advance() -> None`: Move pos forward, update line/col
  
  - **Helper: Skip**
    - `_skip_whitespace() -> None`: Skip spaces, tabs, newlines
    - `_skip_line_comment() -> None`: Skip // comment to newline
    - `_skip_block_comment() -> None`: Skip /* */ comment
  
  - **Helper: Read tokens**
    - `_read_string() -> Token`: Read "..." string, handle escapes
    - `_read_number() -> Token`: Read 123 or 3.14
    - `_read_identifier() -> Token`: Read identifier, check if keyword
    - `_read_operator() -> Token`: Read +, -, ++, ==, etc
  
  - **Helper: Manage tokens**
    - `_add_token(token: Token) -> None`: Append token to list


**Class: PyLexer**
- Purpose: Convert Python source code into tokens
- Attributes: Same as CLexer
  - `code` (str): Input Python source code
  - `pos` (int): Current position
  - `line` (int): Current line number
  - `col` (int): Current column number
  - `tokens` (list): Accumulated tokens
  - `indent_level` (int): Track indentation (Python-specific)

- Methods:
  - `__init__(code: str)`: Initialize lexer with Python code
  - `tokenize() -> list[Token]`: **Main method** - return all tokens
  
  - **Helper: Navigation** (same as CLexer)
    - `_current_char() -> str`
    - `_peek_char() -> str`
    - `_advance() -> None`
  
  - **Helper: Skip** (same as CLexer)
    - `_skip_whitespace() -> None`
    - `_skip_line_comment() -> None` (# comment)
    - `_skip_block_comment() -> None` (""" """ or ''' ''')
  
  - **Helper: Read tokens** (same as CLexer + Python-specific)
    - `_read_string() -> Token`: Handle ", ', """
    - `_read_f_string() -> Token`: Handle f"..." f-strings
    - `_read_number() -> Token`: Handle 123, 3.14
    - `_read_identifier() -> Token`
    - `_read_operator() -> Token`
  
  - **Helper: Indentation** (Python-specific)
    - `_handle_indentation() -> None`: Track indent level changes
    - `_add_indent_token() -> None`: Add INDENT token
    - `_add_dedent_token() -> None`: Add DEDENT token

---

## PART 2: AST NODES

### ast_nodes.py

**Base Class: ASTNode**
- Purpose: Base class for all syntax tree nodes
- No attributes, no methods. Just parent class.

**Class: Literal**
- Purpose: Represent constants (numbers, strings)
- Attributes:
  - `value` (any): The literal value (42, 3.14, "hello", True, None)

**Class: Identifier**
- Purpose: Represent variable/function names
- Attributes:
  - `name` (str): Variable or function name

**Class: VarDeclaration**
- Purpose: Represent variable declaration
- Attributes:
  - `data_type` (str): Type ("int", "float", "char", etc)
  - `name` (str): Variable name
  - `init_value` (ASTNode): Initial value (can be None)

**Class: Assignment**
- Purpose: Represent variable assignment
- Attributes:
  - `target` (str): Variable being assigned to
  - `value` (ASTNode): Value being assigned

**Class: BinaryOp**
- Purpose: Represent binary operations
- Attributes:
  - `left` (ASTNode): Left operand
  - `op` (str): Operator ("+", "-", "==", "&&", etc)
  - `right` (ASTNode): Right operand

**Class: UnaryOp**
- Purpose: Represent unary operations
- Attributes:
  - `op` (str): Operator ("!", "-", "++", "--", etc)
  - `operand` (ASTNode): Operand

**Class: FunctionCall**
- Purpose: Represent function invocation
- Attributes:
  - `name` (str): Function name
  - `args` (list[ASTNode]): Function arguments

**Class: IfStatement**
- Purpose: Represent if-else statement
- Attributes:
  - `condition` (ASTNode): Condition to test
  - `body` (list[ASTNode]): Statements if true
  - `else_body` (list[ASTNode]): Statements if false (can be None)

**Class: ForLoop**
- Purpose: Represent for loop
- Attributes:
  - `init` (ASTNode): Initialization (e.g., int i = 0)
  - `condition` (ASTNode): Loop condition
  - `increment` (ASTNode): Increment expression
  - `body` (list[ASTNode]): Loop body

**Class: WhileLoop**
- Purpose: Represent while loop
- Attributes:
  - `condition` (ASTNode): Loop condition
  - `body` (list[ASTNode]): Loop body

**Class: DoWhileLoop**
- Purpose: Represent do-while loop (C only)
- Attributes:
  - `body` (list[ASTNode]): Loop body
  - `condition` (ASTNode): Loop condition (checked after body)

**Class: FunctionDef**
- Purpose: Represent function definition
- Attributes:
  - `return_type` (str): Return type ("int", "void", etc)
  - `name` (str): Function name
  - `params` (list): Function parameters
  - `body` (list[ASTNode]): Function body

**Class: ClassDef**
- Purpose: Represent class definition (Python)
- Attributes:
  - `name` (str): Class name
  - `base_class` (str): Parent class name (can be None)
  - `body` (list[ASTNode]): Class body

**Class: Block**
- Purpose: Represent code block { }
- Attributes:
  - `statements` (list[ASTNode]): Statements in block

**Class: ReturnStatement**
- Purpose: Represent return statement
- Attributes:
  - `value` (ASTNode): Value to return (can be None)

**Class: BreakStatement**
- Purpose: Represent break statement
- Attributes: None

**Class: ContinueStatement**
- Purpose: Represent continue statement
- Attributes: None

**Class: ArrayAccess**
- Purpose: Represent array indexing
- Attributes:
  - `array` (ASTNode): Array being accessed
  - `index` (ASTNode): Index value

**Class: StructAccess**
- Purpose: Represent struct member access
- Attributes:
  - `object` (ASTNode): Struct/object
  - `field` (str): Field name

---

## PART 3: PARSER

### parser.py

**Class: CParser**
- Purpose: Convert C tokens into Abstract Syntax Tree
- Attributes:
  - `tokens` (list[Token]): Input tokens from lexer
  - `pos` (int): Current position in tokens list

- Methods:
  - `__init__(tokens: list[Token])`: Initialize parser
  - `parse() -> list[ASTNode]`: **Main method** - return complete AST
  
  - **Parse main constructs**
    - `_parse_statement() -> ASTNode`: Parse single statement
    - `_parse_var_declaration() -> VarDeclaration`: Parse "int x;" or "int x = 5;"
    - `_parse_assignment() -> Assignment`: Parse "x = 5;"
    - `_parse_if_statement() -> IfStatement`: Parse "if (cond) { } else { }"
    - `_parse_for_loop() -> ForLoop`: Parse "for (init; cond; incr) { }"
    - `_parse_while_loop() -> WhileLoop`: Parse "while (cond) { }"
    - `_parse_do_while_loop() -> DoWhileLoop`: Parse "do { } while (cond);"
    - `_parse_function_call() -> FunctionCall`: Parse "func(args);"
    - `_parse_function_def() -> FunctionDef`: Parse "int func(params) { }"
    - `_parse_block() -> list[ASTNode]`: Parse "{ statements }"
    - `_parse_return() -> ReturnStatement`: Parse "return value;"
    - `_parse_break() -> BreakStatement`: Parse "break;"
    - `_parse_continue() -> ContinueStatement`: Parse "continue;"
  
  - **Parse expressions (recursive descent)**
    - `_parse_expression() -> ASTNode`: Parse full expression with operators
    - `_parse_logical_or() -> ASTNode`: Parse "a || b"
    - `_parse_logical_and() -> ASTNode`: Parse "a && b"
    - `_parse_equality() -> ASTNode`: Parse "a == b" or "a != b"
    - `_parse_comparison() -> ASTNode`: Parse "a < b", "a <= b", etc
    - `_parse_additive() -> ASTNode`: Parse "a + b" or "a - b"
    - `_parse_multiplicative() -> ASTNode`: Parse "a * b" or "a / b"
    - `_parse_unary() -> ASTNode`: Parse "!a", "-a", "++a"
    - `_parse_primary() -> ASTNode`: Parse literals, identifiers, (expr)
  
  - **Helper: Token navigation**
    - `_current_token() -> Token`: Get current token
    - `_peek_token() -> Token`: Look ahead
    - `_advance() -> Token`: Move to next token, return previous
    - `_is_at_end() -> bool`: Check if at EOF
  
  - **Helper: Token validation**
    - `_expect(token_type: str) -> Token`: Assert token type, advance, or error
    - `_match(token_types: list[str]) -> bool`: Check if current matches any type
    - `_consume(token_type: str, message: str) -> Token`: Expect and consume or error


**Class: PyParser**
- Purpose: Convert Python tokens into Abstract Syntax Tree
- Attributes:
  - `tokens` (list[Token]): Input tokens from lexer
  - `pos` (int): Current position in tokens list
  - `indent_stack` (list): Track indentation levels

- Methods:
  - `__init__(tokens: list[Token])`: Initialize parser
  - `parse() -> list[ASTNode]`: **Main method** - return complete AST
  
  - **Parse main constructs** (similar to CParser but Python syntax)
    - `_parse_statement() -> ASTNode`: Parse single statement
    - `_parse_var_declaration() -> VarDeclaration`: Parse "x = 0" (infer type)
    - `_parse_assignment() -> Assignment`: Parse "x = 5"
    - `_parse_if_statement() -> IfStatement`: Parse "if cond:" with indentation
    - `_parse_for_loop() -> ForLoop`: Parse "for i in range():" 
    - `_parse_while_loop() -> WhileLoop`: Parse "while cond:"
    - `_parse_function_def() -> FunctionDef`: Parse "def func(params):" with indentation
    - `_parse_class_def() -> ClassDef`: Parse "class Name(Base):" with indentation
    - `_parse_block() -> list[ASTNode]`: Parse indented block
    - `_parse_return() -> ReturnStatement`: Parse "return value"
    - `_parse_break() -> BreakStatement`: Parse "break"
    - `_parse_continue() -> ContinueStatement`: Parse "continue"
  
  - **Parse expressions** (same structure as CParser)
    - `_parse_expression() -> ASTNode`
    - `_parse_logical_or() -> ASTNode`
    - `_parse_logical_and() -> ASTNode`
    - `_parse_equality() -> ASTNode`
    - `_parse_comparison() -> ASTNode`
    - `_parse_additive() -> ASTNode`
    - `_parse_multiplicative() -> ASTNode`
    - `_parse_unary() -> ASTNode`
    - `_parse_primary() -> ASTNode`
  
  - **Helper: Indentation** (Python-specific)
    - `_check_indentation() -> None`: Validate indentation matches expected
    - `_push_indent() -> None`: Push new indent level
    - `_pop_indent() -> None`: Pop indent level


**Class: ParseError (Exception)**
- Purpose: Represent parsing errors
- Attributes:
  - `message` (str): Error description
  - `line` (int): Line where error occurred
  - `col` (int): Column where error occurred

---

## PART 4: CODE GENERATORS

### py_generator.py

**Class: PythonGenerator**
- Purpose: Convert C AST back into Python source code
- Attributes:
  - `ast` (list[ASTNode]): Input AST from C parser
  - `output` (list[str]): Accumulated output lines
  - `indent_level` (int): Current indentation level (0, 1, 2, ...)

- Methods:
  - `__init__(ast: list[ASTNode])`: Initialize generator
  - `generate() -> str`: **Main method** - return complete Python code string
  
  - **Generate for each node type**
    - `_generate_node(node: ASTNode) -> None`: Dispatch based on node type
    - `_generate_var_declaration(node: VarDeclaration) -> None`: "int x;" → "x = 0"
    - `_generate_assignment(node: Assignment) -> None`: "x = 5;" → "x = 5"
    - `_generate_binary_op(node: BinaryOp) -> str`: Return expression string
    - `_generate_unary_op(node: UnaryOp) -> str`: Return expression string
    - `_generate_function_call(node: FunctionCall) -> None`: "printf(...)" → "print(...)"
    - `_generate_if_statement(node: IfStatement) -> None`: "if (cond) { }" → "if cond:"
    - `_generate_for_loop(node: ForLoop) -> None`: "for (;;) { }" → "for i in range():"
    - `_generate_while_loop(node: WhileLoop) -> None`: "while (cond) { }" → "while cond:"
    - `_generate_function_def(node: FunctionDef) -> None`: "int foo() { }" → "def foo():"
    - `_generate_block(statements: list[ASTNode]) -> None`: Generate indented block
    - `_generate_return(node: ReturnStatement) -> None`: "return x;" → "return x"
    - `_generate_break(node: BreakStatement) -> None`: "break;" → "break"
    - `_generate_continue(node: ContinueStatement) -> None`: "continue;" → "continue"
  
  - **Helper: Formatting**
    - `_emit(line: str) -> None`: Add line to output with indentation
    - `_indent() -> str`: Return indentation string
    - `_increase_indent() -> None`: Indent deeper
    - `_decrease_indent() -> None`: Unindent
  
  - **Helper: Mapping & Type inference**
    - `_map_c_function_to_python(name: str) -> str`: "printf" → "print", "strlen" → "len"
    - `_map_c_operator_to_python(op: str) -> str`: "==" stays "==", "++" → "+= 1"
    - `_infer_python_type(value: ASTNode) -> str`: Guess Python type from value


### c_generator.py

**Class: CGenerator**
- Purpose: Convert Python AST back into C source code
- Attributes:
  - `ast` (list[ASTNode]): Input AST from Python parser
  - `output` (list[str]): Accumulated output lines
  - `indent_level` (int): Current indentation level (0, 1, 2, ...)

- Methods:
  - `__init__(ast: list[ASTNode])`: Initialize generator
  - `generate() -> str`: **Main method** - return complete C code string
  
  - **Generate for each node type**
    - `_generate_node(node: ASTNode) -> None`: Dispatch based on node type
    - `_generate_var_declaration(node: VarDeclaration) -> None`: "x = 0" → "int x;"
    - `_generate_assignment(node: Assignment) -> None`: "x = 5" → "x = 5;"
    - `_generate_binary_op(node: BinaryOp) -> str`: Return expression string
    - `_generate_unary_op(node: UnaryOp) -> str`: Return expression string
    - `_generate_function_call(node: FunctionCall) -> None`: "print(...)" → "printf(...)"
    - `_generate_if_statement(node: IfStatement) -> None`: "if cond:" → "if (cond) {"
    - `_generate_for_loop(node: ForLoop) -> None`: "for i in range():" → "for (;;)"
    - `_generate_while_loop(node: WhileLoop) -> None`: "while cond:" → "while (cond)"
    - `_generate_function_def(node: FunctionDef) -> None`: "def foo():" → "int foo() {"
    - `_generate_block(statements: list[ASTNode]) -> None`: Generate { } block
    - `_generate_return(node: ReturnStatement) -> None`: "return x" → "return x;"
    - `_generate_break(node: BreakStatement) -> None`: "break" → "break;"
    - `_generate_continue(node: ContinueStatement) -> None`: "continue" → "continue;"
  
  - **Helper: Formatting**
    - `_emit(line: str) -> None`: Add line to output with indentation
    - `_indent() -> str`: Return indentation string
    - `_increase_indent() -> None`: Indent deeper
    - `_decrease_indent() -> None`: Unindent
  
  - **Helper: Mapping & Type inference**
    - `_map_python_function_to_c(name: str) -> str`: "print" → "printf", "len" → "strlen"
    - `_map_python_operator_to_c(op: str) -> str`: "and" → "&&", "or" → "||"
    - `_infer_c_type(value: ASTNode) -> str`: Guess C type from Python value

---

## PART 5: CONVERTERS (Orchestrators)

### c_to_py.py

**Class: CToPhythonConverter**
- Purpose: Orchestrate complete C-to-Python conversion pipeline
- Attributes:
  - `errors` (list[str]): Collected errors
  - `warnings` (list[str]): Collected warnings

- Methods:
  - `__init__()`: Initialize
  - `convert(c_code: str) -> dict`: **Main method**
    - Input: C source code string
    - Process:
      1. Create CLexer, tokenize
      2. Create CParser, parse tokens → AST
      3. Create PythonGenerator, generate Python code
    - Output: Dictionary with keys:
      - `success` (bool): True if conversion succeeded
      - `output` (str): Generated Python code
      - `warnings` (list[str]): Warnings during conversion
      - `errors` (list[str]): Errors encountered
  
  - **Helper: Error handling**
    - `_handle_error(error: Exception) -> None`: Catch and log error
    - `_add_warning(message: str) -> None`: Add warning message


### py_to_c.py

**Class: PythonToCConverter**
- Purpose: Orchestrate complete Python-to-C conversion pipeline
- Attributes:
  - `errors` (list[str]): Collected errors
  - `warnings` (list[str]): Collected warnings

- Methods:
  - `__init__()`: Initialize
  - `convert(py_code: str) -> dict`: **Main method**
    - Input: Python source code string
    - Process:
      1. Create PyLexer, tokenize
      2. Create PyParser, parse tokens → AST
      3. Create CGenerator, generate C code
    - Output: Dictionary with keys:
      - `success` (bool): True if conversion succeeded
      - `output` (str): Generated C code
      - `warnings` (list[str]): Warnings during conversion
      - `errors` (list[str]): Errors encountered
  
  - **Helper: Error handling**
    - `_handle_error(error: Exception) -> None`: Catch and log error
    - `_add_warning(message: str) -> None`: Add warning message

---

## PART 6: WEB API

### server.py (Flask Application)

**Function: create_app() -> Flask**
- Purpose: Create and configure Flask application
- Returns: Configured Flask app instance

**Function: setup_routes(app: Flask) -> None**
- Purpose: Register all API routes with app

**Route Handler: POST /api/convert**
- Purpose: Main API endpoint for code conversion
- Request JSON body:
  - `code` (str): Source code to convert
  - `source_lang` (str): "c" or "python"
  - `target_lang` (str): "c" or "python"
- Response JSON:
  - `success` (bool): Conversion succeeded
  - `output` (str): Converted code
  - `warnings` (list[str]): Warnings
  - `errors` (list[str]): Errors

**Route Handler: GET /api/languages**
- Purpose: Return supported languages and conversion pairs
- Response JSON:
  - `languages` (list[str]): ["c", "python"]
  - `pairs` (list[dict]): Supported conversion pairs

**Route Handler: GET /api/health**
- Purpose: Health check endpoint
- Response JSON:
  - `status` (str): "ok"
  - `timestamp` (str): Current time

---

### routes.py

**Class: ConvertRoute**
- Purpose: Handle conversion route logic
- Methods:
  - `handle(code: str, source_lang: str, target_lang: str) -> dict`: **Main handler**
    - Validate languages
    - Select appropriate converter (CToPhythonConverter or PythonToCConverter)
    - Call converter.convert()
    - Return result dictionary
  
  - `_validate_languages(source: str, target: str) -> bool`: Check if valid pair
  
  - `_sanitize_input(code: str) -> str`: Clean/validate input


### middleware.py

**Function: error_handler(error: Exception) -> dict**
- Purpose: Global error handling for all routes
- Input: Any exception
- Output: JSON response with error details

**Function: rate_limiter() -> Decorator**
- Purpose: Limit API requests (e.g., 100 requests per 15 minutes)
- Prevents abuse

**Function: cors_handler() -> Decorator**
- Purpose: Handle Cross-Origin Resource Sharing
- Allows React frontend to call backend API

---

## CONVERSION FLOW SUMMARY

```
C Code
  ↓
CLexer.tokenize() → [Token, Token, ...]
  ↓
CParser.parse() → [ASTNode, ASTNode, ...]
  ↓
PythonGenerator.generate() → str (Python code)

Python Code
  ↓
PyLexer.tokenize() → [Token, Token, ...]
  ↓
PyParser.parse() → [ASTNode, ASTNode, ...]
  ↓
CGenerator.generate() → str (C code)
```

Web chooses direction. API calls right converter. Profit. 👊
