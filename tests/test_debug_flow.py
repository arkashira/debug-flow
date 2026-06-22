from debug_flow import DebugFlow
import json

def test_upload_code():
    code = 'x = 5\ny = 10'
    debug_flow = DebugFlow(code)
    visual_representation = debug_flow.upload_code(code)
    assert json.loads(visual_representation) == [{'line_number': 1, 'code': 'x = 5'}, {'line_number': 2, 'code': 'y = 10'}]

def test_step_through_code():
    code = 'x = 5\ny = 10'
    debug_flow = DebugFlow(code)
    variables = debug_flow.step_through_code(1)
    assert variables == {'x': ''}

def test_generate_visual_representation():
    code = 'x = 5\ny = 10'
    debug_flow = DebugFlow(code)
    visual_representation = debug_flow.generate_visual_representation()
    assert visual_representation == 'Line 1: x = 5\nLine 2: y = 10\n'

def test_empty_code():
    code = ''
    debug_flow = DebugFlow(code)
    visual_representation = debug_flow.upload_code(code)
    assert json.loads(visual_representation) == []

def test_invalid_code():
    code = 'x ='
    try:
        DebugFlow(code)
        assert False
    except SyntaxError:
        assert True
