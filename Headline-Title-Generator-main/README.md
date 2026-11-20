# Headline & Title Generator

A professional Streamlit application that generates exactly 10 article titles and
distinct headlines with clarity scores using a locally hosted Ollama model.

## Main Features

- Generate 10 distinct article titles and attention-grabbing headlines from an article or topic
- Evaluate each headline with a clarity score from 1 to 10
- Sort results from highest to lowest score
- Validate JSON structure, title and headline count and uniqueness, and scores
- Support Streamlit light and dark themes
- Use only local AI inference through Ollama

## Technology Stack

- Python
- Streamlit
- Ollama
- Qwen 2.5 3B
- Requests
- Pandas

## Project Structure

```text
Headline and Title Generator/
├── .venv/
├── src/
│   └── headline_generator/
│       ├── __init__.py
│       ├── ollama_service.py
│       ├── headline_generator.py
│       ├── response_parser.py
│       └── validators.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Open PowerShell in the project directory.

Create the virtual environment if one does not already exist:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ollama Setup

Verify that Ollama is installed:

```powershell
ollama --version
```

Check available models:

```powershell
ollama list
```

Download the required model:

```powershell
ollama pull qwen2.5:3b
```

Start Ollama in a separate terminal:

```powershell
ollama serve
```

Keep Ollama running while using the application.

## Run the Application

From the project root:

```powershell
streamlit run app.py
```

Open `http://localhost:8501` in a browser.

## Example JSON Output

```json
[
  {
    "title": "Artificial Intelligence in Modern Education",
    "headline": "How AI Is Transforming the Future of Education",
    "clarity_score": 10
  },
  {
    "title": "Personalized Learning Through Artificial Intelligence",
    "headline": "How AI Is Making Learning More Personal for Students",
    "clarity_score": 9
  }
]
```

## Application Workflow

1. Enter an article or topic.
2. Send a structured prompt to the local Ollama API.
3. Parse the returned JSON, including optional Markdown code fences.
4. Validate exactly 10 unique title/headline pairs and clarity scores.
5. Sort the pairs by headline clarity score in descending order.
6. Display the ranked results in a Streamlit table.
