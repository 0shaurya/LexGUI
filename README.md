# LexGUI - Frontend for inferencing with local and API-based LLMs
LexGUI is a Qt-based LLM frontend that supports:

 - [llama.cpp](https://github.com/ggerganov/llama.cpp) (through [llama-cpp-python](https://github.com/abetlen/llama-cpp-python))
 - OpenAI API
 - MistralAI API

LexGUI's goal is to provide a simple, lightweight, and portable GUI interface that supports interacting with LLMs. Currently, LexGUI only supports Windows systems.
## Screenshot
![enter image description here](https://github.com/0shaurya/LexGUI/raw/main/screenshot.png)
## Quickstart
1. Download the release from the releases section.
2. Extract directory
3. Run `LexGUI.exe`
4. Upload a `.gguf` model, or supply your OpenAI/MistralAI API key
5. Prompt
## Building instructions
To build:
1. Download source code
2. Ensure required dependencies are installed (found in `requirements.txt`).
3. Install using a tool such as [PyInstaller](https://pyinstaller.org/) or [py2exe](https://www.py2exe.org/).
## Future Ideas
 - Implement GPU support via [ExLlamaV2](https://github.com/turboderp/exllamav2).
 - Add a chat history function.
 - Support Google's API.
 - Add a tokens/sec and context length counter.
 - Add perplexity highlighting.