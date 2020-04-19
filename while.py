ID, INTEGER,TRUE,FALSE, NOT,PLUS, MINUS, MUL, DIV, AND,OR,LPAREN, RPAREN,ASSIGN,EQUAL,GT,LT,LBRACE,RBRACE ,SEMI, WHILE, DO,IF,THEN,ELSE, SKIP ,EOF = (
    'ID','INTEGER','TRUE','FALSE', 'NOT' ,'PLUS', 'MINUS', 'MUL', 'DIV','∧','∨', '(' ,')',':=','=','>','<','{','}','SEMI','WHILE','DO','IF','THEN','ELSE','SKIP','EOF'
)
ERROR = -999

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"\
        self.tokens = text.split(' ')
        #print(self.tokens)
        # self.pos is an index into self.text
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.tokens) - 1:
            self.current_token = None  # Indicates end of input
        else:
            self.current_token = self.tokens[self.pos]

    def is_integer(self, token):
        try:
            r = int(token)
            return True
        except:
            return False

    def get_next_token(self):
        """Get the next token.
        """

        while self.current_token is not None:
            #print('self.current_token',self.current_token)
            if self.current_token == '':
                self.pos += 1
                continue

            if self.current_token == 'while':
                self.advance()
                return Token(WHILE, 'while')
            if self.current_token == 'do':
                self.advance()
                return Token(DO, 'do')

            if self.current_token == 'if':
                self.advance()
                return Token(IF, 'if')
            if self.current_token == 'then':
                self.advance()
                return Token(THEN, 'then')
            if self.current_token == 'else':
                self.advance()
                return Token(ELSE, 'else')

            if self.current_token == 'skip':
                self.advance()
                return Token(SKIP, 'skip')

            if self.is_integer(self.current_token):
                the_token = Token(INTEGER, int(self.current_token))
                self.advance()
                return the_token

            if self.current_token == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_token == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_token == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_token == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_token == '∧':
                self.advance()
                return Token(AND, '∧')

            if self.current_token == '∨':
                self.advance()
                return Token(OR, '∨')


            if self.current_token == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_token == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_token == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_token == '}':
                self.advance()
                return Token(RBRACE, '}')

            if self.current_token == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_token == ':=':
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_token == '=':
                self.advance()
                return Token(EQUAL, '=')

            if self.current_token == '>':
                self.advance()
                return Token(GT, '>')

            if self.current_token == '<':
                self.advance()
                return Token(LT, '<')

            if self.current_token == 'true':
                self.advance()
                return Token(TRUE, 'true')

            if self.current_token == 'false':
                self.advance()
                return Token(FALSE, 'false')
            if self.current_token == '¬':
                self.advance()
                return Token(NOT, '¬')

            if self.current_token.isidentifier():                
                tk = Token(ID, self.current_token)
                self.advance()
                return tk

            self.error()
            

        return Token(EOF, None)


#############################

class AST(object):
    pass


