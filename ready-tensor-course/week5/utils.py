from typing import Union
import yaml
from pathlib import Path
import os

ROOT_DIR = os.path.dirname((os.path.abspath(__file__)))

PROMPT_CONFIG_FPATH = os.path.join(ROOT_DIR, "prompt_config.yaml")

def load_yaml_config(file_path: Union[str, Path]) -> dict:
    """Loads a YAML configuration file.

    Args:
        file_path: Path to the YAML file.

    Returns:
        Parsed YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there's an error parsing YAML.
        IOError: If there's an error reading the file.
    """
    file_path = Path(file_path)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"YAML config file not found: {file_path}")

    # Read and parse the YAML file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}") from e
    except IOError as e:
        raise IOError(f"Error reading YAML file: {e}") from e

def load_joke_prompt_config(prompt_name: str):
    prompt_config = load_yaml_config(PROMPT_CONFIG_FPATH)
    joke_prompt_config = prompt_config[prompt_name]
    return joke_prompt_config



# print(load_prompt_config(PROMPT_CONFIG_FPATH))