import os
from openai import OpenAI

# Set up the OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Function to read the contents of a text file
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading {file_path}: {e}")

# Read product description and interview questions from text files
product_description_text = read_file("product_description.txt")
questions_text = read_file("questions.txt")

# Define the system prompt combining product description and interview questions
system_prompt = f"""
You are simulating an artificial persona who has been asked to provide feedback on a new product: Jack Sparrow's Chocolate YarrBar.
Below is the product description:

{product_description_text}

You will be asked the following interview questions about this product:

{questions_text}

Your role is to answer each question as if you were a customer who has tried the product. Please be detailed, honest, and ensure your responses align with the character and demographics you are assigned later.
"""

# Define the user prompt that explains how the AI should generate the responses
user_prompt = """
You will assume the role of different artificial personas who will answer the interview questions provided.
Each persona should have a unique age, gender, occupation, and background. For each question, please answer in the tone and perspective of that persona.
Try to include a diverse range of personas (e.g., young adult, middle-aged professional, retiree, student, etc.) in your responses.
Provide answers as if you genuinely experienced the product.
"""

# Function to interpret the prompt using the specified OpenAI client code
def interpret_prompt(prompt, system_prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            model="gpt-3.5-turbo",
        )
        chatgpt_reply = chat_completion.choices[0].message.content
        return chatgpt_reply
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to run 1000 interviews and save each response
def run_interviews(num_interviews=10):
    for i in range(1, num_interviews + 1):
        print(f"Generating response {i}...")
        response_text = interpret_prompt(user_prompt, system_prompt)
        
        if response_text:
            # Save the response to a text file
            with open(f"responses/response_{i}.txt", "w", encoding="utf-8") as file:
                file.write(response_text)
            print(f"Response {i} saved as response_{i}.txt")
        else:
            print(f"Failed to generate response {i}")

if __name__ == "__main__":
    run_interviews()
