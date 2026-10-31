import {useEffect,useMemo,useState} from "react";
import {Search,X,SlidersHorizontal} from "lucide-react";
import AppShell from "../components/AppShell";
import Reveal from "../components/Reveal";
import {api,API_BASE} from "../lib/api";
import {exploreDesigns} from "../data/content";

const mediaUrl=value=>value?.startsWith("http")?value:`${API_BASE}${value||""}`;
const rooms=["All","Living Room","Bedroom","Kitchen","Bathroom","Dining","Home Office","Puja Room","Balcony","Kids Room","Entryway","Villa"];
const styles=["All","Modern Indian","Indian Contemporary","Warm Modern","Quiet Luxury","Contemporary","Minimal","Japandi","Traditional Indian","Organic","Luxury"];

export default function Explore(){
 const[q,setQ]=useState("");const[filter,setFilter]=useState("All");const[style,setStyle]=useState("All");const[list,setList]=useState([]);const[selected,setSelected]=useState(null);const[loading,setLoading]=useState(true);
 const fallback=useMemo(()=>exploreDesigns.filter(item=>
   (filter==="All"||item.room===filter)&&
   (style==="All"||item.style===style)&&
   (!q||`${item.title} ${item.room} ${item.style}`.toLowerCase().includes(q.toLowerCase()))
 ),[q,filter,style]);
 useEffect(()=>{const t=setTimeout(async()=>{
   setLoading(true);
   try{const remote=await api(`/api/explore?q=${encodeURIComponent(q)}&room=${encodeURIComponent(filter)}&style=${encodeURIComponent(style)}`);setList(remote.length?remote:fallback)}
   catch{setList(fallback)}
   finally{setLoading(false)}
 },180);return()=>clearTimeout(t)},[q,filter,style]);
 return <AppShell title="Explore" eyebrow="CURATED INSPIRATION">
  <div className="explore-toolbar"><div className="search-box"><Search size={17}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search rooms, styles or moods…"/></div><span className="explore-count"><SlidersHorizontal size={14}/>{loading?"Updating collection…":`${list.length} spaces`}</span></div>
  <div className="explore-filter-label">Rooms</div><div className="filter-pills filter-scroll">{rooms.map(x=><button key={x} className={filter===x?"active":""} onClick={()=>setFilter(x)}>{x}</button>)}</div>
  <div className="explore-filter-label">Styles</div><div className="filter-pills filter-scroll">{styles.map(x=><button key={x} className={style===x?"active":""} onClick={()=>setStyle(x)}>{x}</button>)}</div>
  <div className="explore-grid">{list.map((item,i)=><Reveal key={`${item.id}-${item.image}`} delay={(i%4)*.05}><article className="interior-card explore-open" onClick={()=>setSelected(item)}><img src={mediaUrl(item.image)} alt={item.title} loading="lazy"/><div className="image-shade"/><div className="interior-card-copy"><span>{item.room}</span><h3>{item.title}</h3><small>{item.style}</small></div><div className="explore-view">View full room</div></article></Reveal>)}</div>
  {!loading&&!list.length&&<div className="empty-state"><h3>No spaces match those filters</h3><p>Try another room or style. The collection is organised by room first, then aesthetic.</p></div>}
  {selected&&<div className="modal-backdrop" onClick={()=>setSelected(null)}><div className="design-modal" onClick={e=>e.stopPropagation()}><button className="modal-close" onClick={()=>setSelected(null)}><X/></button><div className="design-modal-image"><img src={mediaUrl(selected.image)} alt={selected.title}/></div><div className="design-modal-copy"><span className="eyebrow">{selected.room}</span><h2>{selected.title}</h2><p>{selected.description||`A considered ${selected.style} ${selected.room.toLowerCase()} concept with layered materials, lighting and practical styling.`}</p><div className="detail-tags"><span>{selected.style}</span><span>{selected.room}</span><span>DecorAI collection</span></div></div></div></div>}
 </AppShell>
}
