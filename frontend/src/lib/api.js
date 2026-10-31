export const API_BASE = (import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");

export async function api(path, options = {}) {
  const token = localStorage.getItem("decorai-token-v3");
  const headers = new Headers(options.headers || {});

  if (!(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  } catch {
    throw new Error(
      `Cannot connect to DecorAI backend at ${API_BASE}. Start FastAPI with: uvicorn app.main:app --reload`
    );
  }

  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { detail: text };
  }

  if (!response.ok) {
    const detail = data?.detail || data?.message || `Request failed (${response.status})`;
    const message = Array.isArray(detail)
      ? detail.map(item => item?.msg || "Validation error").join(", ")
      : detail;
    throw new Error(message);
  }

  return data;
}
