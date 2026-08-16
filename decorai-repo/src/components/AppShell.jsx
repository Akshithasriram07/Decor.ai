import { NavLink, Link, useNavigate } from "react-router-dom";
import { Home, Sparkles, Compass, ShoppingBag, Users, UserRound, LogOut, Search } from "lucide-react";
import Logo from "./Logo";
import { useAuth } from "../context/AuthContext";

const nav = [
  ["/app", "Home", Home],
  ["/studio", "AI Design Studio", Sparkles],
  ["/explore", "Explore", Compass],
  ["/shopping", "Shopping", ShoppingBag],
  ["/workers", "Local Workers", Users],
  ["/account", "Account", UserRound]
];

export default function AppShell({ children, title, eyebrow="DECORAI STUDIO", action }) {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Logo />
        <nav className="sidebar-nav">
          {nav.map(([to,label,Icon]) => (
            <NavLink key={to} to={to} className={({isActive}) => isActive ? "nav-link active" : "nav-link"}>
              <Icon size={17}/><span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-promo">
            <span>DESIGN BETTER</span>
            <p>Turn an ordinary room into a space with intention.</p>
          </div>
          <button className="sidebar-logout" onClick={() => { signOut(); navigate("/"); }}>
            <LogOut size={15}/> Sign out
          </button>
        </div>
      </aside>

      <main className="app-main">
        <header className="topbar">
          <div className="top-search"><Search size={16}/><input placeholder="Search DecorAI"/></div>
          <div className="top-user">
            <div className="user-avatar">{user?.name?.slice(0,1)?.toUpperCase() || "D"}</div>
            <div><b>{user?.name || "Designer"}</b><small>{user?.plan || "Design Member"}</small></div>
          </div>
        </header>
        <div className="page-wrap">
          <div className="page-title-row">
            <div><span className="eyebrow">{eyebrow}</span><h1>{title}</h1></div>
            {action}
          </div>
          {children}
        </div>
      </main>
    </div>
  );
}
