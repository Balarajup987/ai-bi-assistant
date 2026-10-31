
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.analytics import analyze_sales, compare_months

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"


# Give Groq access to our analytics function.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "analyze_sales",
            "description": (
                "Analyze sales data using revenue, quantity or transaction "
                "count. Supports grouping, filtering, sorting and limits."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "enum": ["revenue", "quantity", "transactions"],
                        "description": "What should be measured."
                    },
                    "group_by": {
                        "type": ["string", "null"],
                        "enum": [
                            "region", "product", "category",
                            "sales_channel", "month", None
                        ],
                        "description": "Dimension for grouping results."
                    },
                    "filters": {
                        "type": "object",
                        "properties": {
                            "region": {"type": ["string", "null"]},
                            "product": {"type": ["string", "null"]},
                            "category": {"type": ["string", "null"]},
                            "sales_channel": {"type": ["string", "null"]},
                            "month": {"type": ["string", "null"]}
                        },
                        "additionalProperties": False
                    },
                    "sort": {
                        "type": "string",
                        "enum": ["asc", "desc"]
                    },
                    "limit": {
                        "type": ["integer", "null"],
                        "description": "Maximum number of grouped results."
                    }
                },
                "required": [
                    "metric", "group_by", "filters", "sort", "limit"
                ],
                "additionalProperties": False
            }
        }
    }
]



def interpret_question(question):
    messages = [
        {
            "role": "system",
            "content": """
You are an AI Business Intelligence Assistant.

You analyze the sales database using the available analytics tool.

Instructions:
1. Understand the user's business question.
2. Call analyze_sales with the appropriate parameters.
3. Use only the returned database results.
4. Never invent sales figures.
5. Explain results in simple business language.
6. If the question is unrelated to sales data, explain that it is unsupported.
7. If the available data cannot answer the question, clearly explain the limitation.
8. You can provide recommendations, but they must be supported by the retrieved data.
9. Revenue means quantity * unit_price - discount_amount.
10. Only completed, valid transactions are included in analytics.
11. All monetary values are in Indian Rupees (INR).
12. Always use ₹ instead of $.
13. Never invent business facts or numerical values.
14. Do not claim that a specific factor caused a revenue
    increase or decrease unless the database supports it.
15. Clearly distinguish observed facts from recommendations
    and possible explanations.
16. For monthly trends, present months in chronological order.
Available dimensions:
region, product, category, sales_channel, month.

Available metrics:
revenue, quantity, transactions.

The dataset contains sales transactions, not customer satisfaction,
marketing campaign or competitor information.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # First Groq call: decide which tool to use.
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0
    )

    assistant_message = response.choices[0].message

    # If Groq decides no tool is needed.
    if not assistant_message.tool_calls:
        return {
            "question": question,
            "analysis": None,
            "explanation": assistant_message.content or
                "I cannot answer this question using the available data."
        }

    # Add the assistant's tool request to conversation.
    messages.append(
        assistant_message.model_dump(exclude_none=True)
    )

    analysis_results = []

    # Execute the requested analytics tool.
    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name

        if function_name != "analyze_sales":
            raise ValueError("Unsupported tool requested by AI")

        arguments = json.loads(tool_call.function.arguments)

        allowed_arguments = {
            "metric", "group_by", "filters", "sort", "limit"
        }

        if not isinstance(arguments, dict):
            raise ValueError("Invalid tool arguments")

        if set(arguments.keys()) != allowed_arguments:
            raise ValueError("Unexpected tool arguments")

        if not isinstance(arguments["filters"], dict):
            raise ValueError("Invalid filters")

        # Execute our predefined Python analytics function.
        result = analyze_sales(**arguments)

        analysis_results.append({
            "tool": function_name,
            "arguments": arguments,
            "result": result
        })

        # Send actual database results back to Groq.
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, default=str)
        })

    # Second Groq call: generate a natural-language explanation.
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return {
        "question": question,
        "analysis": analysis_results,
        "explanation": final_response.choices[0].message.content
    }
