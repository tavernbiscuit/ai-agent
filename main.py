import os
from dotenv import load_dotenv # type: ignore
from openai import OpenAI # type: ignore
import argparse
from prompts import system_prompt # type: ignore
from call_function import available_functions, call_function # type: ignore
import json
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key not found.")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
        ]

    generate_content(client, messages, args)

def generate_content(client, messages, args):
    for _ in range(20):

        response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )    
        if response.usage is None:
                raise RuntimeError("No usage metadata in response.")
        # if args.verbose is True:
        #     print(
        #         f"User prompt: {args.user_prompt}\n" 
        #         f"Prompt tokens: {response.usage.prompt_tokens}\n"
        #         f"Response tokens: {response.usage.completion_tokens}\n"
        #     )

        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] is None:
                    raise RuntimeError(f"Empty function response for {tool_call.function.name}")
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
                # print(f"Calling function: {tool_call.function.name}({function_args})")
        else:
            print(f"Response: {response.choices[0].message.content}")
            return

    print("Maximum number of turns reached.")
    sys.exit(1)

if __name__ == "__main__":
    main()
