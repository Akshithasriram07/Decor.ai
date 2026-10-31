from pathlib import Path
from typing import Any
import base64
import mimetypes
import json
import time
import httpx
from app.core.config import settings


def _local_analysis(source_path: Path, room: str, style: str, prompt: str | None = None) -> dict[str, Any]:
    try:
        from PIL import Image
        from transformers import pipeline
        captioner = pipeline("image-to-text", model=settings.ai_text_model, device=-1)
        image = Image.open(source_path).convert("RGB")
        caption_result = captioner(image, max_new_tokens=60)
        caption = (caption_result[0].get("generated_text") or "").strip()
    except Exception as exc:
        raise RuntimeError(f"Local image analysis is unavailable: {exc}") from exc
    return _build_analysis(room, style, prompt, caption, "local")


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].lstrip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise


def _normalise_analysis(parsed: dict[str, Any], room: str, style: str) -> dict[str, Any]:
    suggestions = parsed.get("suggestions") or []
    strengths = parsed.get("strengths") or []
    improvements = parsed.get("improvements") or []
    style_notes = parsed.get("style_notes") or []
    return {
        "title": str(parsed.get("title") or f"{style} {room} analysis"),
        "room": room,
        "style": style,
        "caption": str(parsed.get("caption") or "The uploaded room image was visually analysed."),
        "summary": str(parsed.get("summary") or "DecorAI analysed the uploaded room and prepared practical modifications."),
        "strengths": [str(x) for x in strengths[:5]],
        "improvements": [str(x) for x in improvements[:5]],
        "style_notes": [str(x) for x in style_notes[:4]],
        "suggestions": [
            {"title": str(item.get("title", "Recommendation")), "detail": str(item.get("detail", ""))}
            for item in suggestions[:8] if isinstance(item, dict)
        ],
        "provider": "gemini",
    }


def _gemini_models() -> list[str]:
    primary = (settings.ai_text_model or "gemini-3.8-flash").strip()
    fallbacks = [x.strip() for x in (settings.ai_text_fallback_models or "").split(",") if x.strip()]
    return list(dict.fromkeys([primary, *fallbacks]))