class BinaryOperator(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Boolean(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
class While(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
class If(AST):
    def __init__(self,  op, cond, right, wrong):

        self.left = cond
        self.token = self.op = op
        self.right = right
        self.wrong = wrong

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
    """Represents a  block"""
    def __init__(self, list_nodes):
        self.children = []
        for node in list_nodes:
            self.children.append(node)
class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # print(self.current_token)
        if self.current_token.type == token_type:
            #print (self.current_token,'is eat')
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Number(token)
        elif token.type == ID:
            self.eat(ID)
            #print('get VAR')
            return Var(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expression()
            self.eat(RPAREN)
            return node
        

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinaryOperator(left=node, op=token, right=self.factor())

        return node
    def variable(self):
        """
        variable : ID
        """
        #print('ID',self.current_token)
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def skip(self):
        """An empty production"""
        self.eat(SKIP)
        return NoOp()

    def expression(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER 
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinaryOperator(left=node, op=token, right=self.term())

        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expression()
        node = Assign(left, token, right)
        return node

    def bool_expression(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        #print('bool_expression')
        node = self.bool_term()

        while self.current_token.type in (OR):
            token = self.current_token
            if token.type == OR:
                self.eat(OR)
            node = Boolean(left=node, op=token, right=self.bool_term())

        return node
        '''
        if self.current_token.type == TRUE:
            #print ('Boolean','true')
            node = Boolean(Number(Token(INTEGER,1)), Token(EQUAL,'='), Number(Token(INTEGER,1)))
        elif self.current_token.type == FALSE:
            node = Boolean(Number(Token(INTEGER,1)), Token(EQUAL,'='), Number(Token(INTEGER,2)))
        else:
            left = self.expression()
            token = self.current_token
            if token.type == EQUAL:
                self.eat(EQUAL)
            elif token.type == LT:
                self.eat(LT)
            elif token.type == GT:
                self.eat(GT)
            right = self.expression()
            node = Boolean(left, token, right)
        return node
        '''

    def bool_term(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        #print('bool_term')
        node = self.bool_factor()

        while self.current_token.type in (AND):
            token = self.current_token
            if token.type == AND:
                self.eat(AND)

            node = Boolean(left=node, op=token, right=self.bool_factor())

        return node
        
    def bool_factor(self):
        """factor : INTEGER """
        #print('bool_factor')
        token = self.current_token
        if self.current_token.type == TRUE:
            #print ('Boolean','true')
            node = Boolean(Number(Token(INTEGER,1)), Token(EQUAL,'='), Number(Token(INTEGER,1)))
            return node
        elif self.current_token.type == FALSE:
            node = Boolean(Number(Token(INTEGER,1)), Token(EQUAL,'='), Number(Token(INTEGER,2)))
            return node
        elif token.type == NOT:
            self.eat(NOT)
            right = self.bool_factor()
            node = Boolean(None, token, right)
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.bool_expression()
            self.eat(RPAREN)
            return node
        else:
            #print('expression here')
            left = self.expression()
            token = self.current_token
            #print('token',token.value)
            if token.type == EQUAL:
                self.eat(EQUAL)
            elif token.type == LT:
                self.eat(LT)
            elif token.type == GT:
                self.eat(GT)
            right = self.expression()
            node = Boolean(left, token, right)
            return node

    def if_statement(self):
        """
        while_statement : while ASSIGN expr
        """
        self.eat(IF)
        left = self.bool_expression()
        token = self.current_token
        if self.current_token.type == TRUE: 
            self.eat(TRUE)
        elif self.current_token.type == FALSE: 
            self.eat(FALSE)
        #print(self.current_token)
        self.eat(THEN)
        right = self.statement()
        self.eat(ELSE)
        wrong = self.statement()
        node = If( token,left,right,wrong)
        return node
    
    def while_statement(self):
        """
        while_statement : while ASSIGN expr
        """
        self.eat(WHILE)
        left = self.bool_expression()

        token = self.current_token
        if self.current_token.type == TRUE: 
            self.eat(TRUE)
        elif self.current_token.type == FALSE: 
            self.eat(FALSE)
        self.eat(DO)
        if self.current_token.type == LBRACE:
            self.eat(LBRACE)
            right = self.statement_list()
            self.eat(RBRACE)
        else:
            right = self.statement()
        #print('while')
        node = While(left, token, right)
        return node
    
    

    def program(self):
        """program : compound_statement DOT"""
        nodes = self.statement_list()
        return nodes

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()
        #print ('results',len(results))
        node = Compound(results)
        return node
    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == WHILE:
            node = self.while_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type == SKIP:
            node = self.skip()
        else:
            node = self.expression()
        return node


    
    def parse(self):
        return self.statement_list()


#############################

class ASTNodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        # print(method_name)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))



class Interpreter(ASTNodeVisitor):
    def __init__(self, parser):
        self.SYMBOL_TABLE={}
        self.parser = parser

    def visit_BinaryOperator(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        return node.value
    def visit_Assign(self, node):
        #print('visit_Assign visit_Assign visit_Assign')
        var_name = node.left.value
        self.SYMBOL_TABLE[var_name] = self.visit(node.right)

    def visit_Boolean(self, node):
        #print('visit_Boolean')
        if node.op.type==EQUAL:
            return  self.visit(node.left) == self.visit(node.right)
        elif node.op.type==LT:

            return  self.visit(node.left) < self.visit(node.right)
        elif node.op.type==GT:
            return  self.visit(node.left) > self.visit(node.right)
        elif node.op.type==AND:
            #print('visit_Boolean', self.visit(node.left) and self.visit(node.right))
            if self.visit(node.left) == False:
                return False
            else:
                return  self.visit(node.left) and self.visit(node.right)
        elif node.op.type==OR:
            if self.visit(node.left) == True:
                return True
            else:
                return  self.visit(node.left) or self.visit(node.right)
        elif node.op.type==NOT:
            return not self.visit(node.right)

    def visit_While(self, node):
        truth_val = self.visit(node.left)
        
        loopCounter = 0
        while (truth_val is True) and (loopCounter <= 10000):
            self.visit(node.right)
            truth_val = self.visit(node.left)
            loopCounter += 1

    def visit_If(self, node):
        #print ('visit_If')
        truth_val = self.visit(node.left)
        
        if truth_val is True:
            #print ('visit_If','true')
            self.visit(node.right)
        else:
            #print ('visit_If','false')
            self.visit(node.wrong)

    def visit_Var(self, node):
        var_name = node.value
        val = self.SYMBOL_TABLE.get(var_name)
        if val is None:
            #print('Go here')
            # self.SYMBOL_TABLE[var_name] = 0
            return 0
        else:
            return val
    def visit_NoOp(self, node):
        pass
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)
        str = "{"
        for key, value in sorted(self.SYMBOL_TABLE.items()) :
            str = str + '{} → {}, '.format(key,value)
        if len(self.SYMBOL_TABLE)>=1:
            str = str.rstrip()[:-1] + "}"
        else:
            str = str.rstrip() + "}"
        return str
    def print_table(self):
        print(self.SYMBOL_TABLE)


def main():
    
    while True:
        try:
            try:
                text = raw_input('')
            except NameError:  # Python3
                text = input('')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
        #interpreter.print_table()


if __name__ == '__main__':
    main()