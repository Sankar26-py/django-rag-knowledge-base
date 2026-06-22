import requests

class LLMService:

    URL = "http://localhost:11434/api/generate"
    MODEL = "llama3.2"
    @classmethod
    def generate_answer(cls, question, context):

        prompt = f"""
        You are an expert document assistant.

        Rules:

        1. Answer only from the supplied context.
        2. Never invent information.
        3. If information is missing, say:
        "I couldn't find that information in the uploaded documents."
        4. Answer clearly using bullet points when appropriate.

        Context:

        {context}

        Question:

        {question}
        """

        response = requests.post(
            cls.URL,
            json={
                "model": cls.MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]