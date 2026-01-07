import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")

    client = genai.Client(api_key=api_key)

    for i in range(10):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
                ),
            )
        
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        
        if response.function_calls:
            # 1) add model’s messages
            for variant in response.candidates:
                messages.append(variant.content)

            # 2) run function calls and add user messages with results
            function_responses = []
            for item in response.function_calls:
                print(response.function_calls)
                function_response = call_function(item, verbose=args.verbose)
                function_responses.append(function_response.parts[0])
            
            # 3) add function responses as user messages
            messages.append(types.Content(role="user", parts=function_responses))
            continue
            
        elif not response.function_calls:
            print(response.candidates[0].content.parts[0].text)
            break
             
if __name__ == "__main__":
    main()