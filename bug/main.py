from sys import argv
from .parser import Parser
from .error import CompilingException

def main():
    if len(argv) <= 1:
        print("error: compiler requires an input program file")
    else:
        program_filename = argv[1]
        output_filename = program_filename.split('.')[0] + '.c'
        try:
            with open(program_filename, 'r') as infile, open(output_filename, 'w') as outfile:
                parser = Parser(infile.read())
                try:
                    ast = parser.parse()
                except CompilingException as err:
                    print(err)
                else:
                    outfile.write(ast.gen_code())
                    print("file successfully compiled")
        except FileNotFoundError:
            print(f'error: file "{program_filename}" cannot be found')

if __name__ == '__main__':
    main()
