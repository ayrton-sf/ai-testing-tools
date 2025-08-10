# 🤖 AI Eval Toolkit

A modular and extensible toolkit to **evaluate LLM outputs** using various metrics including **criteria-based evaluation**, **factual claim checking**, and **semantic similarity**, with support for multiple data backends like **web search**, **ChromaDB**, and **SQL databases**.

> ⚠️ **WIP:** This toolkit is a work in progress. APIs, behaviors, and outputs are subject to change.

---

## 🚀 Quickstart

```python
from metrics import Metrics

# 🔧 Initialize the Metrics class
metrics = Metrics(model="gpt-4o", api_key="my_api_key")
```

---

## ✅ Criteria Evaluation

Use custom criteria to judge if the response meets expectations.

```python
models = ["GPT-4o","Claude 3","Gemini 1.5"]
assistant_response = """
# The impact of LLMs
Large Language Models (LLMs) such as GPT-4, Claude 3, and Gemini 1.5 are transforming the way we interact with technology.

## Capabilities of LLMs
These models understand and generate human-like text, supporting tasks from summarization to code generation.

## Popular LLMs in 2025
Current leading models include GPT-4o by OpenAI, Claude 3 by Anthropic, and Gemini 1.5 by Google DeepMind.
"""

satisfied_criteria_score = metrics.criteria_eval(
    criteria=[
        "The content should talk about LLMs",
        f"The response should mention the following models: {models_list}",
        "The content should have one title and two subtitles"
    ]
)
```

---

## 🧠 Similarity Scoring

Compute semantic similarity between a reference and a candidate response.

```python
similarity_score = metrics.similarity(
    reference=ideal_response,
    candidate=actual_response
)
```

> Supports both **Voyage AI** and **OpenAI embeddings** out of the box.

---

## 🔍 Claim Checking

Verify factual consistency using various data sources.

### 🧠 With ChromaDB

```python
from metrics import DataSource

groundness_score = metrics.claim_check(
    content=assistant_response,
    query=user_query,
    source=DataSource.CHROMA_DB
)
```

### 🌐 With Web URLs

```python
from metrics import DataSource

generated_content = """2025 has cemented the 'anything-goes' era of AI, with over $300 billion poured into rapid LLM development by tech giants and governments alike.
GPT-4o emerged as the de facto standard on April 30, 2025, replacing GPT-4 and bringing native multimodal (text, image, audio) capabilities to mainstream chat interfaces."""

groundness_score = metrics.claim_check(
    content=generated_content,
    source=DataSource.WEB,
    urls=[
        "https://www.techinsights.org/reports/ai-trends-2025",
        "https://www.datasciencehub.com/articles/global-llm-developments",
        "https://www.researchbriefs.net/analysis/ai-evaluation-metrics"
    ]
)
```

### 🗄️ With SQL Databases

```python
from metrics import DataSource

groundness_score = metrics.claim_check(
    content=assistant_response,
    source=DataSource.SQL
    db_url="postgresql://postgres:password@address:1234/your_db"
)
```

> ⚠️ **Note:** When using `DataSource.SQL`, the tool engages an **agentic loop** which leverages **MCP (Model Context Protocol)**.  
> MCP enables a **retrieval subagent** to:
> - Fetch table lists 🗂️  
> - Select relevant tables 📊  
> - Craft and run SQL queries dynamically 🔎  
> ✅ Default implementation uses **PostgreSQL** as the backend.

---

## 📦 Supported Data Sources

- `DataSource.CHROMA_DB` – for vector database retrieval  
- `DataSource.WEB` – for web-grounded evaluation  
- `DataSource.SQL` – for structured data validation (via MCP, PostgreSQL default)
