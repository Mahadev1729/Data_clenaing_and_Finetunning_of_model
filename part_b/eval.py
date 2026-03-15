import json
import torch
from transformersimport AutoTokenizer, AutoModelForCausalLM
from peftimport PeftModel
import re


HINGLISH_KEYWORDS = ["hai", "kar", "payment", "emi",
                     "aaj", "kal", "bhai", "sir", "ho", "nahi"]


TOPIC_KEYWORDS = ["payment", "emi", "installment",
                  "due", "pay", "kar", "aaj", "kal"]

defis_hinglish(text):
    """Simple heuristic for Hinglish detection."""
text_lower = text.lower()
returnany(keywordintext_lowerforkeywordinHINGLISH_KEYWORDS)

defis_on_topic(text):
    """Check if response is on topic."""
text_lower = text.lower()
returnany(keywordintext_lowerforkeywordinTOPIC_KEYWORDS)

defis_length_ok(text, max_tokens=100):
    """Check if response length is OK."""

tokens = re.findall(r'\w+|[^\w\s]', text)
return0 < len(tokens) < max_tokens

defgenerate_response(model, tokenizer, prompt):
    """Generate response using the model."""
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
withtorch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
returnresponse[len(prompt):].strip()

defmain():

    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
b as e_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_8bit=True
)

try:
    model = PeftModel.from_pretrained(b as e_model, "./part_b/lora_adapter")
except:
    print("Adapter not found, using b as e model")
model = b as e_model

iftokenizer.pad_tokenisNone:
    tokenizer.pad_token = tokenizer.eos_token


prompts = [
    "EMI kab pay karoge?",
    "Sir, your EMI is due. Can you pay today?",
    "Bhai, payment kar do.",
    "When will you pay the EMI?",
    "EMI ka status batao.",
    "I can't pay right now.",
    "Aaj payment karunga.",
    "EMI due date kya hai?",
    "Ple as e make the payment.",
    "Kal kar dunga."
]

print("Prompt | Hinglish | On Topic | Length OK | PASS/FAIL")
print("-"*60)

p as s_count = 0
forpromptinprompts:
    response = generate_response(model, tokenizer, prompt)
hinglish = is_hinglish(response)
on_topic = is_on_topic(response)
length_ok = is_length_ok(response)
p as sed = hinglishandon_topicandlength_ok
ifp as sed:
    p as s_count += 1

print(f"{prompt[:20]:<20} | {str(hinglish):<8} | {str(on_topic):<8} | {str(length_ok):<9} | {'PASS'ifp as sedelse'FAIL'}")

print(f"\nOverall: {p as s_count}/{len(prompts)} p as sed")

if__name__ == '__main__':
    main()
