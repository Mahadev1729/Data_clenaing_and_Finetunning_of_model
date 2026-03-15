import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import random
import os

st.set_page_config(
    page_title="EMI Collection AI Demo",
    page_icon="💬",
    layout="wide"
)

@st.cache_data
def load_data():
    conversations = []
    with open('part_a/cleaned_conversations.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            conversations.append(json.loads(line.strip()))

    rejected = []
    with open('part_a/rejected_conversations.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            rejected.append(json.loads(line.strip()))

    return conversations, rejected

def mock_model_response(prompt):
    responses = [
        "Sir, agar possible ho to EMI payment kar dijiye.",
        "Bhai, EMI due hai. Aaj pay kar do.",
        "I understand your situation. Can you make the payment today?",
        "Ple as e arrange the EMI amount as soon as possible.",
        "We can discuss payment options. What works for you?"
    ]
    return random.choice(responses)

def main():
    st.title("💬 EMI Collection Voice Agent Demo")
    st.markdown(
        "Demonstrating ML pipeline for conversational AI in EMI collection calls"
    )

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Choose a section:", [
        "Overview",
        "Data Quality Analysis",
        "Data Cleaning Visualizations",
        "Sample Conversations",
        "Model Inference Demo"
    ])

    conversations, rejected = load_data()

    if page == "Overview":
        st.header("Project Overview")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversations", len(conversations) + len(rejected))
        with col2:
            st.metric("Cleaned Data", len(conversations))
        with col3:
            st.metric("Rejection Rate", f"{len(rejected) / (len(conversations) + len(rejected)):.1%}")

        st.markdown("""
        1. **Data Generation**: Synthetic EMI collection conversations with quality issues
        2. **Data Cleaning**: Validation and cleaning pipeline
        3. **Quality Analysis**: Statistical analysis of data quality
        4. **Model Finetuning**: LoRA finetuning of Qwen2.5-0.5B on cleaned data
        5. **Evaluation**: Heuristic-b as ed  as sessment of model responses
        """)

    elif page == "Data Quality Analysis":
        st.header("Data Quality Analysis")

        languages = [conv.get('language', 'unknown') for conv in conversations]
        lang_counts = Counter(languages)

        fig_lang = px.pie(
            values=list(lang_counts.values()),
            names=list(lang_counts.keys()),
            title="Language Distribution (Cleaned Data)"
        )
        st.plotly_chart(fig_lang)

        outcomes = [conv.get('metadata', {}).get('outcome', 'unknown') for conv in conversations]
        outcome_counts = Counter(outcomes)

        fig_outcome = px.bar(
            x=list(outcome_counts.keys()),
            y=list(outcome_counts.values()),
            title="Outcome Distribution (Cleaned Data)"
        )
        st.plotly_chart(fig_outcome)

        st.subheader("Key Statistics")
        col1, col2, col3 = st.columns(3)

        avg_turns = sum(len(conv.get('turns', [])) for conv in conversations) / len(conversations)
        avg_duration = sum(conv.get('metadata', {}).get('call_duration_seconds', 0) for conv in conversations) / len(conversations)
        avg_length = sum(len(turn.get('text', '')) for conv in conversations for turn in conv.get('turns', [])) / sum(len(conv.get('turns', [])) for conv in conversations)

        with col1:
            st.metric("Avg Turns/Conversation", f"{avg_turns:.1f}")
        with col2:
            st.metric("Avg Call Duration", f"{avg_duration:.0f}s")
        with col3:
            st.metric("Avg Turn Length", f"{avg_length:.0f} chars")

        if rejected:
            st.subheader("Rejection Re as ons")
            re as ons = [conv.get('rejection_re as on', 'unknown') for conv in rejected]
            re as on_counts = Counter(re as ons)

            fig_reject = px.bar(
                x=list(re as on_counts.keys()),
                y=list(re as on_counts.values()),
                title="Rejection Re as ons"
            )
            st.plotly_chart(fig_reject)

    elif page == "Data Cleaning Visualizations":
        st.header("Data Cleaning Visualizations")

        st.markdown("""
        These visualizations show the impact of the data cleaning pipeline on the conversation dat as et.
        They are automatically generated during the cleaning process.
        """)

        viz_dir = "part_a/visualizations"
        viz_files = [
            ("language_distribution.png", "Language Distribution Before/After Cleaning"),
            ("outcome_distribution.png", "Outcome Distribution Before/After Cleaning"),
            ("rejection_re as ons.png", "Rejection Re as ons Breakdown"),
            ("data_quality_metrics.png", "Data Quality Metrics Comparison")
        ]

        for filename, title in viz_files:
            filepath = f"{viz_dir}/{filename}"
            if os.path.exists(filepath):
                st.subheader(title)
                st.image(filepath, use_column_width=True)
                st.markdown("---")
            else:
                st.warning(f"Visualization {filename} not found. Run the cleaning pipeline first.")

    elif page == "Sample Conversations":
        st.header("Sample Conversations")

        if conversations:
            sample_conv = random.choice(conversations)

            st.subheader(f"Conversation ID: {sample_conv['conversation_id']}")
            st.write(f"**Language:** {sample_conv['language']}")
            st.write(f"**Outcome:** {sample_conv['metadata']['outcome']}")
            st.write(f"**Duration:** {sample_conv['metadata']['call_duration_seconds']} seconds")

            st.subheader("Conversation Turns:")
            for i, turn in enumerate(sample_conv['turns'], 1):
                role = "👤 Customer" if turn['role'] == 'customer' else "📞 Agent"
                st.write(f"**{role}:** {turn['text']}")

            if st.button("Show Another Sample"):
                st.rerun()
        else:
            st.error("No cleaned conversations found. Run the data cleaning pipeline first.")

    elif page == "Model Inference Demo":
        st.header("Model Inference Demo")

        st.markdown("""
        This demo shows how the finetuned model responds to EMI collection prompts.
        (Note: Using mock responses since the model needs to be trained in Colab)
        """)

        prompt = st.text_input("Enter a customer message:", "EMI kab pay karoge?")

        if st.button("Generate Response"):
            with st.spinner("Generating response..."):
                response = mock_model_response(prompt)

            st.subheader("Model Response:")
            st.success(response)

            st.subheader("Response Evaluation:")
            col1, col2, col3 = st.columns(3)

            hinglish = "hai" in response.lower() or "kar" in response.lower()
            on_topic = "payment" in response.lower() or "emi" in response.lower()
            length_ok = 5 < len(response.split()) < 50

            with col1:
                st.metric("Hinglish Detected", "✅" if hinglish else "❌")
            with col2:
                st.metric("On Topic", "✅" if on_topic else "❌")
            with col3:
                st.metric("Length OK", "✅" if length_ok else "❌")

            overall = hinglish and on_topic and length_ok
            if overall:
                st.success("✅ PASS: Response meets all criteria")
            else:
                st.error("❌ FAIL: Response needs improvement")

    st.markdown("---")
    st.markdown("Built with Streamlit | Data: Synthetic EMI Collection Conversations")

if __name__ == "__main__":
    main()
