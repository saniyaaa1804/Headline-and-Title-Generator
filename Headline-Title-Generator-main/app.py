import pandas as pd
import streamlit as st

from src.headline_generator.headline_generator import build_headline_prompt
from src.headline_generator.ollama_service import (
    OllamaServiceError,
    generate_headlines,
)
from src.headline_generator.response_parser import (
    ResponseParseError,
    parse_ollama_response,
)
from src.headline_generator.validators import (
    ValidationError,
    sort_headlines,
    validate_headline_records,
)


st.set_page_config(
    page_title="Headline & Title Generator",
    page_icon="",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
    }
    .app-header {
        margin-bottom: 0.35rem;
    }
    .app-subtitle {
        color: var(--text-color);
        opacity: 0.72;
        margin-bottom: 1.5rem;
    }
    .input-card, .results-card {
        border: 1px solid var(--secondary-background-color);
        border-radius: 12px;
        padding: 1.25rem;
        background: var(--secondary-background-color);
        margin-bottom: 1.25rem;
    }
    .results-card {
        background: transparent;
    }
    div[data-testid="stTextArea"] textarea {
        min-height: 180px;
    }
    div.stButton > button {
        min-height: 44px;
        border-radius: 8px;
    }
    .footer {
        border-top: 1px solid var(--secondary-background-color);
        margin-top: 2.25rem;
        padding-top: 1rem;
        text-align: center;
        color: var(--text-color);
        opacity: 0.62;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main() -> None:
    st.markdown(
        '<h1 class="app-header">Headline &amp; Title Generator</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="app-subtitle">Create compelling headlines with '
        "AI-powered clarity evaluation.</p>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    source_text = st.text_area(
        "Article or Topic",
        placeholder="Paste your article or enter a topic to generate headline ideas...",
        height=180,
        label_visibility="visible",
    )
    character_count = len(source_text)
    st.caption(f"{character_count:,} characters")

    generate_clicked = st.button(
        "Generate 10 Headlines",
        type="primary",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if generate_clicked:
        if not source_text.strip():
            st.error("Please enter an article or topic before generating headlines.")
            return

        with st.spinner("Generating and evaluating headlines..."):
            try:
                prompt = build_headline_prompt(source_text)
                response_text = generate_headlines(prompt)
                records = parse_ollama_response(response_text)
                validated_records = validate_headline_records(records)
                sorted_records = sort_headlines(validated_records)
            except (OllamaServiceError, ResponseParseError, ValidationError) as exc:
                st.error(str(exc))
                return

        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        st.subheader("Generated Titles & Headlines")

        results = [
            {
                "Rank": rank,
                "Article Title": record["title"],
                "Headline": record["headline"],
                "Clarity Score": record["clarity_score"],
            }
            for rank, record in enumerate(sorted_records, start=1)
        ]
        results_df = pd.DataFrame(results)

        st.dataframe(
            results_df,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    width="small",
                ),
                "Article Title": st.column_config.TextColumn(
                    "Article Title",
                    width="large",
                ),
                "Headline": st.column_config.TextColumn(
                    "Headline",
                    width="large",
                ),
                "Clarity Score": st.column_config.NumberColumn(
                    "Clarity Score",
                    min_value=1,
                    max_value=10,
                    format="%d",
                    width="medium",
                ),
            },
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">'
        "Headline &amp; Title Generator | Generative AI Mini Project | Roll No. 10"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
