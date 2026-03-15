# Part A: Data Cleaning and Quality Analysis Writeup

## Assumptions Made During Cleaning

1. **Required Fields**: Conversations must have `conversation_id`, `language`, `turns`, and `metadata` with `outcome` and `call_duration_seconds`.
2. **Valid Values**: Language must be one of 'hindi', 'hinglish', 'english'. Outcome must be one of the four specified values. Call duration must be positive.
3. **Turn Structure**: Each turn must have 'role' ('agent' or 'customer') and 'text' (string).
4. **Minimum Turns**: At least 2 turns per conversation.
5. **Garbled Text**: Detected by high proportion of non-alphanumeric characters (excluding common punctuation).

## Hardest Issue to Detect Programmatically

The hardest issue to detect is **language label mismatch**. While garbled text can be detected using character heuristics, determining if the language label matches the actual content requires language detection models or extensive keyword lists. For simplicity, this was not implemented, but in production, tools like langdetect or fasttext could be used.

## Scaling to 100k Conversations

The pipeline would scale well to 100k conversations:
- **Time Complexity**: O(n) for loading and processing, suitable for large datasets.
- **Memory**: Process in batches if needed, but JSONL allows streaming.
- **Parallelization**: Use multiprocessing for validation/cleaning.
- **Storage**: JSONL is efficient for large files.
- **Logging**: Structured logging for monitoring large-scale processing.

## Possible Improvements

1. **Advanced Language Detection**: Integrate language detection to catch mismatches.
2. **Duplicate Detection**: Check for duplicate conversations across the dataset.
3. **Text Quality**: Use NLP models to detect coherence and relevance.
4. **Metadata Validation**: More robust checks for realistic durations and outcomes.
5. **Error Recovery**: Attempt to fix more issues (e.g., infer missing outcomes from text).
6. **Performance**: Add progress bars and parallel processing for large datasets.
7. **Testing**: Unit tests for each validation function.
