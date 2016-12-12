import argparse
from .parser import ParserImproved
from .ast_transformer import ASTTransformer
from .codegen import CGeneratorBase


def main():
    argparser = argparse.ArgumentParser(description='Translator from extended C to normal C')
    argparser.add_argument('input', help='Input file name')
    argparser.add_argument('output', help='Output file name')
    args = argparser.parse_args()

    input_filename = args.input
    input_file = open(input_filename, 'r')
    input_text = input_file.read()
    input_file.close()

    parser = ParserImproved()
    parse_tree = parser.parse(text=input_text, filename=input_filename)
    ast_transformer = ASTTransformer()
    ast_transformer.visit(parse_tree)
    fix_coords(parse_tree)
    generator = CGeneratorBase()
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

if __name__ == '__main__':
    main()
