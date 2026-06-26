import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Breakpoint:
    line: int
    enabled: bool = True

class Debugger:
    def __init__(self, code: str):
        self.code = code.split('\n')
        self.breakpoints: List[Breakpoint] = []
        self.current_line = 0
        self.locals = {}
        self.globals = {}

    def set_breakpoint(self, line: int):
        self.breakpoints.append(Breakpoint(line))

    def move_breakpoint(self, old_line: int, new_line: int):
        for breakpoint in self.breakpoints:
            if breakpoint.line == old_line:
                breakpoint.line = new_line
                break

    def delete_breakpoint(self, line: int):
        self.breakpoints = [bp for bp in self.breakpoints if bp.line != line]

    def step_into(self):
        if self.current_line < len(self.code):
            self.current_line += 1
            if self.current_line in [bp.line for bp in self.breakpoints]:
                return self.current_line
        return None

    def step_over(self):
        """
        Execute the current line and stop at the next breakpoint *after* the current line.
        If the immediate next line is a breakpoint, skip it and stop at the following breakpoint.
        """
        if self.current_line >= len(self.code):
            return None

        # Find all breakpoint lines sorted
        bp_lines = sorted(bp.line for bp in self.breakpoints)
        # Find the first breakpoint strictly greater than current_line
        next_bp = None
        for line in bp_lines:
            if line > self.current_line:
                next_bp = line
                break

        if next_bp is None:
            # No breakpoint ahead; nothing to stop at
            return None

        # If the next breakpoint is the immediate next line, skip it
        if next_bp == self.current_line + 1:
            # Find the following breakpoint
            following_bp = None
            for line in bp_lines:
                if line > next_bp:
                    following_bp = line
                    break
            if following_bp is None:
                # No further breakpoint; step over to the end
                self.current_line = len(self.code)
                return None
            else:
                self.current_line = following_bp
                return following_bp
        else:
            # Next breakpoint is not immediate; stop there
            self.current_line = next_bp
            return next_bp

    def step_out(self):
        if self.current_line < len(self.code):
            self.current_line = len(self.code)
            return self.current_line
        return None

    def get_locals(self):
        return self.locals

    def get_globals(self):
        return self.globals

    def run(self):
        while self.current_line < len(self.code):
            if self.current_line in [bp.line for bp in self.breakpoints]:
                return self.current_line
            self.current_line += 1
        return None
