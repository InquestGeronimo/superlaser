from openai import OpenAI
import os


class SuperLaser:
    def __init__(self, endpoint_id, model_name):
        self.client = OpenAI(
            api_key=os.environ.get("RUNPOD_API_KEY"),
            base_url=f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1",
        )
        self.model_name = model_name

    def __call__(self, user_message):
        response_stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": user_message}],
            temperature=0,
            max_tokens=100,
            stream=True,
        )
        # Stream the response
        for response in response_stream:
            print(response.choices[0].delta.content or "", end="", flush=True)
