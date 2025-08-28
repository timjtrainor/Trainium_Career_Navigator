import logging
from typing import Literal

from openai import OpenAI
import anthropic
import google.generativeai as genai

from .config import settings

logger = logging.getLogger(__name__)

Provider = Literal["openai", "anthropic", "gemini"]


class LLMClient:
    def __init__(self) -> None:
        self._openai = (
            OpenAI(api_key=settings.openai_api_key)
            if settings.openai_api_key
            else None
        )
        self._anthropic = (
            anthropic.Anthropic(api_key=settings.anthropic_api_key)
            if settings.anthropic_api_key
            else None
        )
        if settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)
            self._gemini = genai.GenerativeModel("gemini-pro")
        else:
            self._gemini = None

    def chat(self, provider: Provider, prompt: str) -> str:
        if provider == "openai":
            if not self._openai:
                raise RuntimeError("OpenAI key not configured")
            resp = self._openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content or ""
        if provider == "anthropic":
            if not self._anthropic:
                raise RuntimeError("Anthropic key not configured")
            resp = self._anthropic.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
        if provider == "gemini":
            if not self._gemini:
                raise RuntimeError("Google key not configured")
            resp = self._gemini.generate_content(prompt)
            return resp.text or ""
        raise ValueError(f"Unknown provider: {provider}")
