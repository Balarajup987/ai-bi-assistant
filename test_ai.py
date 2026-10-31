
from app.ai_service import interpret_question

questions = [
    "Which region has the lowest revenue?",
    "How much revenue did South generate?",
    "Show the top three products by revenue.",
    "Show monthly revenue trends.",
    "What is the weather today?"
]

for question in questions:
    print("\nQuestion:", question)

    try:
        result = interpret_question(question)
        print("Analysis:", result["analysis"])
        print("AI Explanation:", result["explanation"])
    except Exception as error:
        print("Error:", error)
