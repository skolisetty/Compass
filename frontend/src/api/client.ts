const BASE = "/api";

async function request<T>(path: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

/* ── Types ──────────────────────────────────────────────────────────── */

export interface Voice {
  id: string;
  user_id: string;
  name: string;
  role: string;
  domains: string;
  icon: string;
}

export interface Guideline {
  id: string;
  user_id: string;
  voice_id: string | null;
  author_name: string;
  author_role: string;
  domain: string;
  guideline_text: string;
  is_safety: boolean;
  active: boolean;
  created_at: string;
}

export interface Attribution {
  voice_name: string;
  voice_icon: string;
  guideline_text: string;
}

export interface AskResponse {
  answer: string;
  attributions: Attribution[];
}

export interface GuidanceOverview {
  voices: { voice: Voice; guidelines: Guideline[] }[];
  platform_defaults: string[];
}

export interface HealthEvent {
  id: string;
  user_id: string;
  event_type: string;
  activity_type: string | null;
  duration_minutes: number | null;
  timestamp: string;
}

/* ── API calls ──────────────────────────────────────────────────────── */

export const api = {
  getVoices: (userId: string) =>
    request<Voice[]>(`/voices/${userId}`),

  getGuidelines: (userId: string, voiceId?: string) =>
    request<Guideline[]>(
      `/guidelines/${userId}${voiceId ? `?voice_id=${voiceId}` : ""}`
    ),

  createGuideline: (
    userId: string,
    voiceId: string,
    data: { guideline_text: string; domain?: string; is_safety?: boolean }
  ) =>
    request<Guideline>(`/guidelines/${userId}/${voiceId}`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  deleteGuideline: (id: string) =>
    request(`/guidelines/${id}`, { method: "DELETE" }),

  getOverview: (userId: string) =>
    request<GuidanceOverview>(`/overview/${userId}`),

  ask: (userId: string, question: string) =>
    request<AskResponse>("/ask", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, question }),
    }),

  logWorkout: (
    userId: string,
    data: {
      activity_type: string;
      duration_minutes: number;
      distance_km?: number;
      calories?: number;
    }
  ) =>
    request<HealthEvent>(`/health/${userId}`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  logMood: (userId: string, mood: number) =>
    request(`/mood/${userId}`, {
      method: "POST",
      body: JSON.stringify({ mood }),
    }),
};
