import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function AdminRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="route-loading">Checking access…</div>;
  if (!user) return <Navigate to="/signin" replace />;
  if (user.role !== "admin") return <Navigate to="/app" replace />;
  return children;
}
