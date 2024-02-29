# CLI tool for working with Ollama

A small python tool I put together to help me use models though ollama on my laptop. Nothing fancy.

It uses the [openai](http://www.openai.com) compatible [ollama](https://ollama.com) API.

## Use
```python3 ./llm.py -m "llama2" -p "say hello" -o "hi.txt" -v```

or 

```chmod +x llm.py && mv ./llm.py llm```

then

```./llm -m "llama2" -p "say hello" -o "hi.txt" -v```

## Args
* **-m** Specify the model to use (required)
* **-p** Prompt (required)
* **-tmp** Model temperature
* **-t** Template text file (see example)
* **-s** System message
* **-o** Text file to save the response to
* **-v** Verbose, print the response to stout
* **--help** This message
