import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import Logo from "../components/Logo";

export default function Intro() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const t = setTimeout(() => setOpen(true), 700);
    const t2 = setTimeout(() => navigate("/welcome"), 4100);
    return () => { clearTimeout(t); clearTimeout(t2); };
  }, [navigate]);

  return (
    <main className="intro">
      <div className="intro-room">
        <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1800&q=90" alt="Luxury interior"/>
        <div className="intro-overlay"/>
        <motion.div className="intro-light" animate={{opacity:open?1:0}} transition={{duration:2}}/>
      </div>
      <motion.div className={`door door-left ${open ? "open" : ""}`} />
      <motion.div className={`door door-right ${open ? "open" : ""}`} />
      <div className="door-seam"/>
      <div className="intro-center">
        <motion.div initial={{opacity:0,scale:.92}} animate={{opacity:open?1:0,scale:open?1:.92}} transition={{duration:1.2,delay:.7}}>
          <Logo light/>
          <p className="intro-tagline">Your space. Reimagined with intelligence.</p>
          <div className="intro-line"/>
        </motion.div>
      </div>
      <button className="intro-skip" onClick={() => navigate("/welcome")}>Enter DecorAI</button>
    </main>
  );
}
