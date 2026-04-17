from ai_extension.llm.ollama_client import query_llm

def generate_insights(df):

    sample = df.head(30).to_string()

    prompt = f"""
You are a senior data analyst.

Analyze the dataset and produce a HIGH-QUALITY PROFESSIONAL REPORT.

Dataset Preview:
{sample}

Columns:
{list(df.columns)}

STRICT FORMAT:

# 📊 Dataset Overview
- Rows:
- Columns:
- Key fields:

# 🔍 Key Patterns & Trends
- (Bullet insights with clear meaning)
- Focus on trends, dominance, relationships

# 📈 Important Insights
- Business-style insights
- What does this data tell?

# ⚠️ Anomalies / Outliers
- Any unusual values or behavior

# 💡 Recommendations
- Actionable suggestions

# ❓ Suggested Questions
- 3–5 smart follow-up questions user can ask

RULES:
- Use headings
- Use bullet points
- Keep it clean and readable
- No generic explanation
- Be specific to data
"""

    return query_llm(prompt)