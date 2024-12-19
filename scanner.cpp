#include <iostream>
#include <cctype>
#include <string>
#include <vector>
#include <map>
#include <unordered_set>
#include <fstream>
#include <sstream>
#include <getopt.h>

// token types
enum TokenType {
    Keyword,
    Identifier,
    Number,
    Operator,
    EndOfFile,
    LeftParenthesis,
    RightParenthesis,
    LeftCurlyBrace,
    RightCurlyBrace,
    Colon,
    Quotation,
    Comma,
    Unknown
};

// token struct
struct Token {
    TokenType type;
    std::string value;
};

// key words
std::unordered_set<std::string> keywords({
    "register_sequencial",
    "for", 
    "to", 
    "begin_generate",
    "end_generate",
    "set_seq_attr",
    // "use_max_acc",
    // "allow_flexible_operation",
    "register_op",
    // "Conv",
    // "FC",
    "break",
    "report",
    "if", 
    "else", 
    "while", 
    "return", 
    "set_soc_attr",
    "generate_success",
    "true",
    "false"
});

std::unordered_set<std::string> operators({
    "+", "-", "*", "/", "=", "==", "!=", ">=", "<=", ">", "<", "&&", "||"
});

std::unordered_set<std::string> special_chars({
    "+", "-", "*", "/", "=", "(", ")", "{", "}", ":", "\"", " ", "\n", ",", "\t", ">", "<", "!", "&", "|"
});
// std::unordered_set<std::string> keywords({"foo", "bar", "baz"});




class Scanner {
public:
    Scanner(const std::string& input) : input(input), position(0), raised_error(false) {}

    Token get_next_token() {
        // decide the starting point of the token, filter out the invalid characters
        while (position < input.size()) {
            char current = input[position];

            // filter the comment line
            if (current == '/' && position + 1 < input.size() && input[position + 1] == '/') {
                while (position < input.size() && current != '\n') {
                    position++;
                    current = input[position];
                }
                continue;
            }

            // skip whitespaces
            if (isspace(current) or current == '\n') {
                position++;
                continue;
            }

            // identify numbers
            if (isdigit(current)) {
                return scan_number();
            }

            // identify identifiers and keywords
            if (isalpha(current)) {
                return scan_identifier_or_keyword();
            }

            // identify operators
            if (is_operator(current)) {
                // Token token = {TokenType::Operator, std::string(1, current)};
                // position++;
                // return token;
                return scan_operator();
            }

            if (current == '(') {
                Token token = {TokenType::LeftParenthesis, std::string(1, current)};
                position++;
                return token;
            }

            if (current == ')') {
                Token token = {TokenType::RightParenthesis, std::string(1, current)};
                position++;
                return token;
            }

            if (current == '{') {
                Token token = {TokenType::LeftCurlyBrace, std::string(1, current)};
                position++;
                return token;
            }

            if (current == '}') {
                Token token = {TokenType::RightCurlyBrace, std::string(1, current)};
                position++;
                return token;
            }

            if (current == ':') {
                Token token = {TokenType::Colon, std::string(1, current)};
                position++;
                return token;
            }

            if (current == '\"') {
                Token token = {TokenType::Quotation, std::string(1, current)};
                position++;
                return token;
            }

            if (current == ',') {
                Token token = {TokenType::Comma, std::string(1, current)};
                position++;
                return token;
            }

            // Unknown character
            // do we need error handling here?
            std::cerr << "Warning: Unknown character: " << current << std::endl;
            raised_error = true;

            position++;
        }

        // end of file
        return {TokenType::EndOfFile, ""};
    }

    bool hasError() {
        return raised_error;
    }

private:
    std::string input;
    size_t position;
    bool raised_error;

    Token scan_number() {
        size_t start = position;
        // while (position < input.size() && !special_chars.count(std::string(1, input[position]))) {
        while (position < input.size() && isalnum(input[position])) {
            position++;
        }

        for (size_t i = start; i < position; i++) {
            if (!isdigit(input[i])) {
                raised_error = true;
                return {TokenType::Unknown, input.substr(start, position - start)};
            }
        }
        return {TokenType::Number, input.substr(start, position - start)};
    }

    Token scan_identifier_or_keyword() {
        size_t start = position;
        // won't need to handle special character as we handled it during the input parsing
        // while (position < input.size() && !special_chars.count(std::string(1, input[position]))) {
        while (position < input.size() && (isalnum(input[position]) || input[position] == '_')) {
            position++;
        }

        // Error checking: if we don't stop after receiving invalid words, we will need this
        // for (size_t i = start; i < position; i++) {
        //     if (!isalnum(input[i]) && input[i] != '_') {
        //         raised_error = true;
        //         return {TokenType::Unknown, input.substr(start, position - start)};
        //     }
        // }

        std::string value = input.substr(start, position - start);
        if (keywords.count(value)) {
            return {TokenType::Keyword, value};
        } else {
            return {TokenType::Identifier, value};
        }
    }

    Token scan_operator() {
        size_t start = position;
        while (position < input.size() && is_operator(input[position])) {
            position++;
        }

        // the equivalent FSM is like first get the operator input, and it will enter the reject states
        std::string value = input.substr(start, position - start);
        if (operators.count(value)) {
            return {TokenType::Operator, value};
        } else {
            raised_error = true;
            return {TokenType::Unknown, value};
        }

    }

    bool is_operator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/' || c == '=' || c == '!'|| c == '>' || c == '<' || c == '&' || c == '|';
    }
};

