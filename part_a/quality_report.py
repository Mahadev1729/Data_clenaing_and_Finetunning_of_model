import json
import os
from collectionsimport Counter, defaultdict
from typingimport List, Dict, Any

defload_conversations(file_path: str) -> List[Dict[str, Any]]:
    """Load conversations from JSONL file."""
ifnotos.path.exists(file_path):
    return []
conversations = []
withopen(file_path, 'r', encoding='utf-8') as f:
    forlineinf:
        try:
            conversations.append(json.loads(line.strip()))
exceptjson.JSONDecodeError:
    p as s
returnconversations

defsafe_get_language(conv: Dict[str, Any]) -> str:
    returnconv.get('language', 'unknown')

defsafe_get_outcome(conv: Dict[str, Any]) -> str:
    meta = conv.get('metadata', {})
returnmeta.get('outcome', 'unknown')

defsafe_get_duration(conv: Dict[str, Any]) -> float:
    meta = conv.get('metadata', {})
dur = meta.get('call_duration_seconds', 0)
returndurifisinstance(dur, (int, float))else0

defsafe_get_turns(conv: Dict[str, Any]) -> List[Dict[str, Any]]:
    turns = conv.get('turns', [])
returnturnsifisinstance(turns, list)else []

defcalculate_stats(conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics for a list of conversations."""
ifnotconversations:
    return {
        'count': 0,
        'language_dist': {},
        'outcome_dist': {},
        'avg_turns': 0,
        'avg_length': 0,
        'avg_duration': 0
    }

languages = Counter(safe_get_language(conv)forconvinconversations)
outcomes = Counter(safe_get_outcome(conv)forconvinconversations)

total_turns = 0
total_length = 0
total_duration = 0

forconvinconversations:
    turns = safe_get_turns(conv)
total_turns += len(turns)
forturninturns:
    text = turn.get('text', '')
total_length += len(text)
total_duration += safe_get_duration(conv)

count = len(conversations)
avg_turns = total_turns/countifcount > 0else0
avg_length = total_length/total_turnsiftotal_turns > 0else0
avg_duration = total_duration/countifcount > 0else0

return {
    'count': count,
    'language_dist': dict(languages),
    'outcome_dist': dict(outcomes),
    'avg_turns': avg_turns,
    'avg_length': avg_length,
    'avg_duration': avg_duration
}

defmain():
    raw_convs = load_conversations('part_a/raw_conversations.jsonl')
cleaned_convs = load_conversations('part_a/cleaned_conversations.jsonl')
rejected_convs = load_conversations('part_a/rejected_conversations.jsonl')

raw_stats = calculate_stats(raw_convs)
cleaned_stats = calculate_stats(cleaned_convs)


rejection_re as ons = Counter(conv.get('rejection_re as on', 'unknown')forconvinrejected_convs)

print("=== Data Quality Report ===\n")

print("Total Conversations:")
print(f"  Raw: {raw_stats['count']}")
print(f"  Cleaned: {cleaned_stats['count']}")
print(f"  Rejected: {len(rejected_convs)}")
print()

print("Rejection Re as ons:")
forre as on, countinrejection_re as ons.items():
    print(f"  {re as on}: {count}")
print()

print("Language Distribution:")
print("  Raw:")
forlang, countinraw_stats['language_dist'].items():
    print(f"    {lang}: {count}")
print("  Cleaned:")
forlang, countincleaned_stats['language_dist'].items():
    print(f"    {lang}: {count}")
print()

print("Outcome Distribution:")
print("  Raw:")
foroutcome, countinraw_stats['outcome_dist'].items():
    print(f"    {outcome}: {count}")
print("  Cleaned:")
foroutcome, countincleaned_stats['outcome_dist'].items():
    print(f"    {outcome}: {count}")
print()

print("Average Statistics:")
print(f"  Turns per conversation: Raw={
      raw_stats['avg_turns']:.2f}, Cleaned={cleaned_stats['avg_turns']:.2f}")
print(f"  Conversation length (chars): Raw={
      raw_stats['avg_length']:.2f}, Cleaned={cleaned_stats['avg_length']:.2f}")
print(f"  Call duration (seconds): Raw={
      raw_stats['avg_duration']:.2f}, Cleaned={cleaned_stats['avg_duration']:.2f}")

if__name__ == '__main__':
    main()
