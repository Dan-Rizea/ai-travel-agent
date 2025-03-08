import json


def get_input_prompt(prompt_path: str, input_filter: str, match_exact_filter: bool) -> str:
    prompt = __read_file(prompt_path)
    prompt = prompt.replace (
        "MATCH_EXACT_REQUEST_OPTION",
        "IF ANY VALUE OF THE GIVEN SCHEMAS DON'T EXACTLY MATCH THE USER'S REQUEST, RETURN THEM WITH A CORRESPONDING NULL VALUE"
        if match_exact_filter else
        ""
    )
    prompt = prompt.replace("FILTER_TO_REPLACE", input_filter)

    return prompt


def get_output_prompt(prompt_path: str, advanced_filter: str, match_exact_filter: bool) -> str:
    prompt = __read_file(prompt_path)
    prompt = prompt.replace (
        "MATCH_EXACT_REQUEST_OPTION",
        "BE AS STRICT AS POSSIBLE IN YOUR ANALYSIS"
        if match_exact_filter else
        "DON'T BE THAT STRICT IN YOUR ANALYSIS"
    )
    prompt = prompt.replace("ADVANCED_FILTER", advanced_filter)

    return prompt


def get_mock_output(file_path: str) -> json:
    content = __read_file(file_path)
    return json.loads(content)


def __read_file(file_path: str) -> str:
    file = open(file_path, "r", encoding='utf-8')
    content = file.read()
    file.close()

    return content
