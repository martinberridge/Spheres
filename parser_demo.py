import ast
import dag_parser

test_file = '''
import dag


class Test(dag.DomainObj):
    x = 0

    @dag.DagMethod
    def bar(self, y):
        return self.foo(y)

    @dag.DagMethod
    def foo(self, y):
        return self.x + y ** 2

    def hey(self, y):
        x = external_method()
        return x.foo(y)

    def you(self, y):
        return self.hey(y)

b = 5

t = Test()

t.x = 2

print t.foo(b)
'''


def main():
    node = ast.parse(test_file)
    print '\nParse Tree:'
    dag_parser.pretty_print_parse_tree(node)
    print '\nTraversal:'
    dag_parser.traverse_parse_tree(node)
    print '\nEvaluation:'
    eval(compile(node, '-', 'exec'), globals())

if __name__ == '__main__':
    main()
