from typing import List, Literal
from pydantic import BaseModel
from pyjokes import get_joke
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, END
from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import Image, display
from langchain_openai import ChatOpenAI
from langchain_cerebras import ChatCerebras
from utils import load_joke_prompt_config
from prompt_bulder import build_prompt_from_config
from dotenv import load_dotenv

load_dotenv()

# 1. defining the state
class Joke(BaseModel):
    text: str
    category: str

class JokeState(BaseModel):
    jokes: List[Joke] = []
    jokes_choice: Literal["n", "c", "l", "r", "q"] = "n" # next joke, change category, change language, reset, or quit
    category: str = "default"
    language: Literal["en", "de", "fr", "es"] = "en"
    quit: bool = False
    latest_joke: str = ""
    approval_status: bool = False
    retry_count: int = 0

# writer_llm = ChatCerebras(model="gpt-oss-120b")
writer_llm = ChatOpenAI(model="gpt-5-nano")
critic_llm = ChatOpenAI(model="gpt-5-nano")


# ===================
# Utilities
# ===================

def get_user_input(prompt: str) -> str:
    return input(prompt).strip().lower()

def print_joke(joke):
    """Print a joke with nice formatting."""
    print(f"\n😂 {joke}\n")
    print("=" * 60)

def print_menu_header(category: str, language: str, total_jokes: int):
    """Print a compact menu header."""
    print(f"🎭 Menu | Category: {category.replace('_', ' ').title()} | Language: {language.upper()} | Jokes: {total_jokes}")
    print("-" * 50)

def print_category_menu():
    """Print a nicely formatted category selection menu."""
    print("📂" + "=" * 58 + "📂")
    print("    CATEGORY SELECTION")
    print("=" * 60)

def print_language_menu():
    """Print a nicely formatted language selection menu."""
    print("🌍" + "=" * 58 + "🌍")
    print("    LANGUAGE SELECTION")
    print("=" * 60)

# 2. Node functions
def show_menu(state: JokeState) -> dict:
    print_menu_header(state.category, state.language, len(state.jokes))
    print("Pick an option:")
    user_input = get_user_input(
        "[n] 🎭 Next Joke  [c] 📂 Change Category  [l] 🌍 Change Language  [r] 🔄 Reset Jokes  [q] 🚪 Quit \n\nUser Input: "
    )
    while user_input not in ["n", "c", "l", "r", "q"]:
        print("❌ Invalid input. Please try again.")
        user_input = get_user_input(
            "[n] 🎭 Next Joke  [c] 📂 Change Category  [l] 🌍 Change Language  [r] 🔄 Reset Jokes  [q] 🚪 Quit\n    User Input: "
        )
    return {"jokes_choice": user_input}

# def fetch_joke(state: JokeState) -> dict:
#     try:
#         joke_text = get_joke(language=state.language, category=state.category)
#         new_joke = Joke(text=joke_text, category=state.category)
#         print_joke(new_joke)
#         return {"jokes": state.jokes + [new_joke]}
#     except Exception as e:
#         print(f"❌ Error fetching joke: {e}")
#         return {}

def writer(state: JokeState) -> dict:
    joke_prompt_config = load_joke_prompt_config('joke_assistant_prompt')
    input_question = f"Category: {state.category}"
    joke_prompt = build_prompt_from_config(joke_prompt_config, input_question )
    response = writer_llm.invoke(joke_prompt)
    # print("Writer output: ", response.content)
    return {"latest_joke": response.content}
    
def critic(state: JokeState) -> dict:
    critic_prompt_config = load_joke_prompt_config('joke_critic_prompt')
    critic_prompt = build_prompt_from_config(critic_prompt_config, f"Joke: {state.latest_joke}")
    response = critic_llm.invoke(critic_prompt).content
    # print("Critic Response: ", response)
    if response == "no" and state.retry_count < 5:
        return {"approval_status": False, "retry_count": state.retry_count + 1}
    else:
        return {"approval_status": True}

def human_approval(state: JokeState) -> dict:
    # print("The joke is: ", state.latest_joke)
    print_joke(state.latest_joke)
    human_input = get_user_input("Is this joke really funny? (y/n): ")
    if human_input == "y":
        new_joke = Joke(text=state.latest_joke, category=state.category)
        return {"jokes": state.jokes + [new_joke], "retry_count": 0, "approval_status": True, "latest_joke": ""}
    else:
        return {"approval_status": False}

def update_category(state: JokeState) -> dict:
    joke_categories = [
        "default",              # Neutral / general jokes
        "syntax_and_semantics", # Missing semicolons, confusing rules
        "language_specific",    # Python, Java, JS, etc.
        "bugs_and_debugging",   # Fixing one bug, creating two
        "compilation_runtime",  # Errors, crashes, infinite loops
        "programmer_lifestyle", # Coffee, late nights, dark mode
        "algorithms_and_math",  # Recursion, 0-based indexing
        "version_control",      # Git mishaps, merge conflicts
        "security_hacking"      # SQL injections, weak passwords
    ]
    print_category_menu()

    for i, cat in enumerate(joke_categories):
        emoji = "🎯" if cat == "default" else "💻" if "syntax" in cat or "language" in cat else "🐛" if "bug" in cat else "⚡" if "compilation" in cat else "☕" if "lifestyle" in cat else "�" if "math" in cat else "🔀" if "version" in cat else "🔒" if "security" in cat else "😄"
        print(f"    {i}. {emoji} {cat.replace('_', ' ').title()}")

    print("=" * 60)

    try:
        selection = int(get_user_input("    Enter category number: "))
        if 0 <= selection < len(joke_categories):
            selected_category = joke_categories[selection]
            print(f"    ✅ Category changed to: {selected_category.replace('_', ' ').title()}")
            return {"category": selected_category}
        else:
            print("    ❌ Invalid choice. Keeping current category.")
            return {}
    except ValueError:
        print("    ❌ Please enter a valid number. Keeping current category.")
        return {}

