import { useMemo, useState } from "react";
import { MapPin, Search, Star, MessageCircle, BriefcaseBusiness } from "lucide-react";
import AppShell from "../components/AppShell";
import Reveal from "../components/Reveal";
import { workers } from "../data/content";

const roles=["All","Interior Designer","Carpenter","Painter","Electrician"];

export default function Workers(){
  const [q,setQ]=useState("");const [role,setRole]=useState("All");
  const list=useMemo(()=>workers.filter(w=>(role==="All"||w.role===role)&&`${w.name} ${w.role} ${w.location}`.toLowerCase().includes(q.toLowerCase())),[q,role]);
  return <AppShell title="Find trusted professionals" eyebrow="FROM IDEA TO REAL ROOM">
    <section className="workers-hero"><div><span className="eyebrow">LOCAL EXPERTISE</span><h2>Build the room you imagined.</h2><p>Discover skilled professionals for the work that happens after the concept.</p></div><img src="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1100&q=85" alt="Interior design workspace"/></section>
    <div className="worker-search"><div className="search-box"><Search size={17}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search by name, service or city…"/></div><div className="filter-pills">{roles.map(x=><button key={x} className={role===x?"active":""} onClick={()=>setRole(x)}>{x}</button>)}</div></div>
    <div className="worker-grid">{list.map((w,i)=><Reveal key={w.id} delay={(i%3)*.06}><article className="worker-card-v2"><div className="worker-cover"><img src={w.image} alt={w.name}/><span>Available</span></div><div className="worker-body"><div className="worker-name-row"><div><h3>{w.name}</h3><p>{w.role}</p></div><div className="rating"><Star size={14} fill="currentColor"/>{w.rating}</div></div><div className="worker-meta"><span><MapPin size={14}/>{w.location}</span><span><BriefcaseBusiness size={14}/>{w.jobs} projects</span></div><div className="worker-actions"><button className="button outline">View profile</button><button className="icon-button dark-icon" title="Message"><MessageCircle size={17}/></button></div></div></article></Reveal>)}</div>
  </AppShell>
}
