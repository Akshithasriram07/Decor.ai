import { createContext, useContext, useEffect, useMemo, useState } from "react";

const AuthContext = createContext(null);
const KEY = "decorai-auth-v2";

const defaultUser = {
  id: "demo-user",
  name: "Your Name",
  email: "you@decorai.app",
  plan: "Design Member",
  location: "India",
  avatar: ""
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(KEY)) || null;
    } catch {
      return null;
    }
  });

  useEffect(() => {
    if (user) localStorage.setItem(KEY, JSON.stringify(user));
    else localStorage.removeItem(KEY);
  }, [user]);

  const signUp = async ({ name, email }) => {
    const next = { ...defaultUser, id: crypto.randomUUID(), name, email };
    setUser(next);
    return next;
  };

  const signIn = async ({ email }) => {
    const saved = JSON.parse(localStorage.getItem(KEY) || "null");
    const next = saved?.email === email
      ? saved
      : { ...defaultUser, id: crypto.randomUUID(), name: email.split("@")[0], email };
    setUser(next);
    return next;
  };

  const signOut = () => setUser(null);

  const updateUser = (updates) => setUser(prev => ({ ...prev, ...updates }));

  const value = useMemo(() => ({
    user, signUp, signIn, signOut, updateUser, isAuthenticated: Boolean(user)
  }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
