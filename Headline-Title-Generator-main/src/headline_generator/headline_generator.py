def build_headline_prompt(source_text: str) -> str:
    source_text = source_text.strip()
    return f"""Generate exactly 10 article title and headline pairs for the article or topic below.

Requirements:
- For each result, write a clear, descriptive, professional article title suitable as the actual title of an article.
- For each result, write a separate engaging, attention-grabbing headline that attracts readers while remaining accurate and relevant.
- Make each title and its headline meaningfully different; do not copy the title or make only a minor wording change.
- Ensure all 10 titles are unique and all 10 headlines are unique.
- Use only facts present in the supplied content.
- Do not invent facts or unsupported claims.
- Avoid misleading or unsupported clickbait.
- Make every title and headline grammatically correct and distinct.
- Evaluate each headline's clarity from 1 to 10.
- Consider ease of understanding, clarity of the main message, specificity, relevance, and simplicity.
- Return valid JSON only, with no Markdown fences, explanations, or extra fields.
- The JSON must be a list containing exactly 10 objects.
- Every object must have exactly these three fields:
  - "title": a non-empty article title string
  - "headline": a non-empty string
  - "clarity_score": an integer from 1 to 10

Use this exact JSON shape:
[
  {{"title": "Artificial Intelligence in Modern Education", "headline": "How AI Is Transforming the Future of Education", "clarity_score": 10}},
  {{"title": "Personalized Learning Through Artificial Intelligence", "headline": "How AI Is Making Learning More Personal for Students", "clarity_score": 9}}
]

Article or topic:
<SOURCE_TEXT>
{source_text}
</SOURCE_TEXT>
"""
