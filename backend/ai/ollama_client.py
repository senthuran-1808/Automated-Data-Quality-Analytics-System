import ollama


class OllamaClient:

    MODEL = "qwen2.5:3b"

    @staticmethod
    def ask(prompt: str):

        response = ollama.chat(

            model=OllamaClient.MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response["message"]["content"]