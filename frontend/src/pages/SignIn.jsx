import {useState} from "react"; import {Link,useLocation,useNavigate} from "react-router-dom"; import Logo from "../components/Logo"; import {useAuth} from "../context/AuthContext";
export default function SignIn(){
 const {signIn,demoSignIn}=useAuth(), nav=useNavigate(), loc=useLocation(); const [form,setForm]=useState({email:"",password:""}); const [error,setError]=useState("");
 async function submit(e){e.preventDefault();setError("");try{await signIn(form);nav(loc.state?.from||"/app",{replace:true})}catch(err){setError(err.message)}}
 return <AuthPage title="Welcome back" subtitle="Continue creating spaces that feel like home."><form className="auth-form" onSubmit={submit}>
  <label>Email<input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="you@example.com"/></label>
  <label>Password<input type="password" required value={form.password} onChange={e=>setForm({...form,password:e.target.value})} placeholder="Your password"/></label>
  <div className="auth-row"><span></span><Link className="plain-link" to="/forgot-password">Forgot password?</Link></div>
  {error&&<p className="form-error">{error}</p>}<button className="button dark full">Sign in</button>
  <div className="auth-divider"><span>or</span></div>
  <button type="button" className="button light full" onClick={async()=>{setError("");try{await demoSignIn();nav(loc.state?.from||"/app",{replace:true})}catch(err){setError(err.message)}}}>Continue with Demo Account</button>
 </form><p className="auth-switch">New to DecorAI? <Link to="/signup">Create an account</Link></p></AuthPage>
}
function AuthPage({title,subtitle,children}){return <main className="auth-layout"><section className="auth-image"><img src="https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1500&q=90"/><div className="auth-image-copy"><span>DECORAI</span><h1>A better room starts with a better idea.</h1></div></section><section className="auth-panel"><div className="auth-box"><Logo/><div className="auth-heading"><span className="eyebrow">YOUR PRIVATE STUDIO</span><h2>{title}</h2><p>{subtitle}</p></div>{children}</div></section></main>}
