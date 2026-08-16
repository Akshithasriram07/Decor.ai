import { useMemo, useState } from "react";
import { Heart, Search, ShoppingBag } from "lucide-react";
import AppShell from "../components/AppShell";
import Reveal from "../components/Reveal";
import { products } from "../data/content";
import { useDesigns } from "../context/DesignContext";

export default function Shopping(){
  const [query,setQuery]=useState(""); const [category,setCategory]=useState("All"); const {savedProducts,toggleProduct}=useDesigns();
  const cats=["All","Furniture","Lighting","Decor"];
  const list=useMemo(()=>products.filter(p=>(category==="All"||p.category===category)&&p.name.toLowerCase().includes(query.toLowerCase())),[category,query]);
  return <AppShell title="Shop your look" eyebrow="DESIGN DISCOVERY" action={<div className="bag-count"><ShoppingBag size={17}/>{savedProducts.length}</div>}>
    <div className="shop-hero"><div><span className="eyebrow">CURATED FOR YOUR SPACE</span><h2>Pieces that make the room.</h2><p>Discover furniture and objects selected to complement the aesthetics you love.</p></div><img src="https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=800&q=85" alt="Interior decor"/></div>
    <div className="shop-toolbar"><div className="search-box"><Search size={17}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search furniture, lighting, decor…"/></div><div className="filter-pills">{cats.map(x=><button key={x} className={category===x?"active":""} onClick={()=>setCategory(x)}>{x}</button>)}</div></div>
    <div className="product-grid-v2">{list.map((p,i)=><Reveal key={p.id} delay={(i%4)*.05}><Product p={p} saved={savedProducts.some(x=>x.id===p.id)} onSave={()=>toggleProduct(p)}/></Reveal>)}</div>
  </AppShell>
}
function Product({p,saved,onSave}){return <article className="product-v2"><div className="product-image"><img src={p.image} alt={p.name}/><button className={saved?"heart saved":"heart"} onClick={onSave}><Heart size={17} fill={saved?"currentColor":"none"}/></button></div><div className="product-info"><span>{p.category}</span><h3>{p.name}</h3><b>₹{p.price.toLocaleString("en-IN")}</b></div></article>}
