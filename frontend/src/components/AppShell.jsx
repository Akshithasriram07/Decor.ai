import {NavLink,useNavigate} from "react-router-dom";
import {Home,Sparkles,Compass,ShoppingBag,Users,UserRound,LogOut,ShieldCheck,Bell,Sun,Moon} from "lucide-react";
import Logo from "./Logo";
import {useAuth} from "../context/AuthContext";
import {useTheme} from "../context/ThemeContext";
import {useEffect,useState} from "react";
import {api} from "../lib/api";

const nav=[["/app","Home",Home],["/studio","AI Design Studio",Sparkles],["/explore","Explore",Compass],["/shopping","Shopping",ShoppingBag],["/workers","Local Workers",Users],["/account","Account",UserRound]];

export default function AppShell({children,title,eyebrow="DECORAI STUDIO",action}){
 const {user,signOut}=useAuth(); const {theme,toggleTheme}=useTheme(); const navigate=useNavigate();
 const [notifications,setNotifications]=useState([]); const [open,setOpen]=useState(false);
 useEffect(()=>{if(!user)return;api("/api/notifications").then(setNotifications).catch(()=>{})},[user]);
 const unread=notifications.filter(n=>!n.read).length;
 async function markRead(n){if(!n.read){await api(`/api/notifications/${n.id}/read`,{method:"POST"}).catch(()=>{});setNotifications(xs=>xs.map(x=>x.id===n.id?{...x,read:true}:x));}}
 return <div className="app-shell">
   <aside className="sidebar"><Logo/><nav className="sidebar-nav">{nav.map(([to,label,Icon])=><NavLink key={to} to={to} className={({isActive})=>isActive?"nav-link active":"nav-link"}><Icon size={19}/><span>{label}</span></NavLink>)}{user?.role==="admin"&&<NavLink to="/admin" className={({isActive})=>isActive?"nav-link active":"nav-link"}><ShieldCheck size={19}/><span>Admin</span></NavLink>}</nav>
   <div className="sidebar-bottom"><div className="sidebar-promo"><span>DESIGN BETTER</span><p>Turn an ordinary room into a space with intention.</p></div><button className="sidebar-logout" onClick={()=>{signOut();navigate("/");}}><LogOut size={17}/> Sign out</button></div></aside>
   <main className="app-main">
    <header className="topbar">
      <div className="topbar-brand"><span className="topbar-mobile-title">DecorAI</span><span className="topbar-context">{eyebrow}</span></div>
      <div className="top-actions">
       <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme==="light"?"dark":"light"} theme`} aria-label="Toggle theme">{theme==="light"?<Moon size={19}/>:<Sun size={19}/>}</button>
       <div className="notification-wrap"><button className="notification-button" onClick={()=>setOpen(v=>!v)} aria-label="Notifications"><Bell size={19}/>{unread>0&&<span>{unread>9?"9+":unread}</span>}</button>
       {open&&<div className="notification-popover"><div className="notification-popover-head"><div><b>Notifications</b><small>{unread?`${unread} unread`:"You're all caught up"}</small></div><button onClick={()=>setOpen(false)}>Close</button></div>{notifications.length?notifications.slice(0,6).map(n=><button key={n.id} className={`notification-pop ${n.read?"":"unread"}`} onClick={()=>markRead(n)}><Bell size={16}/><span><b>{n.title}</b><small>{n.message}</small></span></button>):<p className="notification-empty">No notifications yet.</p>}<NavLink to="/account" onClick={()=>setOpen(false)}>View all notifications</NavLink></div>}</div>
       <div className="top-user"><div className="user-avatar">{user?.name?.slice(0,1)?.toUpperCase()||"D"}</div><div><b>{user?.name||"Designer"}</b><small>{user?.plan||"Design Member"}</small></div></div>
      </div>
    </header>
    <div className="page-wrap"><div className="page-title-row"><div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1></div>{action}</div>{children}</div>
   </main>
 </div>
}
