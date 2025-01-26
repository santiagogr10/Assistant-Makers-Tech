from backend.deepseek_client import get_client
from backend.database_reader import fetch_database_context  # Import the combined function

# Get the configured client
client = get_client()


def generate_response(user_message: str, user_id: int = None, db_name="store.db") -> dict:
    """
    Generates a response based on the user's message and the complete database context.

    Args:
        user_message (str): User's natural language query.
        user_id (int, optional): User's ID.
        db_name (str): Name of the database.

    Returns:
        dict: AI-generated response.
    """
    try:
        # Retrieve the complete context from the database
        database_context = fetch_database_context(db_name)

        # Personalize the context if a user_id is provided
        user_context = f"User ID: {user_id}\n" if user_id else "Unidentified user\n"

        # Prepare the prompt
        prompt = (
            "You are an intelligent assistant for Makers Tech. Classify products into the following categories:\n"
            "- Highly Recommended: Matches the user's history brands or categories.\n"
            "- Recommended: Indirect or complementary relationship.\n"
            "- Not Recommended: No relevant connection.\n\n"
            f"{user_context}"
            f"{database_context}\n\n"
            "User's query:\n"
            f"{user_message}\n"
        )

        # Send the prompt to the AI
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # Extract and return the response
        return {"status": "success", "response": response.choices[0].message.content.strip()}

    except Exception as e:
        return {"status": "error", "message": f"Error generating the response: {e}"}


if __name__ == "__main__":
    user_id = input("Enter your user ID (optional): ")
    user_input = input("Enter your query: ")
    user_id = int(user_id) if user_id.isdigit() else None  # Convert to int if valid
    response = generate_response(user_input, user_id)
    print("System response:")
    print(response)
