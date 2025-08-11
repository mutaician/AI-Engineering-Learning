from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from prompt_builder import build_prompt_from_config, print_prompt_preview
import yaml

with open("config/prompt_config.yaml") as f:
    all_configs = yaml.safe_load(f)

with open("config/config.yaml") as f:
    app_config = yaml.safe_load(f)

with open("data/publication.md", "r") as f:
    publication_content = f.read()
    



def main(prompt_config_key):
    prompt_config = all_configs[prompt_config_key]
    prompt = build_prompt_from_config(prompt_config, publication_content, app_config)

    with open(f"outputs/{prompt_cfg_key}_prompt.md", "w") as f:
        f.write(prompt)

    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])

    print("=" * 40, "\nLLM OUTPUT\n", "=" * 40)
    print(response.content)

    with open(f"outputs/{prompt_cfg_key}_llm_response.md", "w") as f:
        f.write(str(response.content))


if __name__ == "__main__":
    prompt_cfg_key = "summarization_prompt_cfg6"
    main(prompt_cfg_key)
