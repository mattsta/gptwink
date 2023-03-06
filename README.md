# GPTwink

api / library / tool shaped thing


## Usage

### As interactive console Q&A Application
```bash
pyenv install 3.11.2
pyenv local 3.11.2
poetry install
OPENAI_API_KEY=sk-{your-poopie-key} poetry run gptwink
```

Notes about interactive mode:

- First input is the "System Chat Prompt" as described in the API docs
- Each new request submits your session's entire conversation history
- Status bar shows your used/remaining tokens for this session (when it reaches 4096 you can't do anything else)
- Currently passes `mypy --strict` 🦾

TODO:

- Currently the CLI only runs one session per launch. Restart to reset your token counts.
- App / library has some half complete features for running automated and logged multi-agent sessions and chats. Features will continue to be filled out over time as necessary.
- Automated helper for sharing / formatting / annotating chat sessions kinda like https://matt.sh/ai-ground-report-66
- Add real time streaming output support
- Add better status/timing/output/logging/debug support everywhere
- Number each chat input and output result so we can delete them from the recursive result set (if agent gives a nonsense answer, we don't need to waste it in the recusion again).

