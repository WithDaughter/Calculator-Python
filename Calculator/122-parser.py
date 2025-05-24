'''
#include <iostream>
#include <format> // C++ 20
#include <sstream>
#include <cctype>
//#include <stdexcept>

#include "Main.h"

using namespace std;

enum class TokenType {
	None,
	Name,
	Number,
	Operator,
	Assign,
	Let,
	LParan,
	RParan,
	End,
	Quit
};

class Token {
	char op;
	TokenType kind;
	double value;
	string name;
public:
	Token() {}
	Token(TokenType kind) : kind{kind} {}
	Token(TokenType kind, double value) : kind{kind}, value{value} {}
	Token(TokenType kind, char op) : kind{kind}, op{op} {}
	Token(TokenType kind, string n) : kind{kind}, name{n} {}
	TokenType GetTokenType() const {
		return kind;
	}
	double GetValue() const {
		return value;
	}
	char GetOperator() const {
		return op;
	}
	string GetName() const {
		return name;
	}
};

class Lexer {
	bool isFull{false};
	int index{0};
	Token buffer;
public:
	Token GetToken() {
		if (isFull) {
			isFull = false;
			return buffer;
		}
		char ch;
		cin >> ch;
		switch (ch) {
		case 'q':
			return Token{TokenType::Quit};
		case ';':
			return Token{TokenType::End};
		case '(':
			return Token{TokenType::LParan};
		case ')':
			return Token{TokenType::RParan};
		case '+': case '-': case '*': case '/':
			return Token{TokenType::Operator, ch};
		case '=':
			return Token{TokenType::Assign};
		case '.':
		case '0': case '1': case '2': case '3': case '4':
		case '5': case '6': case '7': case '8': case '9':
			return Token{TokenType::Number, getNumber()};
		default:
			if (isalpha(ch) || ch == '_') {
				string s = getName(ch);
				if (s == "let")
					return Token{TokenType::Let};
				return Token{TokenType::Name, getName(ch)};
			}
			throw runtime_error("올바른 토큰이 아닙니다.");
		}
	}
	void UnGetToken(Token t) {
		buffer = t;
		isFull = true;
	}
private:
	string getName(char ch) {
		string s{ch};
		while (true) {
			cin.get(ch);
			if (!isalpha(ch) && !isdigit(ch) && ch != '_') {
				cin.unget();
				cout << endl << "토큰: " << s << endl;
				return s;
			}
			s += ch;
		}
	}
	double getNumber() {
		cin.unget();
		double num;
		cin >> num;
		return num;
	}
};

Lexer lex;

// 구문 해석기
class Parser {
public:
	double Expression() {
		double left = term();
		while (true) {
			Token t = lex.GetToken();
			if (!isExpression(t)) {
				lex.UnGetToken(t);
				return left;
			}
			double right = term();
			left = calculate(left, t.GetOperator(), right);
		}
	}
private:
	double declaration(Token t) {
		Token t = lex.GetToken();
		if (t.GetTokenType() != TokenType::Name)
			throw runtime_error("변수 선언에 변수 이름이 없음");

	}
	bool isExpression(Token t) {
		TokenType tt = t.GetTokenType();
		if (tt != TokenType::Operator || !(t.GetOperator() == '+' || t.GetOperator() == '-'))
			return false;
		return true;
	}
	double term() {
		double left = primary();
		while (true) {
			Token t = lex.GetToken();
			if (!isTerm(t)) {
				lex.UnGetToken(t);
				return left;
			}
			double right = primary();
			left = calculate(left, t.GetOperator(), right);
		}
	}
	bool isTerm(Token t) {
		TokenType tt = t.GetTokenType();
		if (tt != TokenType::Operator || !(t.GetOperator() == '*' || t.GetOperator() == '/'))
			return false;
		return true;
	}
	double primary() {
		Token t = lex.GetToken();
		if (t.GetTokenType() != TokenType::LParan) {
			return t.GetValue();
		}
		double ex = Expression();
		t = lex.GetToken();
		if (t.GetTokenType() != TokenType::RParan) {
			throw runtime_error("() 짝이 안 맞습니다.");
		}
		return ex;
	}
	double calculate(double n1, char op, double n2) {
		switch (op) {
		case '+': return n1 + n2;
		case '-': return n1 - n2;
		case '*': return n1 * n2;
		case '/': return n1 / n2; // ToDo: 0으로 나누는 문제
		}
	}
};

class Calculator {
public:
	void Calculate() {
		double result;
		while (true) {
			cout << "> ";
			try {
				Token t = lex.GetToken();
				if (t.GetTokenType() == TokenType::Quit) {
					cout << "\r";
					break;
				} else if (t.GetTokenType() == TokenType::End) {
					// 결과 출력 : ToDo 계산식
					std::cout << format("\r= {}\n", result);
				} else {
					lex.UnGetToken(t);
					result = Parser().Expression();
				}
			} catch (const exception& e) {
				result = 0;
				cout << e.what() << endl;
			}
		}
	}
};

int main()
{
	// OOP: 계산에 참여하는 객체들
	cout << "계산식을 입력하세요." << endl;
	Calculator calc = Calculator();
	calc.Calculate();
}
'''