import json
import random
import string

LANGUAGES = ['hindi', 'hinglish', 'english']

OUTCOMES = [
    'payment_committed',
    'callback_scheduled',
    'escalated',
    'no_resolution'
]

SAMPLE_DIALOGUES = {
    'hindi': {
        'agent': [
            "नमस्ते, मैं EMI कलेक्शन एजेंट बोल रहा हूं। क्या आप अपना EMI पेमेंट कर सकते हैं?",
            "सर, आपका EMI ड्यू है। कृपया आज पेमेंट करें।",
            "मैं आपकी मदद करना चाहता हूं। क्या आप पेमेंट कर सकते हैं?"
        ],
        'customer': [
            "हां, मैं आज पेमेंट कर दूंगा।",
            "मैं कल पेमेंट करूंगा।",
            "मैं अभी पेमेंट नहीं कर सकता।"
        ]
    },
    'hinglish': {
        'agent': [
            "Hello sir, EMI ka payment karoge?",
            "Bhai, EMI due hai. Aaj pay kar do.",
            "Sir, agar possible ho to payment kar dijiye."
        ],
        'customer': [
            "Haan, aaj kar dunga.",
            "Kal karunga.",
            "Abhi nahi kar sakta."
        ]
    },
    'english': {
        'agent': [
            "Hello sir, this is EMI collection agent. Can you make the payment?",
            "Sir, your EMI is due. Please pay today.",
            "I want to help you. Can you make the payment?"
        ],
        'customer': [
            "Yes, I will pay today.",
            "I will pay tomorrow.",
            "I cannot pay right now."
        ]
    }
}


def generate_conversation(conversation_id):
    language = random.choice(LANGUAGES)
    outcome = random.choice(OUTCOMES)

    num_turns = random.randint(2, 5)
    turns = []

    for i in range(num_turns):
        role = 'agent' if i % 2 == 0 else 'customer'
        text = random.choice(SAMPLE_DIALOGUES[language][role])
        turns.append({'role': role, 'text': text})

    call_duration = random.randint(60, 600)

    metadata = {
        'call_duration_seconds': call_duration,
        'outcome': outcome
    }

    conversation = {
        'conversation_id': conversation_id,
        'language': language,
        'turns': turns,
        'metadata': metadata
    }

    # Inject random issues
    if random.random() < 0.35:
        issue_type = random.choice([
            'empty_turn',
            'duplicate_turn',
            'few_turns',
            'missing_metadata',
            'null_outcome',
            'negative_duration',
            'language_mismatch',
            'garbled_text'
        ])

        if issue_type == 'empty_turn':
            idx = random.randint(0, len(turns) - 1)
            turns[idx]['text'] = ''

        elif issue_type == 'duplicate_turn':
            if len(turns) > 1:
                turns.append(turns[-1].copy())

        elif issue_type == 'few_turns':
            turns = turns[:1]

        elif issue_type == 'missing_metadata':
            del metadata[random.choice(list(metadata.keys()))]

        elif issue_type == 'null_outcome':
            metadata['outcome'] = None

        elif issue_type == 'negative_duration':
            metadata['call_duration_seconds'] = -abs(call_duration)

        elif issue_type == 'language_mismatch':
            wrong_lang = random.choice([l for l in LANGUAGES if l != language])
            conversation['language'] = wrong_lang

        elif issue_type == 'garbled_text':
            idx = random.randint(0, len(turns) - 1)
            turns[idx]['text'] = ''.join(
                random.choices(string.ascii_letters + string.digits, k=20)
            )

    return conversation


def main():
    conversations = []

    for i in range(1, 101):
        conv_id = f"conv_{i:03d}"
        conv = generate_conversation(conv_id)
        conversations.append(conv)

    with open('part_a/raw_conversations.jsonl', 'w', encoding='utf-8') as f:
        for conv in conversations:
            f.write(json.dumps(conv, ensure_ascii=False) + '\n')

    print("Generated 100 raw conversations in part_a/raw_conversations.jsonl")


if __name__ == '__main__':
    main()
