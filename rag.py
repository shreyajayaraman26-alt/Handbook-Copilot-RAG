import os

from dotenv import load_dotenv
from groq import Groq

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# Load environment variables
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY not found in .env file")
    exit()


# Connect to Groq
client = Groq(api_key=api_key)


# Create the same embedding model used when building the database
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to the existing ChromaDB
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

print("Handbook database connected successfully!")
print("Groq AI connected successfully!")


# Keep asking questions
while True:

    question = input("\nAsk a question about the handbook (or type 'exit'): ")

    # Stop the program
    if question.lower() == "exit":
        print("\nGoodbye! 👋")
        break


    # Search for relevant handbook chunks
    results = vectorstore.similarity_search(
        question,
        k=4
    )


    # Combine retrieved handbook information
    context = ""

    for i, result in enumerate(results, 1):

        page_number = result.metadata.get(
            "page",
            "Unknown"
        )

        context += f"""
--- Handbook Result {i} ---
Page: {page_number}

{result.page_content}

"""


    # Create the prompt
    prompt = f"""
You are a helpful Harvard Law School handbook assistant.

Answer the user's question using ONLY the information
provided from the handbook below.

If the answer cannot be found in the handbook, clearly say:

"I couldn't find this information in the handbook."

Do not make up information.

HANDBOOK INFORMATION:
{context}

USER QUESTION:
{question}
"""


    # Ask Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You answer questions accurately using the provided handbook context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )


    # Get AI answer
    answer = response.choices[0].message.content


    # Display answer
    print("\n========== HANDBOOK AI ANSWER ==========\n")
    print(answer)


    # Display sources
    print("\n=========================================")
    print("Sources used:")

    for i, result in enumerate(results, 1):

        page_number = result.metadata.get(
            "page",
            "Unknown"
        )

        print(f"- Result {i}: Page {page_number}")


    print("\n=========================================")
    print("You can ask another question.")


print("\nProgram closed.")




