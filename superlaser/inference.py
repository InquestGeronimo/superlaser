import os
from openai import OpenAI
from .utils.errata import RoleError, ApiKeyError


class SuperLaser:
    def __init__(self, api_key, endpoint_id, model_name, stream=False, chat=True):
        self.api_key = api_key or os.getenv("RUNPOD_API_KEY")
        if not api_key:
            raise ApiKeyError()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1",
        )
        self.model_name = model_name
        self.stream = stream
        self.chat = chat

    def __call__(self, prompt_or_user_message, role=None, sampling_params=None):
        if self.chat:
            return self._handle_chat_completion(
                prompt_or_user_message, role, sampling_params
            )
        else:
            return self._handle_non_chat_completion(
                prompt_or_user_message, sampling_params
            )

    def _handle_chat_completion(self, user_message, role=None, sampling_params=None):
        if not self.chat:
            raise RoleError()

        messages = [{"role": role or "user", "content": user_message}]
        if self.stream:
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True,
                sampling_params=sampling_params,
            )
            return response_stream
        else:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                sampling_params=sampling_params,
            )
            return response.choices[0].message.content

    def _handle_non_chat_completion(self, prompt, sampling_params=None):
        if self.stream:
            response_stream = self.client.completions.create(
                model=self.model_name,
                prompt=prompt,
                stream=True,
                sampling_params=sampling_params,
            )
            return response_stream
        else:
            response = self.client.completions.create(
                model=self.model_name, prompt=prompt, sampling_params=sampling_params
            )
            return response.choices[0].text
