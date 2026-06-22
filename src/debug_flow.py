import ast
import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Variable:
    name: str
    value: str

@dataclass
class CodeLine:
    line_number: int
    code: str
    variables: List[Variable]

class DebugFlow:
    def __init__(self, code: str):
        self.code = code
        self.ast_tree = ast.parse(code)
        self.lines = self.parse_code()

    def parse_code(self) -> List[CodeLine]:
        lines = []
        for node in self.ast_tree.body:
            if isinstance(node, ast.Assign):
                line_number = node.lineno
                code = self.get_code_line(line_number)
                variables = self.get_variables(node)
                lines.append(CodeLine(line_number, code, variables))
        return lines

    def get_code_line(self, line_number: int) -> str:
        lines = self.code.split('\n')
        return lines[line_number - 1]

    def get_variables(self, node: ast.Assign) -> List[Variable]:
        variables = []
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable = Variable(target.id, '')
                variables.append(variable)
        return variables

    def step_through_code(self, line_number: int) -> Dict[str, str]:
        line = next((line for line in self.lines if line.line_number == line_number), None)
        if line:
            variables = {variable.name: variable.value for variable in line.variables}
            return variables
        else:
            return {}

    def upload_code(self, code: str) -> str:
        self.code = code
        self.ast_tree = ast.parse(code)
        self.lines = self.parse_code()
        return json.dumps([{'line_number': line.line_number, 'code': line.code} for line in self.lines])

    def generate_visual_representation(self) -> str:
        visual_representation = ''
        for line in self.lines:
            visual_representation += f'Line {line.line_number}: {line.code}\n'
        return visual_representation
