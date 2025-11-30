from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load model
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def rewrite_text(text: str) -> str:
    prompt = f"Rewrite this in a human, natural, unique way:\n{text}"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=150)

    return tokenizer.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    user = input("Enter text to rewrite: ")
    print("\nRewritten:\n", rewrite_text(user))
