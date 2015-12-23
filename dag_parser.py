import sys
import ast
import re


def pretty_print_parse_tree(node):
    indent = 0

    def pr(*args):
        for n in range(0, indent):
            sys.stdout.write('\t')
        for s in args:
            sys.stdout.write(s)
        sys.stdout.write('\n')
    t = re.split('(\(\),?|\[\],?|\(|\),?|\[|\],?|,) ?', ast.dump(node))
    while len(t) > 1:
        a, b, t = t[0], t[1], t[2:]
        if b[0] in ')]':
            if a:
                pr(a)
            indent -= 1
            pr(b)
        else:
            pr(a, b)
            if b[-1] in '([':
                indent += 1


def traverse_parse_tree(node):
    pass
