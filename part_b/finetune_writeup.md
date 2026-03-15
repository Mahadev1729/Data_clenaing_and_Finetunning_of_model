# Part B: Finetuning Writeup

## Why This Model Was Chosen

Qwen2.5-0.5B-Instruct was chosen because:
- Small size (0.5B parameters) fits within Colab free tier limits
- Instruction-tuned for chat applications
- Good performance on multilingual tasks including Hindi/Hinglish
- Efficient for LoRA finetuning

## LoRA Configuration Reasoning

- **r=8**: Balance between parameter efficiency and performance
- **alpha=16**: Standard scaling factor (alpha = 2*r)
- **target_modules**: ["q_proj", "v_proj"] - attention layers for conversational tasks
- **dropout=0.05**: Minimal regularization to prevent overfitting on small dataset

## What Worked Well

- Model converged quickly on the small dataset
- Generated responses were contextually relevant
- LoRA kept training efficient and memory-friendly
- Multilingual capability handled Hinglish well

## What Did Not Work

- Limited dataset size (50 examples) led to some repetitive responses
- Temperature sampling sometimes produced off-topic content
- Evaluation metrics are heuristic-based, not using proper BLEU/ROUGE
- No hyperparameter tuning due to time constraints

## Improvements for Production Systems

1. **Larger Dataset**: Use thousands of examples with diverse scenarios
2. **Better Evaluation**: Implement proper metrics like BLEU, ROUGE, and human evaluation
3. **Hyperparameter Tuning**: Grid search over LoRA parameters and training settings
4. **Data Augmentation**: Generate synthetic conversations to expand dataset
5. **Advanced Techniques**: Use DPO or RLHF for better alignment
6. **Model Selection**: Consider larger models like 1.5B or 3B for better performance
7. **Multilingual Focus**: Fine-tune specifically on Hindi/Hinglish data
8. **Safety Alignment**: Add safety instructions to prevent harmful responses
9. **Monitoring**: Implement logging and monitoring for production deployment
10. **A/B Testing**: Compare finetuned vs base model performance in real scenarios
