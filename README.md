# TerminalAssistantProject

A terminal-based assistant that allows you to interact with ChatGPT using your API key. This assistant can open files, URLs, and execute custom commands you teach it. It has built-in voice-to-text and text-to-voice capabilities.

![image](https://github.com/user-attachments/assets/0fa8d3fc-1b05-4dc7-a47e-0fcc035de08f)

All conversations are kept in the 'session.json' file.

---

## Features

- **ChatGPT Integration**: Communicate directly with ChatGPT via the terminal using your OpenAI API Key.
- **Command Execution**: Open files, launch URLs, and execute terminal commands easily.
- **Custom Commands**: You can easily add new commands and modify existing ones.
- **Voice-to-Text**: Speak to the assistant, and it transcribes your voice into text for processing using Whisper.
- **Text-to-Voice**: The assistant speaks as it responds.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GabrielVY/TerminalAssistantProject.git
   cd TerminalAssistantProject
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have `FFmpeg` installed for audio processing:
   - On Debian/Ubuntu:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - On macOS (via Homebrew):
     ```bash
     brew install ffmpeg
     ```
   - On Windows:
     - [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your system's PATH.

4. Set up your OpenAI API key as an environment variable:
   ```bash
   OPENAI_API_KEY='your_api_key_here'
   ```

---

## Usage

1. Launch the program:
   ```bash
   python main.py
   ```

2. Use commands to interact with the assistant:
   - **`$voice`**: Activate voice input mode.
   - **`$quit`**: Exit the program.
   - **`$debug`**: Toggle debug mode.

3. You'll certainly need to modify the absolute paths of the program.

---

## Example Interaction

```
===============================================================
                  Welcome to AI Assistant                      
                     Use $voice to talk                        
                     Use $quit  to quit                        
===============================================================

You: Open Google
Assistant: Sure, opening Google for you.
```

---

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with your enhancements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Troubleshooting

If you encounter issues:
- Ensure all dependencies are installed using `pip install -r requirements.txt`.
- Verify `FFmpeg` is properly installed and added to your system's PATH.
- Check your OpenAI API Key is valid and correctly set as an environment variable.

---

## Notes

- **Audio Support**: Ensure your microphone and speakers are configured correctly for the voice features.
- **API Costs**: Interactions with ChatGPT may incur costs depending on your OpenAI plan.
