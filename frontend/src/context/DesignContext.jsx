import {createContext,useContext,useEffect,useMemo,useState} from "react";
import {api} from "../lib/api";
const C=createContext(null);
export function DesignProvider({children}){
  const [designs,setDesigns]=useState([]); const [savedProducts,setSavedProducts]=useState([]); const [cart,setCart]=useState({items:[],subtotal:0,shipping:0,total:0});
  const [refresh,setRefresh]=useState(0);
  useEffect(()=>{(async()=>{try{const [d,w,c]=await Promise.all([api("/api/designs"),api("/api/wishlist"),api("/api/cart")]);setDesigns(d);setSavedProducts(w);setCart(c)}catch{}})()},[refresh]);
  const saveDesign=async(d)=>{setDesigns(x=>[d,...x.filter(i=>i.id!==d.id)]);return d};
  const toggleProduct=async(p)=>{const exists=savedProducts.some(x=>x.id===p.id);if(exists)await api(`/api/wishlist/${p.id}`,{method:"DELETE"});else await api(`/api/wishlist/${p.id}`,{method:"POST"});setRefresh(x=>x+1)};
  const addToCart=async(p,quantity=1)=>{await api("/api/cart/items",{method:"POST",body:JSON.stringify({product_id:p.id,quantity})});setRefresh(x=>x+1)};
  const updateCart=async(itemId,quantity)=>{await api(`/api/cart/items/${itemId}`,{method:"PATCH",body:JSON.stringify({quantity})});setRefresh(x=>x+1)};
  const removeCart=async(itemId)=>{await api(`/api/cart/items/${itemId}`,{method:"DELETE"});setRefresh(x=>x+1)};
  const value=useMemo(()=>({designs,savedProducts,cart,saveDesign,toggleProduct,addToCart,updateCart,removeCart,refreshCart:()=>setRefresh(x=>x+1)}),[designs,savedProducts,cart]);
  return <C.Provider value={value}>{children}</C.Provider>
}
export const useDesigns=()=>useContext(C);
