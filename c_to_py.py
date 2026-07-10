class CToPythonConverter:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def convert(self, c_code: str) -> dict:
        """
        Main method to convert C source code to Python code.

        Args:
            c_code (str): C source code string.

        Returns:
            dict: Dictionary with keys:
                - success (bool): True if conversion succeeded.
                - output (str): Generated Python code.
                - warnings (list[str]): Warnings during conversion.
                - errors (list[str]): Errors encountered.
        """
        try:
            lexer = CLexer(c_code)
            tokens = lexer.tokenize()

            parser = CParser(tokens)
            ast = parser.parse()

            generator = PythonGenerator(ast)
            python_code = generator.generate()

            return {
                'success': True,
                'output': python_code,
                'warnings': self.warnings,
                'errors': self.errors
            }
        except Exception as e:
            self._handle_error(e)
            return {
                'success': False,
                'output': '',
                'warnings': self.warnings,
                'errors': self.errors
            }

    def _handle_error(self, error: Exception) -> None:
        """
        Catch and log error.

        Args:
            error (Exception): Exception object.
        """
        self.errors.append(str(error))

    def _add_warning(self, message: str) -> None:
        """
        Add warning message.

        Args:
            message (str): Warning message.
        """
        self.warnings.append(message)