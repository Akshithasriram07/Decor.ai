import { Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Intro from "./pages/Intro";
import Landing from "./pages/Landing";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import Studio from "./pages/Studio";
import Explore from "./pages/Explore";
import Shopping from "./pages/Shopping";
import Workers from "./pages/Workers";
import Account from "./pages/Account";
import ProtectedRoute from "./components/ProtectedRoute";

function Page({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.42, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}

function AnimatedRoutes() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Page><Intro /></Page>} />
        <Route path="/welcome" element={<Page><Landing /></Page>} />
        <Route path="/signin" element={<Page><SignIn /></Page>} />
        <Route path="/signup" element={<Page><SignUp /></Page>} />
        <Route path="/app" element={<ProtectedRoute><Page><Dashboard /></Page></ProtectedRoute>} />
        <Route path="/studio" element={<ProtectedRoute><Page><Studio /></Page></ProtectedRoute>} />
        <Route path="/explore" element={<ProtectedRoute><Page><Explore /></Page></ProtectedRoute>} />
        <Route path="/shopping" element={<ProtectedRoute><Page><Shopping /></Page></ProtectedRoute>} />
        <Route path="/workers" element={<ProtectedRoute><Page><Workers /></Page></ProtectedRoute>} />
        <Route path="/account" element={<ProtectedRoute><Page><Account /></Page></ProtectedRoute>} />
        <Route path="*" element={<Page><Landing /></Page>} />
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  return <AnimatedRoutes />;
}
