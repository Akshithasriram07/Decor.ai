import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import Logo from "../components/Logo";
import { useAuth } from "../context/AuthContext";

export default function SignIn() {
  const { signIn } = useAuth();
  const [form,setForm] = useState({email:"",password:""});
  const [error,setError] = useState("");
  const navigate=useNavigate();
  const location=useLocation();

  async function submit(e){
    e.preventDefault();
    if(!form.email || form.password.length < 6){ setError("Enter a valid email and a password with at least 6 characters."); return; }
    await signIn(form);
    navigate(location.state?.from || "/app", {replace:true});
  }

  return <AuthPage title="Welcome back" subtitle="Continue creating spaces that feel like home.">
    <form className="auth-form" onSubmit={submit}>
      <label>Email<input type="email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="you@example.com"/></label>
      <label>Password<input type="password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} placeholder="At least 6 characters"/></label>
      {error && <p className="form-error">{error}</p>}
      <button className="button dark full">Sign in</button>
      <div className="auth-divider"><span>or</span></div>
      <button type="button" className="button outline full" onClick={()=>{setForm({email:"demo@decorai.app",password:"123456"});setError("")}}>Use demo account</button>
    </form>
    <p className="auth-switch">New to DecorAI? <Link to="/signup">Create an account</Link></p>
  </AuthPage>
}

function AuthPage({title,subtitle,children}){
  return <main className="auth-layout"><section className="auth-image"><img src="https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1500&q=90" alt="Elegant interior"/><div className="auth-image-copy"><span>DECORAI</span><h1>A better room starts with a better idea.</h1></div></section><section className="auth-panel"><div className="auth-box"><Logo/><div className="auth-heading"><span className="eyebrow">YOUR PRIVATE STUDIO</span><h2>{title}</h2><p>{subtitle}</p></div>{children}</div></section></main>
}
