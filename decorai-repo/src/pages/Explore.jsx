import { useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";
import AppShell from "../components/AppShell";
import InteriorCard from "../components/InteriorCard";
import Reveal from "../components/Reveal";
import { exploreDesigns } from "../data/content";

const filters=["All","Living Room","Bedroom","Kitchen","Dining","Office"];

export default function Explore(){
  const [query,setQuery]=useState(""); const [filter,setFilter]=useState("All");
  const filtered=useMemo(()=>exploreDesigns.filter(x=>(filter==="All"||x.room===filter)&&`${x.title} ${x.style} ${x.room}`.toLowerCase().includes(query.toLowerCase())),[query,filter]);
  return <AppShell title="Explore" eyebrow="CURATED INSPIRATION">
    <div className="explore-toolbar"><div className="search-box"><Search size={17}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search rooms, styles or moods…"/></div><button className="filter-button"><SlidersHorizontal size={16}/> Filters</button></div>
    <div className="filter-pills">{filters.map(x=><button key={x} className={filter===x?"active":""} onClick={()=>setFilter(x)}>{x}</button>)}</div>
    <div className="explore-grid">{filtered.map((item,i)=><Reveal key={item.id} delay={(i%4)*.05}><InteriorCard item={item} tall={i%5===0}/></Reveal>)}</div>
    {!filtered.length&&<div className="empty-state"><h3>No rooms found</h3><p>Try a different search or category.</p></div>}
  </AppShell>
}
