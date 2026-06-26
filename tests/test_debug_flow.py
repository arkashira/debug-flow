from debug_flow import Debugger, Breakpoint

def test_set_breakpoint():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    assert len(debugger.breakpoints) == 1
    assert debugger.breakpoints[0].line == 1

def test_move_breakpoint():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    debugger.move_breakpoint(1, 2)
    assert len(debugger.breakpoints) == 1
    assert debugger.breakpoints[0].line == 2

def test_delete_breakpoint():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    debugger.delete_breakpoint(1)
    assert len(debugger.breakpoints) == 0

def test_step_into():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    assert debugger.step_into() == 1

def test_step_over():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    debugger.set_breakpoint(2)
    assert debugger.step_over() == 2

def test_step_out():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    assert debugger.step_out() == 3

def test_get_locals():
    debugger = Debugger("line1\nline2\nline3")
    debugger.locals = {"var": "value"}
    assert debugger.get_locals() == {"var": "value"}

def test_get_globals():
    debugger = Debugger("line1\nline2\nline3")
    debugger.globals = {"var": "value"}
    assert debugger.get_globals() == {"var": "value"}

def test_run():
    debugger = Debugger("line1\nline2\nline3")
    debugger.set_breakpoint(1)
    assert debugger.run() == 1
