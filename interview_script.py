import os
import openai
import ollama

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
def generate_response(client, model, system_prompt, user_prompt):
    try:
        if model == "openai" and client:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            return response.choices[0].message.content

        elif model == "ollama":
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

    # Initialize OpenAI client if the preferred model is OpenAI and the API key exists
    client = None
    if preferred_model == "openai" and os.getenv("OPENAI_API_KEY"):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        preferred_model = "ollama"  # fallback to Ollama if OpenAI API key is not present

    # Define the system prompt
    system_prompt = """
You are to assume the role of a **random, realistic persona**. The persona will have attributes such as age (ranging from 4 to 99), gender, occupation, and background. This persona must be realistic and should reflect everyday people, without any themes or fictional elements.
Once assigned, you must remain in character as this persona throughout the session. Your answers should reflect the experiences, thoughts, and opinions of a regular person, based on the given attributes. Stay consistent in your tone and voice, and ensure that you do not introduce any exaggerated or fictional traits.
    """

    # Define the user prompt
    user_prompt = f"""
You have recently tested a new product and partaking a survey.

Below is the product description:
{product_description_text}

Here are the questions:
{questions_text}
    """

    for i in range(1, num_interviews + 1):
        print(f"Generating response {i} with model {preferred_model}...")
        response_text = generate_response(client, preferred_model, system_prompt, user_prompt)
        if response_text:
            save_response(response_text, i, preferred_model)
        else:
            print(f"Failed to generate response {i}")
        print(f"Completed response {i}")

if __name__ == "__main__":
    # Example: Run interviews with preferred model, fallback to Ollama if OpenAI key is missing
    run_interviews(num_interviews=10, preferred_model="openai")
