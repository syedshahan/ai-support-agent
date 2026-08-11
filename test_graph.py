from app.agent.graph import graph


result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Where is my order #1?",
            }
        ]
    }
)

for message in result["messages"]:
    print("\n---")
    print(message)