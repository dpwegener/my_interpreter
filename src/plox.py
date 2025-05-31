"""
Python Interpretor based on https://craftinginterpreters.com/
"""

import sys

from ast_printer import AstPrinter
from parser import Parser
from scanner import Scanner


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


class ErrorReporter:
    had_error: bool = False

    @classmethod
    def report_error(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        ErrorReporter.had_error = True


def run_file(path: str) -> None:
    with open(path, "r") as file:
        content = file.read()
        run(content)
        if ErrorReporter.had_error:
            sys.exit(65)


def run_prompt() -> None:
    while True:
        try:
            line = input("> ")
            run(line)
            ErrorReporter.had_error = False
        except EOFError:
            break


def run(source: str) -> None:
    tokens = list(Scanner(source, error).scan_tokens())

    parser = Parser(tokens, report)
    expression = parser.parse()

    if ErrorReporter.had_error:
        return
    if expression:
        print(AstPrinter().print(expression))


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str) -> None:
    ErrorReporter.report_error(line, where, message)


if __name__ == "__main__":
    main()
