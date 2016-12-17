import sys
import os
import argparse
import tempfile

from appdirs import AppDirs

from .parser import ParserImproved
from .ast_transformer import ASTTransformer
from .codegen import CodeGenerator


def main():
    argparser = argparse.ArgumentParser(description='Translator from extended C to normal C')
    argparser.add_argument('input', help='Input file name')
    argparser.add_argument('output', help='Output file name')
    argparser.add_argument('--preprocessor',
                           help='Specify C preprocessor executable (use {input} and {output} for substitution).'
                           ' Example: "gcc -E -o {output} {input}"')
    argparser.add_argument('--debug', action='store_true', help='Disable parser optimization')
    argparser.add_argument('--debug-dump', action='store_true', help='Dump parser information')
    argparser.add_argument('--verbose-debug', action='store_true', help='Display verbose debug messages while parsing')
    argparser.add_argument('--no-sync-lines', action='store_true', help='Disable emiting #line directives')
    args = argparser.parse_args()

    input_filename = args.input
    input_filename = os.path.abspath(input_filename)
    temp_filename = None
    if args.preprocessor:
        temp_filename = tempfile.mktemp(suffix='.c')
        retval = os.system(args.preprocessor.format(output=temp_filename, input=input_filename))
        if retval != 0:
            # Preprocessor failed
            return
        input_file = open(temp_filename, 'r')
    else:
        input_file = open(input_filename, 'r')
    input_text = input_file.read()
    input_file.close()
    if args.preprocessor:
        os.remove(temp_filename)

    parser_options = dict()
    if not args.debug:
        appname = __name__.split('.')
        if len(appname) > 1:
            del appname[-1]
        appname = '.'.join(appname)
        appdirs = AppDirs(appname=appname, appauthor='KivApple')
        cache_dir = appdirs.user_cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        parser_options['taboutputdir'] = cache_dir
        parser_options['write_tables'] = True
        parser_options['lex_optimize'] = True
        parser_options['yacc_optimize'] = True
        sys.path.insert(0, cache_dir)
    if args.debug_dump:
        parser_options['yacc_debug'] = True

    parser = ParserImproved(**parser_options)
    parse_tree = parser.parse(text=input_text, filename=input_filename, debuglevel=1 if args.verbose_debug else 0)
    fix_coords(parse_tree)
    ast_transformer = ASTTransformer()
    ast_transformer.visit(parse_tree)
    fix_extension_qualifier(parse_tree)
    fix_coords(parse_tree)
    generator = CodeGenerator(emit_line_numbers=not args.no_sync_lines)
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
