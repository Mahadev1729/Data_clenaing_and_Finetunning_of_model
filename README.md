# ML Intern Take-Home Assignment: EMI Collection Voice Agent Data Pipeline

## Project Overview

This project simulates a real-world ML engineering task for a conversational AI company building voice agents for EMI collection calls. The assignment demonstrates end-to-end ML pipeline skills including data cleaning, quality analysis, and model finetuning.

The project is structured in two parts:
- **Part A**: Data cleaning and quality analysis of messy conversation data
- **Part B**: Finetuning a small LLM on cleaned data for conversational tasks

## Architecture

```
├── part_a/                          # Data Cleaning Pipeline
│   ├── generate_dataset.py         # Synthetic data generation
│   ├── raw_conversations.jsonl     # Raw messy data
│   ├── clean_data.py              # Cleaning pipeline with visualizations
│   ├── cleaned_conversations.jsonl # Clean data
│   ├── rejected_conversations.jsonl # Rejected data
│   ├── visualizations/            # Data quality plots
│   │   ├── language_distribution.png
│   │   ├── outcome_distribution.png
│   │   ├── rejection_reasons.png
│   │   └── data_quality_metrics.png
│   ├── quality_report.py          # Quality analysis
│   └── writeup.md                 # Analysis writeup
│
├── part_b/                         # Model Finetuning
│   ├── finetune.ipynb             # Colab notebook for training
│   ├── eval.py                    # Model evaluation script
│   └── finetune_writeup.md        # Training analysis
│
├── demo.py                        # Streamlit demo app
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Dataset Description

The dataset contains simulated EMI collection call conversations with the following structure:

```json
{
 "conversation_id": "conv_001",
 "language": "hindi | hinglish | english",
 "turns": [
   {"role": "agent", "text": "..."},
   {"role": "customer", "text": "..."}
 ],
 "metadata": {
   "call_duration_seconds": 180,
   "outcome": "payment_committed | callback_scheduled | escalated | no_resolution"
 }
}
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Colab account (for Part B)

### Local Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Part A
1. Generate raw dataset:
   ```bash
   python part_a/generate_dataset.py
   ```

2. Clean the data (includes automatic visualization generation):
   ```bash
   python part_a/clean_data.py
   ```

   This will create visualization plots in `part_a/visualizations/` showing:
   - Language distribution before/after cleaning
   - Outcome distribution before/after cleaning
   - Rejection reasons breakdown
   - Data quality metrics comparison

3. Generate quality report:
   ```bash
   python part_a/quality_report.py
   ```

### Running Part B
1. Open `part_b/finetune.ipynb` in Google Colab
2. Run all cells to finetune the model
### Running the Demo
1. Install additional dependencies:
   ```bash
   pip install streamlit plotly
   ```

2. Run the demo app:
   ```bash
   streamlit run demo.py
   ```

3. Open the provided URL in your browser to interact with the demo.

The demo includes:
- Data quality visualizations
- Sample conversation browser
- Data cleaning visualization plots
- Mock model inference with evaluation

## Training Pipeline Explanation

### Data Preparation
- Raw conversations are cleaned to remove invalid entries
- Data is formatted into instruction-response pairs
- Tokenized using chat templates

### Model Configuration
- **Model**: Qwen2.5-0.5B-Instruct (0.5B parameters)
- **Technique**: LoRA with r=8, alpha=16
- **Target Modules**: q_proj, v_proj (attention layers)
- **Training**: 1 epoch, batch size 2, ~50 examples

### Evaluation Method
The model is evaluated on:
1. **Hinglish Detection**: Presence of Hinglish keywords
2. **Topic Relevance**: Response contains EMI/payment related terms
3. **Response Length**: Non-empty, under 100 tokens

## Key Features

- **Modular Design**: Separate functions for data loading, validation, cleaning
- **Defensive Programming**: Error handling, logging, input validation
- **Reproducibility**: Fixed random seeds, versioned dependencies
- **Colab Compatible**: Runs on free tier with T4 GPU
- **Professional Code**: Type hints, docstrings, clean structure

## Results Summary

- **Data Cleaning**: 86% of conversations retained after cleaning
- **Model Performance**: Evaluated on 10 prompts with heuristic metrics
- **Training Time**: ~5-10 minutes on Colab free tier

## Technologies Used

- **Data Processing**: Python, JSONL
- **ML Framework**: Transformers, PEFT, Datasets
- **Model**: Qwen2.5-0.5B-Instruct
- **Infrastructure**: Google Colab (free tier)

## Future Improvements

- Implement proper evaluation metrics (BLEU, ROUGE)
- Add hyperparameter tuning
- Expand dataset with real conversation data
- Deploy model as API endpoint
- Add monitoring and logging for production use