def update_language(state: JokeState) -> dict:
    languages = ["en", "de", "fr", "es"]
    lang_names = ["English", "German", "French", "Spanish"]
    print_language_menu()

    for i, (lang, name) in enumerate(zip(languages, lang_names)):
        emoji = "🇺🇸" if lang == "en" else "🇩🇪" if lang == "de" else "🇫🇷" if lang == "fr" else "🇪🇸"
        print(f"    {i}. {emoji} {name}")

    print("=" * 60)

    try:
        selection = int(get_user_input("    Enter language number: "))
        if 0 <= selection < len(languages):
            selected_language = languages[selection]
            print(f"    ✅ Language changed to: {lang_names[selection]}")
            return {"language": selected_language}
        else:
            print("    ❌ Invalid choice. Keeping current language.")
            return {}
    except ValueError:
        print("    ❌ Please enter a valid number. Keeping current language.")
        return {}

def reset_jokes(state: JokeState) -> dict:
    confirm = get_user_input("    Are you sure you want to reset all jokes? (y/n): ")
    if confirm == "y":
        print("    🔄 Jokes reset!")
        return {"jokes": []}
    else:
        print("    ❌ Reset cancelled.")
        return {}

def exit_bot(state: JokeState) -> dict:
    print("\n" + "🚪" + "=" * 58 + "🚪")
    print("    GOODBYE!")
    print("=" * 60)
    return {"quit": True}

# router function to decide which node to go to next
def route_choice(state: JokeState) -> str:
    if state.jokes_choice == "n":
        return "fetch_joke"
    elif state.jokes_choice == "c":
        return "update_category"
    elif state.jokes_choice == "l":
        return "update_language"
    elif state.jokes_choice == "r":
        return "reset_jokes"
    elif state.jokes_choice == "q":
        return "exit_bot"
    return "exit_bot"

def build_joke_graph() -> CompiledStateGraph:
    workflow = StateGraph(JokeState)
    
    workflow.add_node("show_menu", show_menu)
    # workflow.add_node("fetch_joke", fetch_joke)
    workflow.add_node("writer", writer)
    # workflow.add_node("critic", critic)
    workflow.add_node("human_approval", human_approval)
    # workflow.add_node("show_final_joke", show_final_joke)
    workflow.add_node("update_category", update_category)
    workflow.add_node("update_language", update_language)
    workflow.add_node("reset_jokes", reset_jokes)
    workflow.add_node("exit_bot", exit_bot)
    
    workflow.set_entry_point("show_menu")
    
    workflow.add_conditional_edges(
        "show_menu",
        route_choice,
        {
            "fetch_joke": "writer",
            "update_category": "update_category",
            "update_language": "update_language",
            "reset_jokes": "reset_jokes",
            "exit_bot": "exit_bot"
        }
    )
    # workflow.add_edge("fetch_joke", "show_menu")
    workflow.add_edge("writer", "human_approval")
    workflow.add_conditional_edges(
        "human_approval",
        lambda state: "show_menu" if state.approval_status else "writer",
        {
            "show_menu": "show_menu",
            "writer": "writer"
        }
    )
    # workflow.add_edge("show_final_joke", "show_menu")
    workflow.add_edge("update_category", "show_menu")
    workflow.add_edge("update_language", "show_menu")
    workflow.add_edge("reset_jokes", "show_menu")
    workflow.add_edge("exit_bot", END)
    
    return workflow.compile()

# def main():
#     graph = build_joke_graph()
#     # final_state = graph.invoke(JokeState(), config={"recursion_limit": 100})
#     with open("graph.png", "wb") as f:
#         f.write(graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER))

def main():
    print("\n" + "🎉" + "=" * 58 + "🎉")
    print("    WELCOME TO THE LANGGRAPH JOKE BOT!")
    print("    This example demonstrates agentic state flow")
    print("=" * 60 + "\n")

    graph = build_joke_graph()

    # print("\n📊 === MERMAID DIAGRAM ===")
    # print(graph.get_graph().draw_mermaid())

    print("\n" + "🚀" + "=" * 58 + "🚀")
    print("    STARTING JOKE BOT SESSION...")
    print("=" * 60)

    final_state = graph.invoke(JokeState(), config={"recursion_limit": 100})

    print("\n" + "🎊" + "=" * 58 + "🎊")
    print("    SESSION COMPLETE!")
    print("=" * 60)
    jokes = final_state.get('jokes', [])
    print(f"    📈 You enjoyed {len(jokes)} jokes during this session!")
    print(f"    📂 Final category: {final_state.get('category', 'unknown').replace('_', ' ').title()}")
    print(f"    🌍 Final language: {final_state.get('language', 'unknown').upper()}")
    if jokes:
        print("    🙏 Thanks for using the LangGraph Joke Bot!")
        print("    Here are your jokes:")
        for i, joke in enumerate(jokes, 1):
            print(f"    {i}. {joke.text}")
    print("=" * 60 + "\n")

    # Save graph PNG
    # with open("joke-llm-graph.png", "wb") as f:
    #     f.write(graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER))

if __name__ == "__main__":
    main()