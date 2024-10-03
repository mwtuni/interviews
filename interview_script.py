import os
import openai
import ollama

# Initialize OpenAI client if API key is available
api_key = os.getenv("OPENAI_API_KEY")
client = None
if api_key:
    client = openai.OpenAI(api_key=api_key)

# Function to read the contents of a text file
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading {file_path}: {e}")

# Unified function to interpret prompt using either OpenAI GPT or Ollama Llama 3.2
def generate_response(model, system_prompt, user_prompt):
    try:
        if model == "openai" and client:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            # Correct way to access the first choice's message content
            return response.choices[0].message.content

        elif model == "ollama" or not client:
            chat_completion = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            return chat_completion['message']['content']

    except Exception as e:
        print(f"An error occurred while generating response using {model}: {e}")
        return None

# Function to save the response to a file
def save_response(response_text, i, model):
    if response_text:
        try:
            with open(f"responses/response_{i}_{model}.txt", "w", encoding="utf-8") as file:
                file.write(response_text)
            print(f"Response {i} saved as response_{i}_{model}.txt")
        except Exception as e:
            print(f"An error occurred while saving response {i}: {e}")
    else:
        print(f"Failed to generate response {i}")

# Function to run interviews and save responses
def run_interviews(num_interviews=10, preferred_model="openai"):
    try:
        # Read product description and questions
        product_description_text = read_file("product_description.txt")
        questions_text = read_file("questions.txt")
    except Exception as e:
        print(f"An error occurred while reading files: {e}")
        return

    # Define the system prompt
    system_prompt = f"""
    You are simulating an artificial persona who has been asked to provide feedback on a new product: Jack Sparrow's Chocolate YarrBar.
    Below is the product description:

    {product_description_text}

    You will be asked the following interview questions about this product:

    {questions_text}

    Your role is to answer each question as if you were a customer who has tried the product. Please be detailed, honest, and ensure your responses align with the character and demographics you are assigned later.
    """

    # Define the user prompt
    user_prompt = """
    You will assume the role of different artificial personas who will answer the interview questions provided.
    Each persona should have a unique age, gender, occupation, and background. For each question, please answer in the tone and perspective of that persona.
    Try to include a diverse range of personas (e.g., young adult, middle-aged professional, retiree, student, etc.) in your responses.
    Provide answers as if you genuinely experienced the product.
    """

    # If OpenAI API key is missing, fallback to Ollama
    model_to_use = preferred_model if client else "ollama"

    for i in range(1, num_interviews + 1):
        print(f"Generating response {i} with model {model_to_use}...")
        response_text = generate_response(model_to_use, system_prompt, user_prompt)
        if response_text:
            save_response(response_text, i, model_to_use)
        else:
            print(f"Failed to generate response {i}")
        print(f"Completed response {i}")

if __name__ == "__main__":
    # Example: Run interviews with preferred model, fallback to Ollama if OpenAI key is missing
    run_interviews(num_interviews=10, preferred_model="ollama")
