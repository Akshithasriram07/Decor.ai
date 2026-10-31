import {Link} from "react-router-dom";
import {Instagram,Linkedin,Mail,ArrowUpRight} from "lucide-react";
import Logo from "./Logo";

export default function Footer(){
  return <footer className="site-footer">
    <div className="footer-main">
      <div className="footer-brand"><Logo/><p>Indian-first AI interior design for homes that feel like you.</p><div className="footer-socials">
        <a href="https://www.linkedin.com/" target="_blank" rel="noreferrer" aria-label="LinkedIn"><Linkedin size={17}/></a>
        <a href="https://www.instagram.com/" target="_blank" rel="noreferrer" aria-label="Instagram"><Instagram size={17}/></a>
        <a href="mailto:hello@decorai.local" aria-label="Email"><Mail size={17}/></a>
      </div></div>
      <div><b>Explore</b><Link to="/app">Home</Link><Link to="/explore">Indian interiors</Link><Link to="/shopping">Shopping</Link><Link to="/workers">Local workers</Link></div>
      <div><b>Studio</b><Link to="/studio">AI Design Studio</Link><Link to="/account">Your profile</Link><Link to="/account">Notifications</Link></div>
      <div><b>About DecorAI</b><p>College project · Indian-focused interior discovery · Built for simple, accessible design.</p><a href="mailto:hello@decorai.local">Contact us <ArrowUpRight size={13}/></a></div>
    </div>
    <div className="footer-bottom"><span>© 2026 DecorAI. All rights reserved.</span><span>Designed for clarity. Built for the next room.</span></div>
  </footer>
}
