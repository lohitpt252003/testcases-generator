from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from codegen import CodeGenerator
from error_handler import ErrorHandler

class STCLCompiler:
    def compile(self, source):
        # Lexical analysis
        lexer = Lexer(source)
        
        # Parsing
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Semantic analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        if ErrorHandler.has_errors():
            return "\n".join(ErrorHandler.errors)
            
        # Code generation
        generator = CodeGenerator()
        return generator.generate(ast)