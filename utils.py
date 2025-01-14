import os
import json

CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), ".sagy.config.json")

def get_model():
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["model"]

def get_lang():
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["lang"]

def get_proofread_prompt(selected_text: str):
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["proofread_prompt"].replace("$$TEXT$$", selected_text).replace("$$LANG$$", get_lang())

def get_summarize_prompt(selected_text: str):
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["summarize_prompt"].replace("$$TEXT$$", selected_text).replace("$$LANG$$", get_lang())

def get_continue_prompt(selected_text: str):
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["continue_prompt"].replace("$$TEXT$$", selected_text).replace("$$LANG$$", get_lang())

def get_simplify_prompt(selected_text: str):
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["simplify_prompt"].replace("$$TEXT$$", selected_text).replace("$$LANG$$", get_lang())

def get_format_prompt(selected_text: str):
    with open(CONFIG_FILE_PATH, "r") as f:
        return json.load(f)["format_prompt"].replace("$$TEXT$$", selected_text).replace("$$LANG$$", get_lang())

def check_first_launch():
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w") as f:
            json.dump({
                "proofread_prompt": "Answer in this language: '$$LANG$$'. Use proper grammar. Please proofread the following text, and ONLY return the corrected text: '$$TEXT$$'",
                "summarize_prompt": "Answer in this language: '$$LANG$$'. Use proper grammar. Please summarize the following text, and ONLY return the summary: '$$TEXT$$'",
                "continue_prompt": "Continue the previous response in this language: '$$LANG$$'. Use proper grammar. Please continue the following text, and ONLY return the full text including the Continuation: '$$TEXT$$'",
                "simplify_prompt": "Answer in this language: '$$LANG$$'. Use proper grammar. Please simplify the following text, and ONLY return the simplified text: '$$TEXT$$'",
                "format_prompt": "Answer in this language: '$$LANG$$'. Use proper grammar. Please format the following text in Markdown, and ONLY return the formatted text: '$$TEXT$$'",
            }, f, indent=4)

        return True
    else:
        return False

def save_config(config: dict) -> None:
    """Save the entire config object to file"""
    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(config, f, indent=4)

def set_model(model: str) -> None:
    """Set the model in config"""
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
        config["model"] = model
        save_config(config)
    except FileNotFoundError:
        save_config({"model": model})

def set_lang(lang: str) -> None:
    """Set the language in config"""
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
        config["lang"] = lang
        save_config(config)
    except FileNotFoundError:
        save_config({"lang": lang})

def set_proofread_prompt(prompt: str) -> None:
    """Set the proofreading prompt template"""
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
        config["proofread_prompt"] = prompt
        save_config(config)
    except FileNotFoundError:
        save_config({"proofread_prompt": prompt})

def set_summarize_prompt(prompt: str) -> None:
    """Set the summarize prompt template"""
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
        config["summarize_prompt"] = prompt
        save_config(config)
    except FileNotFoundError:
        save_config({"summarize_prompt": prompt})
