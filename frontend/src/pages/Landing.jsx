import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, Palette, Sofa, ShieldCheck, Sun, Moon } from "lucide-react";
import { motion } from "framer-motion";
import Logo from "../components/Logo";
import Reveal from "../components/Reveal";
import {useTheme} from "../context/ThemeContext";

export default function Landing() { const {theme,toggleTheme}=useTheme();
  return (
    <main className="landing">
      <nav className="landing-nav"><Logo/><div className="landing-links"><a href="#how">How it works</a><a href="#inspiration">Inspiration</a><a href="#professionals">Professionals</a></div><div className="landing-actions"><button className="theme-toggle landing-theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">{theme==="light"?<Moon size={17}/>:<Sun size={17}/>}</button><Link to="/signin" className="plain-link">Sign in</Link><Link to="/signup" className="nav-cta">Create account</Link></div></nav>

      <section className="landing-hero">
        <div className="landing-hero-copy">
          <span className="eyebrow">AI-POWERED INTERIOR DESIGN</span>
          <h1>Make your home feel <em>exceptional.</em></h1>
          <p>DecorAI turns the rooms you have into the spaces you've imagined — from first inspiration to final detail.</p>
          <div className="hero-cta-row"><Link className="button dark" to="/signup">Start designing <ArrowRight size={16}/></Link><a className="plain-link" href="#how">See how it works</a></div>
          <div className="hero-proof"><span><ShieldCheck size={15}/> Personal design workspace</span><span><Sparkles size={15}/> AI-assisted concepts</span></div>
        </div>
        <div className="landing-hero-image"><img src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1500&q=90" alt="Luxury living room"/><div className="floating-design-card"><span>AI CONCEPT</span><b>Quiet Luxury</b><small>Warm oak · linen · natural stone</small></div></div>
      </section>

      <section className="brand-strip"><span>DESIGN</span><span>VISUALIZE</span><span>DISCOVER</span><span>BUILD</span></section>

      <section id="how" className="landing-section">
        <Reveal><div className="section-intro"><span className="eyebrow">THE DECORAI METHOD</span><h2>One calm workspace for the entire journey.</h2><p>Start with a photograph. Finish with a room you can actually build.</p></div></Reveal>
        <div className="method-grid">
          {[["01","Upload","Give DecorAI a photo of your existing room."],["02","Imagine","Choose your style, mood, palette and priorities."],["03","Create","Generate a visual concept and refine the details."],["04","Build","Save products and find trusted local professionals."]].map(([n,t,d],i)=><Reveal key={n} delay={i*.08}><article className="method-card"><span>{n}</span><h3>{t}</h3><p>{d}</p></article></Reveal>)}
        </div>
      </section>

      <section id="inspiration" className="landing-feature">
        <div className="feature-image"><img src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1400&q=90" alt="Warm modern living room"/></div>
        <div className="feature-copy"><span className="eyebrow">YOUR AI DESIGN STUDIO</span><h2>See possibilities before you move a single piece of furniture.</h2><p>Explore styles, upload your room and create a visual direction that feels personal — not generic.</p><Link className="text-button" to="/signup">Create your first concept <ArrowRight size={16}/></Link></div>
      </section>

      <section className="landing-gallery">
        <Reveal><div className="section-intro"><span className="eyebrow">CURATED INSPIRATION</span><h2>Rooms worth coming home to.</h2></div></Reveal>
        <div className="landing-photo-grid">
          <img src="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=900&q=85" alt="Living room"/>
          <img className="wide" src="https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=85" alt="Kitchen"/>
          <img src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=85" alt="Bedroom"/>
        </div>
      </section>

      <section id="professionals" className="landing-final"><span className="eyebrow">FROM IDEA TO REAL ROOM</span><h2>When you're ready to build, DecorAI helps you take the next step.</h2><p>Save your design, discover pieces that fit it, and connect with skilled professionals.</p><Link className="button light" to="/signup">Begin your design journey <ArrowRight size={16}/></Link></section>
      <footer className="landing-footer"><Logo/><span>Build your dream home.</span><small>© 2026 DecorAI</small></footer>
    </main>
  );
}
