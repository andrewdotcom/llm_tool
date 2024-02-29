#!/usr/bin/env python3

import argparse
from openai import OpenAI
import sys

def get_stdin_input():
    # Check if there is data available on stdin
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None

def read_file(file_path, verbose=False):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        if verbose:
            print(f"Note: No context file found at path {file_path}")

def llm(args):

    #Get stdin or file as prompt input if available
    prompt = args.p or (read_file(args.i) if args.i else None)
    context = get_stdin_input() or args.c or (read_file(args.cf) if args.cf else None)
    system = args.s or ""
    verbose = False if args.v is None else True

    if prompt is None and args.t is None:
        print("Error: You must provide a prompt or a template as minimum.")
        sys.exit()

    if prompt is None:
        if args.v:
            print("Note: No prompt was provided. Just using the template.")
        prompt = ""

    if context is None:
        if args.v:
            print("Note: No context was provided.")
        context = ""

    if system is None:
        if args.v:
            print("Note: No system prompt was provided.")
        context = ""

    # Define the prompt template
    if args.t:
        prompt_template = read_file(args.t, verbose)
    else:
        prompt_template = "[[system]][[prompt]][[context]]"

    # Fill in the template with provided values
    compiled_prompt = prompt_template.replace("[[system]]", system)
    compiled_prompt = compiled_prompt.replace("[[prompt]]", prompt)
    compiled_prompt = compiled_prompt.replace("[[context]]", context)

    if verbose:
        print("#" * 60)
        print(f"Compiled Prompt:")
        print("#" * 60)
        print(compiled_prompt)
        print("\n")
        print("#" * 60)
        print("Model Response:")
        print("#" * 60)
        print("\n")


    # Set up OpenAI API key and parameters
    client = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key='ollama', # required, but unused
    )

    response = client.chat.completions.create(
      model="llama2",
      temperature = args.tmp,
      messages=[
        {"role": "system", "content": f"{system}"},
        {"role": "user", "content": f"{compiled_prompt}"},
      ]
    )

    # Print or save the response
    if verbose:
        print(response.choices[0].message.content)

    if args.o:
        with open(args.o, "w") as file:
            file.write(response.choices[0].message.content)

if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="LLM - OpenAI Chat Completions CLI Tool")
    parser.add_argument("-m", required=True, help="Specify the model")
    parser.add_argument("-t", default=None, help="Specify the template for the prompt")
    parser.add_argument("-i", default="", help="Specify the path to a file to read as the prompt")
    parser.add_argument("-c", default="", help="Specify additional context")
    parser.add_argument("-cf", default=None, help="Specify the path to a file to read as additional context")
    parser.add_argument("-tmp", default=0.2, type=float, help="Specify the model temperature")
    parser.add_argument("-p", default="", help="Specify the prompt text")
    parser.add_argument("-s", default="", help="Specify the system message")
    parser.add_argument("-v", action="store_true", default=None, help="Print the response to stdout")
    parser.add_argument("-o", default="", help="Save the response to a text file at the provided location")

    # Parse command-line arguments
    args = parser.parse_args()

    # Execute the llm function with the provided arguments
    llm(args)

    #example use
   # python3 ./llm.py -m "llama2" -p "say hello" -o "hi.txt" -v
   # or chmod +x llm.py then
   # ./llm -m "llama2" -p "say hello" -o "hi.txt" -v
