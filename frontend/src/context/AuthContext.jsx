import { createContext,useContext,useEffect,useMemo,useState } from "react";
import { api } from "../lib/api";
const AuthContext=createContext(null);

export function AuthProvider({children}){
  const [user,setUser]=useState(()=>{try{return JSON.parse(localStorage.getItem("decorai-user-v3"))||null}catch{return null}});
  const [loading,setLoading]=useState(Boolean(localStorage.getItem("decorai-token-v3")));

  useEffect(()=>{ if(user)localStorage.setItem("decorai-user-v3",JSON.stringify(user)); else localStorage.removeItem("decorai-user-v3"); },[user]);
  useEffect(()=>{ (async()=>{ if(!localStorage.getItem("decorai-token-v3")) return setLoading(false); try{setUser(await api("/api/auth/me"))}catch{localStorage.removeItem("decorai-token-v3");setUser(null)} finally{setLoading(false)} })() },[]);

  const signUp=async(form)=>api("/api/auth/signup",{method:"POST",body:JSON.stringify(form)});
  const verifyEmail=async(email,code)=>api("/api/auth/verify-email",{method:"POST",body:JSON.stringify({email,code})});
  const resendVerification=async(email)=>api("/api/auth/resend-verification",{method:"POST",body:JSON.stringify({email})});
  const signIn=async(form)=>{const data=await api("/api/auth/signin",{method:"POST",body:JSON.stringify(form)});localStorage.setItem("decorai-token-v3",data.access_token);setUser(data.user);return data.user};
  const demoSignIn=async()=>{const data=await api("/api/auth/demo-signin",{method:"POST"});localStorage.setItem("decorai-token-v3",data.access_token);setUser(data.user);return data.user};
  const forgotPassword=async(email)=>api("/api/auth/forgot-password",{method:"POST",body:JSON.stringify({email})});
  const resetPassword=async(payload)=>api("/api/auth/reset-password",{method:"POST",body:JSON.stringify(payload)});
  const updateUser=async(updates)=>{const next=await api("/api/users/me",{method:"PUT",body:JSON.stringify(updates)});setUser(next);return next};
  const signOut=()=>{localStorage.removeItem("decorai-token-v3");setUser(null)};
  const value=useMemo(()=>({user,setUser,loading,signUp,verifyEmail,resendVerification,signIn,demoSignIn,forgotPassword,resetPassword,updateUser,signOut,isAuthenticated:Boolean(user)}),[user,loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
export const useAuth=()=>useContext(AuthContext);
