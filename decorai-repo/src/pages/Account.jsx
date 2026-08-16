import { useState } from "react";
import { Camera, Check, Edit3, Heart, Save, UserRound } from "lucide-react";
import AppShell from "../components/AppShell";
import InteriorCard from "../components/InteriorCard";
import { useAuth } from "../context/AuthContext";
import { useDesigns } from "../context/DesignContext";

export default function Account(){
  const {user,updateUser}=useAuth(); const {designs,savedProducts}=useDesigns(); const [editing,setEditing]=useState(false); const [name,setName]=useState(user.name); const [location,setLocation]=useState(user.location);
  const save=()=>{updateUser({name,location});setEditing(false)};
  return <AppShell title="Your account" eyebrow="PERSONAL STUDIO">
    <section className="profile-layout">
      <div className="profile-card-v2 card"><div className="profile-photo">{user.name.slice(0,1).toUpperCase()}<button><Camera size={15}/></button></div>{editing?<><input className="profile-input" value={name} onChange={e=>setName(e.target.value)}/><input className="profile-input" value={location} onChange={e=>setLocation(e.target.value)}/><button className="button dark full" onClick={save}><Check size={15}/> Save profile</button></>:<><span className="eyebrow">PROFILE</span><h2>{user.name}</h2><p>{user.email}</p><p className="location">{user.location}</p><button className="button outline" onClick={()=>setEditing(true)}><Edit3 size={15}/> Edit profile</button></>}</div>
      <div className="account-overview card"><div><span>DESIGNS</span><strong>{designs.length}</strong><small>Saved concepts</small></div><div><span>WISHLIST</span><strong>{savedProducts.length}</strong><small>Saved pieces</small></div><div><span>PROJECTS</span><strong>0</strong><small>Active projects</small></div><div><span>MEMBERSHIP</span><strong>Free</strong><small>{user.plan}</small></div></div>
    </section>
    <section className="section-head-app"><div><span className="eyebrow">MY DESIGNS</span><h2>Your saved concepts</h2></div></section>
    {designs.length?<div className="dashboard-designs">{designs.map(d=><InteriorCard key={d.id} item={d}/>)}</div>:<div className="empty-state"><Save/><h3>Your designs will appear here.</h3><p>Open the AI Design Studio to create your first concept.</p></div>}
    <section className="account-wishlist"><div className="section-head-app"><div><span className="eyebrow">WISHLIST</span><h2>Saved pieces</h2></div></div>{savedProducts.length?<div className="wishlist-row">{savedProducts.map(p=><div className="wishlist-item" key={p.id}><img src={p.image} alt={p.name}/><div><b>{p.name}</b><span>₹{p.price.toLocaleString("en-IN")}</span></div><Heart size={16} fill="currentColor"/></div>)}</div>:<div className="empty-state compact"><Heart/><h3>Nothing saved yet.</h3><p>Save products you love from Shopping.</p></div>}</section>
  </AppShell>
}
