import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, Plus, Bookmark } from "lucide-react";
import AppShell from "../components/AppShell";
import InteriorCard from "../components/InteriorCard";
import Reveal from "../components/Reveal";
import { useAuth } from "../context/AuthContext";
import { useDesigns } from "../context/DesignContext";
import { exploreDesigns } from "../data/content";

export default function Dashboard(){
  const {user}=useAuth(); const {designs,savedProducts}=useDesigns();
  return <AppShell title={`Good to see you, ${user.name.split(" ")[0]}.`} eyebrow="YOUR DESIGN SPACE">
    <section className="dashboard-hero">
      <div><span className="eyebrow">READY WHEN YOU ARE</span><h2>What will you transform today?</h2><p>Start from a room photo and let DecorAI help you shape the direction.</p><Link className="button light" to="/studio">Open AI Design Studio <ArrowRight size={16}/></Link></div>
      <div className="dashboard-hero-image"><img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1100&q=85" alt="Modern living room"/></div>
    </section>
    <section className="stats-row"><Stat label="Saved designs" value={designs.length}/><Stat label="Wishlist" value={savedProducts.length}/><Stat label="Projects" value="0"/><Stat label="Design ideas" value={exploreDesigns.length}/></section>
    <Reveal><div className="section-head-app"><div><span className="eyebrow">YOUR COLLECTION</span><h2>Recent designs</h2></div><Link to="/account">View all <ArrowRight size={15}/></Link></div></Reveal>
    <div className="dashboard-designs">{designs.slice(0,3).map((d,i)=><Reveal key={d.id} delay={i*.08}><InteriorCard item={d}/></Reveal>)}<Link className="new-design-card" to="/studio"><Plus/><span>Start a new design</span><small>Upload a room photo</small></Link></div>
    <Reveal><div className="section-head-app"><div><span className="eyebrow">INSPIRATION</span><h2>Designed to spark an idea</h2></div><Link to="/explore">Explore all <ArrowRight size={15}/></Link></div></Reveal>
    <div className="dashboard-designs">{exploreDesigns.slice(0,3).map((d,i)=><Reveal key={d.id} delay={i*.08}><InteriorCard item={d}/></Reveal>)}</div>
  </AppShell>
}
function Stat({label,value}){return <div className="stat-card"><span>{label}</span><strong>{value}</strong></div>}
