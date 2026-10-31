from pathlib import Path
from uuid import uuid4
import base64, shutil
import httpx
from app.core.config import settings

class MockDesignGenerator:
    def generate(self, source_path: Path, room: str, style: str, prompt: str | None = None) -> Path:
        Path(settings.generated_dir).mkdir(parents=True, exist_ok=True)
        output = Path(settings.generated_dir) / f"{uuid4()}{source_path.suffix.lower()}"
        shutil.copy2(source_path, output)
        return output

class GeminiGenerator:
    def generate(self, source_path: Path, room: str, style: str, prompt: str | None = None) -> Path:
        instruction = (
            f"Redesign this exact {room} as a photorealistic interior in {style} style. "
            "Preserve the room architecture, camera perspective and major openings. "
            "Improve furniture, materials, lighting, styling and spatial harmony. "
            + (prompt or "")
        )
        url = f"{settings.ai_base_url.rstrip('/')}/models/{settings.ai_model}:generateContent"
        body = {
            "contents": [{
                "parts": [
                    {"text": instruction},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(source_path.read_bytes()).decode()}}
                ]
            }]
        }
        r = httpx.post(url, params={"key": settings.ai_api_key}, json=body, timeout=180)
        r.raise_for_status()
        data = r.json()
        for cand in data.get("candidates", []):
            for part in cand.get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    mime = inline.get("mimeType", "image/png")
                    ext = ".jpg" if "jpeg" in mime else ".webp" if "webp" in mime else ".png"
                    out = Path(settings.generated_dir) / f"{uuid4()}{ext}"
                    out.write_bytes(base64.b64decode(inline["data"]))
                    return out
        raise RuntimeError("Gemini returned no generated image. Check the selected image-capable model and API key.")

class XAIImageGenerator:
    def generate(self, source_path: Path, room: str, style: str, prompt: str | None = None) -> Path:
        instruction = (
            f"Photorealistic {room} interior redesign, {style} aesthetic. Preserve the original room structure and viewpoint. "
            "Premium residential interior photography, realistic materials and natural lighting. "
            + (prompt or "")
        )
        url = f"{settings.xai_base_url.rstrip('/')}/images/generations"
        headers = {"Authorization": f"Bearer {settings.ai_api_key}"}
        payload = {"model": settings.ai_model, "prompt": instruction, "n": 1, "response_format": "b64_json"}
        with httpx.Client(timeout=180) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        item = (data.get("data") or [{}])[0]
        raw = item.get("b64_json")
        if raw:
            out = Path(settings.generated_dir) / f"{uuid4()}.png"
            out.write_bytes(base64.b64decode(raw))
            return out
        image_url = item.get("url")
        if image_url:
            content = httpx.get(image_url, timeout=120).content
            out = Path(settings.generated_dir) / f"{uuid4()}.png"
            out.write_bytes(content)
            return out
        raise RuntimeError("xAI returned no image data.")

def get_generator():
    provider = settings.ai_provider.lower()
    if provider in {"locked","disabled"}:
        raise RuntimeError("Photorealistic image generation is locked for the current DecorAI plan.")
    if provider == "mock": return MockDesignGenerator()
    if provider == "gemini": return GeminiGenerator()
    if provider in {"xai", "grok"}: return XAIImageGenerator()
    raise RuntimeError(f"Unsupported AI_PROVIDER={settings.ai_provider}")
