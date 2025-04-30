class ErrorHandler:
    errors = []
    
    @classmethod
    def add_error(cls, line, column, message):
        cls.errors.append(f"Line {line}:{column} - {message}")
        
    @classmethod
    def clear_errors(cls):
        cls.errors = []
        
    @classmethod
    def has_errors(cls):
        return len(cls.errors) > 0