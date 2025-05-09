#include <iostream>
#include <string>
#include <vector>
#include <memory>

using namespace std;

// AST Node types
struct ASTNode {
    virtual ~ASTNode() = default;
    virtual double eval(int depth=0) const = 0;
    virtual string str(int depth) const = 0;
};

struct NumberNode : ASTNode {
    double value;
    
    NumberNode(double v) : value(v) {}
    
    double eval(int depth) const override {
        cout << string(depth*2, ' ') 
             << "Evaluating Number: " << value << endl;
        return value;
    }
    
    string str(int depth) const override {
        return string(depth*2, ' ') + to_string(value);
    }
};

struct AddNode : ASTNode {
    unique_ptr<ASTNode> left;
    unique_ptr<ASTNode> right;
    
    AddNode(unique_ptr<ASTNode> l, unique_ptr<ASTNode> r)
        : left(move(l)), right(move(r)) {}
    
    double eval(int depth) const override {
        cout << string(depth*2, ' ') << "Evaluating AddNode\n";
        double l = left->eval(depth+1);
        double r = right->eval(depth+1);
        
        cout << string(depth*2, ' ') 
             << l << " + " << r << " = " << (l+r) << endl;
        return l + r;
    }
    
    string str(int depth) const override {
        string indent(depth*2, ' ');
        return indent + "Add(\n" + 
               left->str(depth+1) + ",\n" + 
               right->str(depth+1) + "\n" + 
               indent + ")";
    }
};

// Parser
class Parser {
    vector<string> tokens;
    size_t pos = 0;
    
    unique_ptr<ASTNode> parse_add() {
        auto left = parse_number();
        while (peek() == "+") {
            consume();
            auto right = parse_number();
            left = make_unique<AddNode>(move(left), move(right));
        }
        return left;
    }
    
    unique_ptr<ASTNode> parse_number() {
        double value = stod(tokens[pos++]);
        return make_unique<NumberNode>(value);
    }
    
    string peek() const {
        return pos < tokens.size() ? tokens[pos] : "";
    }
    
    void consume() { pos++; }

public:
    Parser(vector<string> t) : tokens(move(t)) {}
    
    unique_ptr<ASTNode> parse() {
        return parse_add();
    }
};

// Tokenizer
vector<string> tokenize(const string& expr) {
    vector<string> tokens;
    string current;
    
    for (char c : expr) {
        if (isspace(c)) {
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
            continue;
        }
        
        if (isdigit(c) || c == '.') {
            current += c;
        } else {
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
            tokens.push_back(string(1, c));
        }
    }
    
    if (!current.empty()) {
        tokens.push_back(current);
    }
    
    return tokens;
}

int main() {
    string expr = "1 + 2 + 3+2+221000*00010*5/1";
    
    try {
        auto tokens = tokenize(expr);
        Parser parser(move(tokens));
        auto ast = parser.parse();
        
        cout << "AST Structure:\n" << ast->str(0) << "\n\n";
        cout << "Evaluation Steps:\n";
        double result = ast->eval();
        cout << "\nFinal Result: " << result << endl;
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
    }
    
    return 0;
}