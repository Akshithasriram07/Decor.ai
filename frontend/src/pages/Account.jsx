import {useEffect,useRef,useState} from "react";
import {Camera,Check,Edit3,Heart,Save,Bell,ShoppingBag} from "lucide-react";
import AppShell from "../components/AppShell";
import InteriorCard from "../components/InteriorCard";
import {useAuth} from "../context/AuthContext";
import {useDesigns} from "../context/DesignContext";
import {api,API_BASE} from "../lib/api";

export default function Account(){
 const{user,setUser,updateUser}=useAuth();
 const{designs,savedProducts}=useDesigns();
 const avatarInput=useRef(null);
 const[orders,setOrders]=useState([]);
 const[notifications,setNotifications]=useState([]);
 const[editing,setEditing]=useState(false);
 const[name,setName]=useState(user?.name||"");
 const[location,setLocation]=useState(user?.location||"");
 const[message,setMessage]=useState("");
 const[avatarError,setAvatarError]=useState("");
 const[avatarUploading,setAvatarUploading]=useState(false);
 const avatarUrl=user?.avatar?.startsWith("http")?user.avatar:user?.avatar?`${API_BASE}${user.avatar}`:"";

 useEffect(()=>{
  Promise.all([api("/api/orders"),api("/api/notifications")])
   .then(([ordersData,notificationsData])=>{setOrders(ordersData);setNotifications(notificationsData)})
   .catch(()=>{});
 },[]);

 async function save(){
  await updateUser({name,location});
  setEditing(false);
  setMessage("Profile updated.");
 }

 async function uploadAvatar(event){
  const input=event.currentTarget;
  const file=input.files?.[0];
  if(!file)return;
  const formData=new FormData();
  formData.append("image",file);
  setAvatarError("");
  setAvatarUploading(true);
  try{
   const updated=await api("/api/users/me/avatar",{method:"POST",body:formData});
   setUser(current=>({...current,...updated}));
   setMessage("Profile photo updated.");
  }catch(error){
   setAvatarError(error.message||"Unable to upload profile photo.");
  }finally{
   setAvatarUploading(false);
   input.value="";
  }
 }

 return <AppShell title="Your account" eyebrow="PERSONAL STUDIO">
  <section className="profile-layout">
   <div className="profile-card-v2 card">
    <div className="profile-photo">
     {avatarUrl?<img className="profile-avatar-image" src={avatarUrl} alt={`${user?.name||"Profile"} avatar`}/>:user?.name?.slice(0,1).toUpperCase()}
     <input ref={avatarInput} type="file" accept="image/jpeg,image/png,image/webp" onChange={uploadAvatar} hidden/>
     <button type="button" onClick={()=>avatarInput.current?.click()} disabled={avatarUploading} aria-label="Upload profile photo" title={avatarUploading?"Uploading photo":"Change profile photo"}><Camera size={15}/></button>
    </div>
    {editing?<>
     <input className="profile-input" value={name} onChange={e=>setName(e.target.value)}/>
     <input className="profile-input" value={location} onChange={e=>setLocation(e.target.value)}/>
     <button className="button dark full" onClick={save}><Check size={15}/> Save profile</button>
    </>:<>
     <span className="eyebrow">PROFILE</span>
     <h2>{user?.name}</h2>
     <p>{user?.email}</p>
     <p className="location">{user?.location}</p>
     <span className="verified-badge">{user?.email_verified?"Verified email":"Email not verified"}</span>
     <button className="button outline account-edit" onClick={()=>setEditing(true)}><Edit3 size={15}/> Edit profile</button>
    </>}
   </div>
   <div className="account-overview card">
    <div><span>DESIGNS</span><strong>{designs.length}</strong><small>Saved concepts</small></div>
    <div><span>WISHLIST</span><strong>{savedProducts.length}</strong><small>Saved pieces</small></div>
    <div><span>ORDERS</span><strong>{orders.length}</strong><small>Shopping history</small></div>
    <div><span>MEMBERSHIP</span><strong>Free</strong><small>{user?.plan}</small></div>
   </div>
  </section>
  {message&&<p className="form-success account-message">{message}</p>}
  {avatarError&&<p className="form-error account-message">{avatarError}</p>}
  <section className="section-head-app"><div><span className="eyebrow">MY DESIGNS</span><h2>Your saved concepts</h2></div></section>
  {designs.length?<div className="dashboard-designs">{designs.map(design=><InteriorCard key={design.id} item={{...design,image:design.image.startsWith("http")?design.image:`${API_BASE}${design.image}`}}/>)}</div>:<div className="empty-state"><Save/><h3>Your designs will appear here.</h3><p>Open the AI Design Studio to create your first concept.</p></div>}
  <section className="account-wishlist">
   <div className="section-head-app"><div><span className="eyebrow">WISHLIST</span><h2>Saved pieces</h2></div></div>
   {savedProducts.length?<div className="wishlist-row">{savedProducts.map(product=><div className="wishlist-item" key={product.id}><img src={product.image} alt={product.name}/><div><b>{product.name}</b><span>₹{product.price.toLocaleString("en-IN")}</span></div><Heart size={16} fill="currentColor"/></div>)}</div>:<div className="empty-state compact"><Heart/><h3>Nothing saved yet.</h3><p>Save products you love from Shopping.</p></div>}
  </section>
  <section className="account-orders">
   <div className="section-head-app"><div><span className="eyebrow">ORDERS</span><h2>Recent orders</h2></div></div>
   {orders.length?orders.slice(0,5).map(order=><div className="order-row card" key={order.id}><div><b>#{order.id.slice(0,8)}</b><span>{new Date(order.created_at).toLocaleDateString()} · {order.items.length} items</span></div><strong>₹{order.total.toLocaleString("en-IN")}</strong><em>{order.status}</em></div>):<div className="empty-state compact"><ShoppingBag/><h3>No orders yet.</h3></div>}
  </section>
  <section className="account-notifications">
   <div className="section-head-app"><div><span className="eyebrow">NOTIFICATIONS</span><h2>Studio updates</h2></div></div>
   {notifications.length?notifications.slice(0,6).map(notification=><div className={`notification-row ${notification.read?"":"unread"}`} key={notification.id}><Bell size={15}/><div><b>{notification.title}</b><p>{notification.message}</p></div></div>):<div className="empty-state compact"><Bell/><h3>No new notifications.</h3></div>}
  </section>
 </AppShell>
}