def _gemini_analysis(source_path: Path, room: str, style: str, prompt: str | None = None) -> dict[str, Any]:
    if not settings.ai_api_key:
        raise RuntimeError("Gemini API key is not configured. Add AI_API_KEY to backend/.env.")

    mime = mimetypes.guess_type(source_path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(source_path.read_bytes()).decode("utf-8")
    user_requirements = prompt.strip() if prompt else "No additional requirements were provided."
    instruction = f"""
You are DecorAI's interior-design vision assistant. The uploaded image is the PRIMARY source of truth.
Actually inspect the image before writing the answer. Do not rely on the selected room label if the image contradicts it.

Selected room context: {room}
Preferred design direction: {style}
User requirements: {user_requirements}

Return ONLY valid JSON with this exact structure:
{{
  "title": "short professional title",
  "caption": "one sentence describing only clearly visible elements in the uploaded image",
  "summary": "2-4 sentences explaining what the room currently looks like and the overall improvement plan",
  "strengths": ["2-4 things that are already working"],
  "improvements": ["2-4 specific visible issues or opportunities"],
  "style_notes": ["2-3 concrete ways the selected style should be applied to this room"],
  "suggestions": [
    {{"title":"short actionable heading", "detail":"specific modification based on what you can actually see and the user's requirements"}}
  ]
}}

Give 5-7 useful suggestions. Mention visible furniture, layout, lighting, windows, flooring, colours and empty areas when they are genuinely visible.
Do not invent measurements, furniture, structural features or objects that cannot reasonably be seen.
Prioritise practical changes. Do not suggest structural wall changes unless the user explicitly asks for them.
If the user asks to keep an item, explicitly preserve it.
Keep recommendations specific enough that a homeowner could act on them.
"""
    payload = {
        "contents": [{"parts": [
            {"text": instruction},
            {"inline_data": {"mime_type": mime, "data": encoded}},
        ]}],
        "generationConfig": {"temperature": 0.25, "responseMimeType": "application/json"},
    }

    errors = []
    with httpx.Client(timeout=90) as client:
        for model in _gemini_models():
            url = f"{settings.ai_base_url.rstrip('/')}/models/{model}:generateContent"
            for attempt in range(2):
                try:
                    response = client.post(url, params={"key": settings.ai_api_key}, json=payload)
                except httpx.HTTPError as exc:
                    errors.append(f"{model}: {exc}")
                    break

                if response.status_code < 400:
                    try:
                        data = response.json()
                        text = "".join(
                            part.get("text", "")
                            for candidate in data.get("candidates", [])
                            for part in candidate.get("content", {}).get("parts", [])
                        ).strip()
                        if not text:
                            raise RuntimeError("Gemini returned an empty analysis response.")
                        parsed = _extract_json(text)
                        if not isinstance(parsed, dict) or not isinstance(parsed.get("suggestions"), list):
                            raise ValueError("Gemini response did not contain a suggestions list.")
                        return _normalise_analysis(parsed, room, style)
                    except (ValueError, json.JSONDecodeError, RuntimeError) as exc:
                        errors.append(f"{model}: invalid response: {exc}")
                        break

                try:
                    detail = response.json().get("error", {}).get("message", response.text)
                except Exception:
                    detail = response.text
                errors.append(f"{model}: Gemini request failed ({response.status_code}): {detail}")

                # 429/5xx are commonly transient. Retry once before trying the fallback model.
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt == 0:
                        time.sleep(1.2)
                        continue
                break

    raise RuntimeError("Gemini room analysis failed after trying the configured model(s). " + " | ".join(errors[-4:]))


def analyze_room_image(source_path: Path, room: str, style: str, prompt: str | None = None) -> dict[str, Any]:
    """Analyze a room photo and return a written design plan. Image generation is not involved."""
    provider = (settings.ai_text_provider or "local").lower()
    if provider == "gemini":
        return _gemini_analysis(source_path, room, style, prompt)
    return _local_analysis(source_path, room, style, prompt)


def _build_analysis(room: str, style: str, prompt: str | None, caption: str, provider: str) -> dict[str, Any]:
    style_lower = style.lower()
    caption_lower = caption.lower()
    room_lower = room.lower()
    requirements = prompt.strip() if prompt else "Keep the design practical and visually balanced."
    suggestions = [
        {"title": "Protect the existing layout", "detail": f"The image appears to show a {room_lower}. Keep the main circulation path and the strongest existing furniture relationship unless the room clearly needs re-planning."},
        {"title": f"Build the {style} direction", "detail": _style_tip(style_lower)},
        {"title": "Layer the lighting", "detail": "Use ambient lighting plus focused task lighting and a warm accent layer. Keep the main focal area brighter than secondary corners."},
        {"title": "Create one clear focal point", "detail": "Choose one wall, furniture group or artwork area as the visual anchor and keep nearby surfaces quieter so the room feels more intentional."},
        {"title": "Add Indian material character", "detail": "Use teak or cane, handloom textiles, brass, terracotta, stone or locally crafted decor as controlled accents rather than filling every surface."},
        {"title": "Apply the user's brief", "detail": f"Prioritise this requirement while making changes: {requirements}"},
    ]
    if any(k in caption_lower for k in ["sofa", "couch", "chair"]):
        suggestions.append({"title": "Refine the seating zone", "detail": "Keep comfortable walking space around the seating and use a properly scaled rug and coffee-table relationship to visually connect the furniture."})
    if any(k in caption_lower for k in ["bed", "bedroom"]):
        suggestions.append({"title": "Calm the sleeping zone", "detail": "Use layered bedside lighting, soft textiles and concealed storage so the bed remains the visual anchor without making the room feel crowded."})
    return {"title": f"{style} {room} analysis", "room": room, "style": style, "caption": caption or "The room was analysed visually.", "summary": f"DecorAI analysed the uploaded {room_lower} with the {style} direction and translated the visual reading into practical recommendations. This is a text-only planning step; image generation is not required.", "strengths": ["The uploaded image was visually reviewed.", "The recommendations are tailored to the selected room and style."], "improvements": ["Add clearer functional zoning where the room needs it.", "Strengthen lighting, texture and focal hierarchy where appropriate."], "style_notes": [_style_tip(style_lower)], "suggestions": suggestions, "provider": provider}


def _style_tip(style: str) -> str:
    tips = {
        "modern indian": "Combine clean contemporary proportions with one or two recognisable Indian craft elements such as teak, brass, cane, handloom or stone.",
        "indian contemporary": "Keep the base restrained and introduce Indian character through material, art, textile and craft rather than excessive ornament.",
        "kerala traditional": "Use warm timber, cane, natural fibres, muted earthy colour and a few traditional craft details while protecting daylight and ventilation.",
        "chettinad heritage": "Use rich wood, brass, patterned textiles and heritage-inspired details as accents, balanced by open negative space.",
        "rajasthani haveli": "Use lime/plaster-like warmth, carved or crafted wood, brass and controlled artisan colour without turning the room into a theme set.",
    }
    return tips.get(style, "Use the selected style as a material and proportion guide: repeat two or three finishes, keep the palette coherent, and leave visual breathing room.")
