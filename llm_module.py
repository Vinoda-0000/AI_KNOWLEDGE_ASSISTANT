from transformers import pipeline, set_seed

# Initialize the model only once for efficiency
_generator = None

def get_generator():
    global _generator
    if _generator is None:
        _generator = pipeline("text-generation", model="distilgpt2")
        set_seed(42)  # Optional: makes output more consistent
    return _generator

def generate_response(context, query, max_length=200, temperature=0.7):
    """
    Generates an AI response based on context and query.
    temperature: lower value → more deterministic answers
    """
    generator = get_generator()
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    
    output = generator(
        prompt, 
        max_length=max_length, 
        num_return_sequences=1, 
        temperature=temperature
    )
    
    generated_text = output[0]['generated_text']
    answer = generated_text.replace(prompt, "").strip()
    
    return answer

