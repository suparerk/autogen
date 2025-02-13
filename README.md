ENV:

OPENAI_API_KEY=

AZURE_OPENAI_API_KEY=

AZURE_OPENAI_ENDPOINT=

OPENAI_API_VERSION=

OLLAMA_BASE_URL=http://localhost:11434/v1


command:
pip install -U -r requirement.txt

to run autogenstudio server:
autogenstudio ui --port 8088

to run api server
agentstudio serve --team  team.json --port=8085

swagger path:
localhost:8085/docs
