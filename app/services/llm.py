import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from sqlalchemy.orm import Session

from app.services.tools import (
    get_customer,
    get_order,
    get_refund_policy,
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


def generate_response(prompt: str, db: Session) -> str:

    tools = [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="get_order",
                    description="Get information about a customer's order.",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={
                            "order_id": types.Schema(
                                type="INTEGER",
                                description="The ID of the order.",
                            )
                        },
                        required=["order_id"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="get_customer",
                    description="Get information about a customer.",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={
                            "user_id": types.Schema(
                                type="INTEGER",
                                description="The ID of the customer.",
                            )
                        },
                        required=["user_id"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="get_refund_policy",
                    description="Get the company's refund policy.",
                ),
            ]
        )
    ]

    # First LLM call
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=tools,
        ),
    )

    # Check whether Gemini requested a tool
    if response.function_calls:

        function_call = response.function_calls[0]

        # Execute get_order
        if function_call.name == "get_order":

            order_id = function_call.args["order_id"]

            tool_result = get_order(
                order_id=order_id,
                db=db,
            )

        # Execute get_customer
        elif function_call.name == "get_customer":

            user_id = function_call.args["user_id"]

            tool_result = get_customer(
                user_id=user_id,
                db=db,
            )

        # Execute get_refund_policy
        elif function_call.name == "get_refund_policy":

            tool_result = get_refund_policy()

        else:
            tool_result = None

        # Send the tool result back to Gemini
        tool_response = types.Part.from_function_response(
            name=function_call.name,
            response={
                "result": tool_result,
            },
        )

        # Second LLM call
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                prompt,
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=[tool_response],
                ),
            ],
            config=types.GenerateContentConfig(
                tools=tools,
            ),
        )

    return response.text