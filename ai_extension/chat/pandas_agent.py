from ai_extension.llm.ollama_client import query_llm

def ask_question(df, question):

    sample = df.head(30).to_string()

    prompt = f"""
You are a professional data analyst.

Dataset Preview:
{sample}

Columns:
{list(df.columns)}

Question:
{question}

STRICT FORMAT:

## ✅ Answer
(1-2 line direct answer)

## 📊 Explanation
- Point 1
- Point 2
- Point 3

## 🔍 Key Insights
- Insight 1
- Insight 2
- Insight 3

## ❓ Follow-up Questions
- Question 1
- Question 2
- Question 3

IMPORTANT RULES:
- ALWAYS put a newline after headings
- NEVER write heading + text in same line
- Use clean spacing
- Use bullet points
"""

    return query_llm(prompt)