// output to stdout
void print_token(const Token& token) {
    std::string typeStr;
    switch (token.type) {
        case TokenType::Keyword: typeStr = "Keyword"; break;
        case TokenType::Identifier: typeStr = "Identifier"; break;
        case TokenType::Number: typeStr = "Number"; break;
        case TokenType::Operator: typeStr = "Operator"; break;
        case TokenType::EndOfFile: typeStr = "End of File"; break;
        case TokenType::LeftParenthesis: typeStr = "Left Parenthesis"; break;
        case TokenType::RightParenthesis: typeStr = "Right Parenthesis"; break;
        case TokenType::LeftCurlyBrace: typeStr = "Left Curly Brace"; break;
        case TokenType::RightCurlyBrace: typeStr = "Right Curly Brace"; break;
        case TokenType::Colon: typeStr = "Colon"; break;
        case TokenType::Quotation: typeStr = "Quotation"; break;
        case TokenType::Comma: typeStr = "Comma"; break;

        default: typeStr = "Unknown";
    }
    if (typeStr == "Unknown") {
        std::cerr << "Warning -- Unknown token: \"" << token.value << "\""<< std::endl;
    } else if (typeStr == "End of File") {
        
    } else {
        // std::cout << "Token: " << typeStr << ", Value: " << token.value << std::endl;
        std::cout << "<" << typeStr << ", \"" << token.value << "\">" << std::endl;
    }
    
}

// file option
void dump_token( std::fstream& outfile , const Token& token) {
    std::string typeStr;
    switch (token.type) {
        case TokenType::Keyword: typeStr = "Keyword"; break;
        case TokenType::Identifier: typeStr = "Identifier"; break;
        case TokenType::Number: typeStr = "Number"; break;
        case TokenType::Operator: typeStr = "Operator"; break;
        case TokenType::EndOfFile: typeStr = "End of File"; break;
        case TokenType::LeftParenthesis: typeStr = "Left Parenthesis"; break;
        case TokenType::RightParenthesis: typeStr = "Right Parenthesis"; break;
        case TokenType::LeftCurlyBrace: typeStr = "Left Curly Brace"; break;
        case TokenType::RightCurlyBrace: typeStr = "Right Curly Brace"; break;
        case TokenType::Colon: typeStr = "Colon"; break;
        case TokenType::Quotation: typeStr = "Quotation"; break;
        case TokenType::Comma: typeStr = "Comma"; break;

        default: typeStr = "Unknown";
    }
    if (typeStr == "Unknown") {
        std::cerr << "Warning -- Unknown token: \"" << token.value << "\""<< std::endl;
    } else if (typeStr == "End of File") {
        
    } else {
        // std::cout << "Token: " << typeStr << ", Value: " << token.value << std::endl;
        outfile << "<" << typeStr << ", \"" << token.value << "\">" << std::endl;
    }
    
}


void show_help() {
    std::cout << "Usage: ./scanner [options] input_file\n"
              << "Options:\n"
              << "  -o, --output [file]     Specify the output file\n"
              << "  -c, --config [file]     Specify the config file\n"
              << "  -h, --help              Show help message\n";
}



int parse_options(std::string& in_file_name, std::string& out_file_name, int argc, char *argv[]) {
    
    static struct option long_options[] = {
        {"output", required_argument, 0, 'o'},
        {"help",   no_argument,       0, 'h'},
        {0, 0, 0, 0}
    };

    int opt;
    int option_index = 0;
    
    
    while ((opt = getopt_long(argc, argv, "o:c:h", long_options, &option_index)) != -1) {
        switch (opt) {
            case 'o':
                out_file_name = optarg;
                break;
            case 'h':
                show_help();
                return -1;
            default:
                show_help();
                return -1;
        }
    }
    
    if (optind < argc) {
        // this is in file name
        in_file_name = argv[optind];
    } else {
        return -1;
    }
    return 0;
}



int main(int argc, char *argv[]) {
    // std::string input = "if x == 10 return x + 20 @@ else while y";
    std::string in_file_name;
    std::string out_file_name;
    std::fstream output_file;
    
    if (parse_options(in_file_name, out_file_name, argc, argv) == -1) {
        return 1;
    }

    if (in_file_name.empty()) {
        std::cerr << "input file not specified, use \"input1.hl\" as default\n";
        in_file_name = "input1.hl";
    }

    std::fstream input_file(in_file_name, std::ios::in);
    if (!input_file.is_open()) {
        std::cerr << "Error: Could not open input file" << std::endl;
        return 1;
    }
    

    if (out_file_name.empty()) {
        std::cerr << "output file not specified, use stdout as default\n";
    } else {
        output_file.open(out_file_name, std::ios::out);
        if (!output_file.is_open()) {
            std::cerr << "Error: Could not open output file" << std::endl;
            return 1;
        }
        // redirect std::cout to output file
        // std::cout.rdbuf(output_file.rdbuf());
    }
    
    // Read the file into the buffer
    std::stringstream buffer;
    buffer << input_file.rdbuf();

    std::string input = buffer.str();  // Convert buffer into string


    Scanner scanner(input);
    
    Token token;
    do {
        
        token = scanner.get_next_token();
        if (out_file_name.empty()) {
            print_token(token);
        } else {
            dump_token(output_file, token);
        }
    } while (token.type != TokenType::EndOfFile);


    if (!out_file_name.empty()) {
        output_file.close();
    }

    if (scanner.hasError()) {
        std::cerr << "Error: Scanner encountered an error during lexical analysis" << std::endl;
        return 1;
    }


    return 0;
}
