#!/usr/bin/env python3

import argparse
from openai import OpenAI
import sys

def get_stdin_input():
    # Check if there is data available on stdin
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None

def prompt_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
        sys.exit(1)

def llm(args):

    #Get stdin or file as prompt input if available
    prompt_from_stdin = get_stdin_input()
    prompt = prompt_from_stdin or args.p or (prompt_from_file(args.f) if args.f else None)

    if prompt is None:
        print("Error: No prompt was provided.")
        sys.exit(1)

    # Define the prompt template
    prompt_template = f"{args.t} [[system]] [[context]] [[prompt]]"

    # Fill in the template with provided values
    compiled_prompt = prompt_template.replace("[[system]]", args.s or "")
    compiled_prompt = compiled_prompt.replace("[[context]]", args.c or "")
    compiled_prompt = compiled_prompt.replace("[[prompt]]", prompt)

    # Set up OpenAI API key and parameters
    client = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key='ollama', # required, but unused
    )

    response = client.chat.completions.create(
      model="llama2",
      temperature = args.tmp,
      messages=[
        {"role": "system", "content": f"{args.s}"},
        {"role": "user", "content": f"{compiled_prompt}"},
      ]
    )

    # Print or save the response
    if args.v:
        print(response.choices[0].message.content)

    if args.o:
        with open(args.o, "w") as file:
            file.write(response.choices[0].message.content)

if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="LLM - OpenAI Chat Completions CLI Tool")
    parser.add_argument("-m", required=True, help="Specify the model")
    parser.add_argument("-t", default="", help="Specify the template for the prompt")
    parser.add_argument("-c", default="", help="Specify additional context")
    parser.add_argument("-tmp", default=1.0, type=float, help="Specify the model temperature")
    parser.add_argument("-p", default="", help="Specify the prompt text")
    parser.add_argument("-s", default="", help="Specify the system message")
    parser.add_argument("-v", action="store_true", help="Print the response to stdout")
    parser.add_argument("-f", help="Specify the path to a file to read as the prompt")
    parser.add_argument("-o", default="", help="Save the response to a text file at the provided location")

    # Parse command-line arguments
    args = parser.parse_args()

    # Execute the llm function with the provided arguments
    llm(args)

    #example use
   # python3 ./llm.py -m "llama2" -p "say hello" -o "hi.txt" -v
   # or chmod +x llm.py then
   # ./llm -m "llama2" -p "say hello" -o "hi.txt" -v
