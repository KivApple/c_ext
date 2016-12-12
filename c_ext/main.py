import os
import argparse
import tempfile
from .parser import ParserImproved
from .ast_transformer import ASTTransformer
from .codegen import CodeGenerator


def main():
    argparser = argparse.ArgumentParser(description='Translator from extended C to normal C')
    argparser.add_argument('input', help='Input file name')
    argparser.add_argument('output', help='Output file name')
    argparser.add_argument('--preprocessor', help='Specify C preprocessor executable')
    args = argparser.parse_args()

    input_filename = args.input
    if args.preprocessor:
        temp_filename = tempfile.mktemp(suffix='.c')
        os.system(args.preprocessor % (temp_filename, input_filename))
        input_file = open(temp_filename, 'r')
    else:
        input_file = open(input_filename, 'r')
    input_text = input_file.read()
    input_file.close()
    if args.preprocessor:
        os.remove(temp_filename)

    parser = ParserImproved()
    parse_tree = parser.parse(text=input_text, filename=input_filename)
    fix_coords(parse_tree)
    ast_transformer = ASTTransformer()
    ast_transformer.visit(parse_tree)
    fix_extension_qualifier(parse_tree)
    fix_coords(parse_tree)
    generator = CodeGenerator()
    result = generator.visit(parse_tree)

    output_filename = args.output
    output_file = open(output_filename, 'w')
    output_file.write(result)
    output_file.close()


def fix_coords(node, parent_coord=None):
    if node.coord is None:
        node.coord = parent_coord
    for c_name, c in node.children():
        fix_coords(c, node.coord)
        if ((node.coord is None) or (node.coord.line == 0)) and (c.coord is not None) and (c.coord != 0):
            node.coord = c.coord


def fix_extension_qualifier(node):
    if hasattr(node, 'storage') and hasattr(node, 'quals'):
        if '__extension__' in node.quals:
            node.quals.remove('__extension__')
            node.storage.insert(0, '__extension__')
    for c_name, c in node.children():
        fix_extension_qualifier(c)

if __name__ == '__main__':
    main()
