import json
from dataclasses import dataclass
from urllib.parse import urlencode
from argparse import ArgumentParser

@dataclass
class Script:
    code: str
    explanations: str
    documentation: str

def generate_shareable_link(script: Script) -> str:
    """Generate a shareable link for a Python script"""
    query_params = {
        "code": script.code,
        "explanations": script.explanations,
        "documentation": script.documentation
    }
    return f"https://example.com/debug-flow?{urlencode(query_params)}"

def customize_shareable_link(script: Script, custom_content: str) -> str:
    """Allow users to customize the content of the shareable link"""
    query_params = {
        "code": script.code,
        "explanations": script.explanations,
        "documentation": script.documentation,
        "custom_content": custom_content
    }
    return f"https://example.com/debug-flow?{urlencode(query_params)}"

def main():
    parser = ArgumentParser()
    parser.add_argument("--code", help="Python script code")
    parser.add_argument("--explanations", help="Explanations for the script")
    parser.add_argument("--documentation", help="Documentation for the script")
    parser.add_argument("--custom_content", help="Custom content for the shareable link")
    args = parser.parse_args()

    script = Script(args.code, args.explanations, args.documentation)
    if args.custom_content:
        link = customize_shareable_link(script, args.custom_content)
    else:
        link = generate_shareable_link(script)
    print(link)

if __name__ == "__main__":
    main()
