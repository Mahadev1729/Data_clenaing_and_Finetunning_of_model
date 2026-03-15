import json
import os
from collections import Counter, defaultdict
from typing import List, Dict, Any


def load_conversations(file_path: str) -> List[Dict[str, Any]]:
    """Load conversations from JSONL file."""

    if not os.path.exists(file_path):
        return []

    conversations = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                conversations.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass

    return conversations


def safe_get_language(conv: Dict[str, Any]) -> str:
    return conv.get('language', 'unknown')


def safe_get_outcome(conv: Dict[str, Any]) -> str:
    meta = conv.get('metadata', {})
    return meta.get('outcome', 'unknown')


def safe_get_duration(conv: Dict[str, Any]) -> float:
    meta = conv.get('metadata', {})
    dur = meta.get('call_duration_seconds', 0)
    return dur if isinstance(dur, (int, float)) else 0


def safe_get_turns(conv: Dict[str, Any]) -> List[Dict[str, Any]]:
    turns = conv.get('turns', [])
    return turns if isinstance(turns, list) else []


def calculate_stats(conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics for conversations."""

    if not conversations:
        return {
            'count': 0,
            'language_dist': {},
            'outcome_dist': {},
            'avg_turns': 0,
            'avg_length': 0,
            'avg_duration': 0
        }

    languages = Counter(safe_get_language(conv) for conv in conversations)
    outcomes = Counter(safe_get_outcome(conv) for conv in conversations)

    total_turns = 0
    total_length = 0
    total_duration = 0

    for conv in conversations:
        turns = safe_get_turns(conv)

        total_turns += len(turns)

        for turn in turns:
            text = turn.get('text', '')
            total_length += len(text)

        total_duration += safe_get_duration(conv)

    count = len(conversations)

    avg_turns = total_turns / count if count > 0 else 0
    avg_length = total_length / total_turns if total_turns > 0 else 0
    avg_duration = total_duration / count if count > 0 else 0

    return {
        'count': count,
        'language_dist': dict(languages),
        'outcome_dist': dict(outcomes),
        'avg_turns': avg_turns,
        'avg_length': avg_length,
        'avg_duration': avg_duration
    }


def main():

    raw_convs = load_conversations('part_a/raw_conversations.jsonl')
    cleaned_convs = load_conversations('part_a/cleaned_conversations.jsonl')
    rejected_convs = load_conversations('part_a/rejected_conversations.jsonl')

    raw_stats = calculate_stats(raw_convs)
    cleaned_stats = calculate_stats(cleaned_convs)

    rejection_reasons = Counter(
        conv.get('rejection_reason', 'unknown') for conv in rejected_convs
    )

    print("=== Data Quality Report ===\n")

    print("Total Conversations:")
    print(f"  Raw: {raw_stats['count']}")
    print(f"  Cleaned: {cleaned_stats['count']}")
    print(f"  Rejected: {len(rejected_convs)}")
    print()

    print("Rejection Reasons:")
    for reason, count in rejection_reasons.items():
        print(f"  {reason}: {count}")
    print()

    print("Language Distribution:")
    print("  Raw:")
    for lang, count in raw_stats['language_dist'].items():
        print(f"    {lang}: {count}")

    print("  Cleaned:")
    for lang, count in cleaned_stats['language_dist'].items():
        print(f"    {lang}: {count}")
    print()

    print("Outcome Distribution:")
    print("  Raw:")
    for outcome, count in raw_stats['outcome_dist'].items():
        print(f"    {outcome}: {count}")

    print("  Cleaned:")
    for outcome, count in cleaned_stats['outcome_dist'].items():
        print(f"    {outcome}: {count}")
    print()

    print("Average Statistics:")
    print(
        f"  Turns per conversation: Raw={raw_stats['avg_turns']:.2f}, "
        f"Cleaned={cleaned_stats['avg_turns']:.2f}"
    )

    print(
        f"  Conversation length (chars): Raw={raw_stats['avg_length']:.2f}, "
        f"Cleaned={cleaned_stats['avg_length']:.2f}"
    )

    print(
        f"  Call duration (seconds): Raw={raw_stats['avg_duration']:.2f}, "
        f"Cleaned={cleaned_stats['avg_duration']:.2f}"
    )


if __name__ == '__main__':
    main()
