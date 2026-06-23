from debug_flow import generate_shareable_link, customize_shareable_link, Script

def test_generate_shareable_link():
    script = Script("print('Hello World')", "This script prints Hello World", "No documentation")
    link = generate_shareable_link(script)
    assert link == "https://example.com/debug-flow?code=print%28%27Hello+World%27%29&explanations=This+script+prints+Hello+World&documentation=No+documentation"

def test_customize_shareable_link():
    script = Script("print('Hello World')", "This script prints Hello World", "No documentation")
    custom_content = "This is custom content"
    link = customize_shareable_link(script, custom_content)
    assert link == "https://example.com/debug-flow?code=print%28%27Hello+World%27%29&explanations=This+script+prints+Hello+World&documentation=No+documentation&custom_content=This+is+custom+content"

def test_generate_shareable_link_empty_code():
    script = Script("", "This script prints Hello World", "No documentation")
    link = generate_shareable_link(script)
    assert link == "https://example.com/debug-flow?code=&explanations=This+script+prints+Hello+World&documentation=No+documentation"

def test_customize_shareable_link_empty_custom_content():
    script = Script("print('Hello World')", "This script prints Hello World", "No documentation")
    custom_content = ""
    link = customize_shareable_link(script, custom_content)
    assert link == "https://example.com/debug-flow?code=print%28%27Hello+World%27%29&explanations=This+script+prints+Hello+World&documentation=No+documentation&custom_content="
