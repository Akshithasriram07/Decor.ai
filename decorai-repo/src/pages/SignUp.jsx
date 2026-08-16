import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Logo from "../components/Logo";
import { useAuth } from "../context/AuthContext";

export default function SignUp(){
  const {signUp}=useAuth(), navigate=useNavigate();
  const [form,setForm]=useState({name:"",email:"",password:"",confirm:""}), [error,setError]=useState("");
  async function submit(e){
    e.preventDefault();
    if(form.name.trim().length<2) return setError("Please enter your name.");
    if(form.password.length<6) return setError("Password must contain at least 6 characters.");
    if(form.password!==form.confirm) return setError("Passwords do not match.");
    await signUp(form); navigate("/app",{replace:true});
  }
  return <main className="auth-layout"><section className="auth-image"><img src="https://images.unsplash.com/photo-1600607688969-a5bfcd646154?auto=format&fit=crop&w=1500&q=90" alt="Refined interior"/><div className="auth-image-copy"><span>YOUR SPACE, YOUR STORY</span><h1>Design the feeling you want to come home to.</h1></div></section><section className="auth-panel"><div className="auth-box"><Logo/><div className="auth-heading"><span className="eyebrow">GET STARTED</span><h2>Create your studio</h2><p>Save designs, discover inspiration and build your dream home.</p></div><form className="auth-form" onSubmit={submit}><label>Full name<input value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="Your name"/></label><label>Email<input type="email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="you@example.com"/></label><label>Password<input type="password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} placeholder="At least 6 characters"/></label><label>Confirm password<input type="password" value={form.confirm} onChange={e=>setForm({...form,confirm:e.target.value})} placeholder="Repeat password"/></label>{error&&<p className="form-error">{error}</p>}<button className="button dark full">Create account</button></form><p className="auth-switch">Already have an account? <Link to="/signin">Sign in</Link></p></div></section></main>
}
