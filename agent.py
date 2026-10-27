"""basketball სტატისტიკის აგენტი — ეტაპი 1.

გაშვება Colab-ში (Runtime -> Change runtime type -> GPU):
    !pip install -q -r requirements.txt
    !python agent.py
"""
from smolagents import ToolCallingAgent, TransformersModel

from tools import get_stat_average


MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"

INSTRUCTIONS = (
    "You are a basketball statistics assistant for one player. "
    "Answer ONLY using numbers returned by your tools. "
    "Never invent statistics. If a tool returns an ERROR or you have no tool "
    "for the question, say so honestly."
)


def build_agent() -> ToolCallingAgent:
    model = TransformersModel(model_id=MODEL_ID, device_map="auto", max_new_tokens=512)
    return ToolCallingAgent(
        tools=[get_stat_average],
        model=model,
        instructions=INSTRUCTIONS,
        max_steps=5,
    )


def main() -> None:
    agent = build_agent()
    print("აგენტი მზადაა. გასასვლელად ჩაწერე: exit")
    while True:
        question = input("\nშეკითხვა: ").strip()
        if question.lower() in {"exit", "quit", ""}:
            break
        answer = agent.run(question, reset=False)
        print(f"\nპასუხი: {answer}")


if __name__ == "__main__":
    main()
