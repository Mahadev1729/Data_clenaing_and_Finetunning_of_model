import json
import logging
import os
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

plt.style.use('default')
sns.set_palette("husl")

VALID_LANGUAGES = ['hindi', 'hinglish', 'english']
VALID_OUTCOMES = ['payment_committed', 'callback_scheduled', 'escalated', 'no_resolution']


def load_conversations(file_path: str) -> List[Dict[str, Any]]:
    """Load conversations from JSONL file."""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")

    conversations = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                conv = json.loads(line.strip())
                conversations.append(conv)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON at line {line_num}: {e}")

    logger.info(f"Loaded {len(conversations)} conversations from {file_path}")

    return conversations


def validate_conversation(conv: Dict[str, Any]) -> tuple[bool, str]:
    """Validate a conversation and return (is_valid, reason)."""

    required_fields = ['conversation_id', 'language', 'turns', 'metadata']

    for field in required_fields:
        if field not in conv:
            return False, f"Missing required field: {field}"

    if not isinstance(conv['conversation_id'], str) or not conv['conversation_id'].startswith('conv_'):
        return False, "Invalid conversation_id format"

    if conv['language'] not in VALID_LANGUAGES:
        return False, f"Invalid language: {conv['language']}"

    if not isinstance(conv['turns'], list) or len(conv['turns']) < 2:
        return False, "Must have at least 2 turns"

    for turn in conv['turns']:
        if not isinstance(turn, dict) or 'role' not in turn or 'text' not in turn:
            return False, "Invalid turn structure"

        if turn['role'] not in ['agent', 'customer']:
            return False, f"Invalid role: {turn['role']}"

        if not isinstance(turn['text'], str):
            return False, "Turn text must be string"

    meta = conv['metadata']

    if not isinstance(meta, dict):
        return False, "Metadata must be dict"

    if 'outcome' not in meta or meta['outcome'] not in VALID_OUTCOMES:
        return False, f"Invalid or missing outcome: {meta.get('outcome')}"

    if 'call_duration_seconds' not in meta or \
       not isinstance(meta['call_duration_seconds'], (int, float)) or \
       meta['call_duration_seconds'] <= 0:

        return False, f"Invalid call_duration_seconds: {meta.get('call_duration_seconds')}"

    # Garbled text detection
    for turn in conv['turns']:
        text = turn['text']
        if len(text) > 0:
            special_chars = sum(1 for c in text if not c.isalnum() and c not in ' ,.!?')
            if special_chars / len(text) > 0.5:
                return False, "Garbled text detected"

    return True, ""


def clean_conversation(conv: Dict[str, Any]) -> Dict[str, Any]:
    """Clean a conversation by fixing minor issues."""

    cleaned = conv.copy()

    # Remove empty turns
    cleaned['turns'] = [turn for turn in cleaned['turns'] if turn['text'].strip()]

    # Remove duplicate consecutive turns
    turns = cleaned['turns']
    deduped = []

    for turn in turns:
        if not deduped or turn != deduped[-1]:
            deduped.append(turn)

    cleaned['turns'] = deduped

    if len(cleaned['turns']) < 2:
        pass  # validation will reject later

    return cleaned


def generate_quality_report(conversations: List[Dict[str, Any]], rejected: List[Dict[str, Any]]):
    """Generate quality report with visualizations."""

    os.makedirs('part_a/visualizations', exist_ok=True)

    # Language distribution
    languages = [conv['language'] for conv in conversations]
    lang_counts = Counter(languages)

    plt.figure(figsize=(8, 6))
    plt.bar(lang_counts.keys(), lang_counts.values())
    plt.title('Language Distribution (Cleaned Data)')
    plt.savefig('part_a/visualizations/language_distribution.png')
    plt.close()

    # Outcome distribution
    outcomes = [conv['metadata']['outcome'] for conv in conversations]
    outcome_counts = Counter(outcomes)

    plt.figure(figsize=(8, 6))
    plt.bar(outcome_counts.keys(), outcome_counts.values())
    plt.title('Outcome Distribution (Cleaned Data)')
    plt.xticks(rotation=45)
    plt.savefig('part_a/visualizations/outcome_distribution.png')
    plt.close()

    # Rejection reasons
    if rejected:
        reasons = [conv.get('rejection_reason', 'unknown') for conv in rejected]
        reason_counts = Counter(reasons)

        plt.figure(figsize=(8, 6))
        plt.bar(reason_counts.keys(), reason_counts.values())
        plt.title('Rejection Reasons')
        plt.xticks(rotation=45)
        plt.savefig('part_a/visualizations/rejection_reasons.png')
        plt.close()

    # Data quality metrics
    total = len(conversations) + len(rejected)

    cleaned_rate = len(conversations) / total if total > 0 else 0
    avg_turns = sum(len(conv['turns']) for conv in conversations) / len(conversations) if conversations else 0

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Cleaned Rate', 'Avg Turns'], [cleaned_rate, avg_turns])
    ax.set_title('Data Quality Metrics')

    plt.savefig('part_a/visualizations/data_quality_metrics.png')
    plt.close()


def main():

    raw_conversations = load_conversations('part_a/raw_conversations.jsonl')

    cleaned = []
    rejected = []

    for conv in raw_conversations:

        is_valid, reason = validate_conversation(conv)

        if is_valid:
            cleaned_conv = clean_conversation(conv)
            cleaned.append(cleaned_conv)

        else:
            conv['rejection_reason'] = reason
            rejected.append(conv)

    # Save cleaned conversations
    with open('part_a/cleaned_conversations.jsonl', 'w', encoding='utf-8') as f:
        for conv in cleaned:
            f.write(json.dumps(conv, ensure_ascii=False) + '\n')

    # Save rejected conversations
    with open('part_a/rejected_conversations.jsonl', 'w', encoding='utf-8') as f:
        for conv in rejected:
            f.write(json.dumps(conv, ensure_ascii=False) + '\n')

    # Generate report
    generate_quality_report(cleaned, rejected)

    logger.info(f"Processed {len(raw_conversations)} conversations")
    logger.info(f"Cleaned: {len(cleaned)}, Rejected: {len(rejected)}")


if __name__ == '__main__':
    main()
