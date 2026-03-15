import streamlit as st
import json
import plotly.express as px
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
    rejected = []

    if os.path.exists('part_a/cleaned_conversations.jsonl'):
        with open('part_a/cleaned_conversations.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                conversations.append(json.loads(line.strip()))

    if os.path.exists('part_a/rejected_conversations.jsonl'):
        with open('part_a/rejected_conversations.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                rejected.append(json.loads(line.strip()))

    return conversations, rejected


def mock_model_response(prompt):

    responses = [
        "Sir, agar possible ho to EMI payment kar dijiye.",
        "Bhai, EMI due hai. Aaj pay kar do.",
        "I understand your situation. Can you make the payment today?",
        "Please arrange the EMI amount as soon as possible.",
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

    # ==========================
    # Overview
    # ==========================
    if page == "Overview":

        st.header("Project Overview")

        total = len(conversations) + len(rejected)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Conversations", total)

        with col2:
            st.metric("Cleaned Data", len(conversations))

        with col3:
            rate = len(rejected)/total if total else 0
            st.metric("Rejection Rate", f"{rate:.1%}")

        st.markdown("""
        1. **Data Generation**: Synthetic EMI collection conversations with quality issues  
        2. **Data Cleaning**: Validation and cleaning pipeline  
        3. **Quality Analysis**: Statistical analysis of data quality  
        4. **Model Finetuning**: LoRA finetuning of Qwen2.5-0.5B on cleaned data  
        5. **Evaluation**: Heuristic-based assessment of model responses  
        """)

    # ==========================
    # Data Quality Analysis
    # ==========================
    elif page == "Data Quality Analysis":

        st.header("Data Quality Analysis")

        languages = [conv.get('language', 'unknown') for conv in conversations]
        lang_counts = Counter(languages)

        fig_lang = px.pie(
            values=list(lang_counts.values()),
            names=list(lang_counts.keys()),
            title="Language Distribution"
        )

        st.plotly_chart(fig_lang)

        outcomes = [
            conv.get('metadata', {}).get('outcome', 'unknown')
            for conv in conversations
        ]

        outcome_counts = Counter(outcomes)

        fig_outcome = px.bar(
            x=list(outcome_counts.keys()),
            y=list(outcome_counts.values()),
            title="Outcome Distribution"
        )

        st.plotly_chart(fig_outcome)

        st.subheader("Key Statistics")

        col1, col2, col3 = st.columns(3)

        if conversations:

            avg_turns = sum(len(conv.get('turns', [])) for conv in conversations) / len(conversations)

            avg_duration = sum(
                conv.get('metadata', {}).get('call_duration_seconds', 0)
                for conv in conversations
            ) / len(conversations)

            total_turns = sum(len(conv.get('turns', [])) for conv in conversations)

            avg_length = sum(
                len(turn.get('text', ''))
                for conv in conversations
                for turn in conv.get('turns', [])
            ) / total_turns if total_turns else 0

        else:
            avg_turns = avg_duration = avg_length = 0

        with col1:
            st.metric("Avg Turns/Conversation", f"{avg_turns:.1f}")

        with col2:
            st.metric("Avg Call Duration", f"{avg_duration:.0f}s")

        with col3:
            st.metric("Avg Turn Length", f"{avg_length:.0f} chars")

        # Rejection reasons
        if rejected:

            st.subheader("Rejection Reasons")

            reasons = [conv.get('rejection_reason', 'unknown') for conv in rejected]

            reason_counts = Counter(reasons)

            fig_reject = px.bar(
                x=list(reason_counts.keys()),
                y=list(reason_counts.values()),
                title="Rejection Reasons"
            )

            st.plotly_chart(fig_reject)

    # ==========================
    # Visualizations
    # ==========================
    elif page == "Data Cleaning Visualizations":

        st.header("Data Cleaning Visualizations")

        st.markdown("""
        These visualizations show the impact of the data cleaning pipeline
        on the conversation dataset.
        """)

        viz_dir = "part_a/visualizations"

        viz_files = [
            ("language_distribution.png", "Language Distribution"),
            ("outcome_distribution.png", "Outcome Distribution"),
            ("rejection_reasons.png", "Rejection Reasons"),
            ("data_quality_metrics.png", "Data Quality Metrics")
        ]

        for filename, title in viz_files:

            path = f"{viz_dir}/{filename}"

            if os.path.exists(path):

                st.subheader(title)

                st.image(path, use_column_width=True)

                st.markdown("---")

            else:

                st.warning(f"{filename} not found. Run cleaning pipeline.")

    # ==========================
    # Sample Conversations
    # ==========================
    elif page == "Sample Conversations":

        st.header("Sample Conversations")

        if conversations:

            sample = random.choice(conversations)

            st.subheader(f"Conversation ID: {sample['conversation_id']}")

            st.write(f"Language: {sample['language']}")
            st.write(f"Outcome: {sample['metadata']['outcome']}")
            st.write(f"Duration: {sample['metadata']['call_duration_seconds']} seconds")

            st.subheader("Conversation Turns")

            for turn in sample['turns']:

                role = "👤 Customer" if turn['role'] == 'customer' else "📞 Agent"

                st.write(f"**{role}:** {turn['text']}")

            if st.button("Show Another Sample"):
                st.rerun()

        else:
            st.error("No cleaned conversations found.")

    # ==========================
    # Model Demo
    # ==========================
    elif page == "Model Inference Demo":

        st.header("Model Inference Demo")

        prompt = st.text_input(
            "Enter a customer message:",
            "EMI kab pay karoge?"
        )

        if st.button("Generate Response"):

            with st.spinner("Generating response..."):

                response = mock_model_response(prompt)

            st.subheader("Model Response")

            st.success(response)

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

            if hinglish and on_topic and length_ok:
                st.success("✅ PASS")
            else:
                st.error("❌ FAIL")

    st.markdown("---")
    st.markdown("Built with Streamlit | Synthetic EMI Collection Dataset")


if __name__ == "__main__":
    main()
