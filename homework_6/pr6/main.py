import openai
import os


def get_openai_response(prompt: str) -> str:
    """
    Send a prompt to the OpenAI API and return the response.
    """
    try:
        response = openai.Completion.create(
            model="gpt-4o-mini",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
