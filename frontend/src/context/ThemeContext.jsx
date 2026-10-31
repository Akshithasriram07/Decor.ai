import {createContext,useContext,useEffect,useMemo,useState} from "react";

const ThemeContext=createContext(null);

export function ThemeProvider({children}){
  const [theme,setTheme]=useState(()=>localStorage.getItem("decorai-theme")||"light");
  useEffect(()=>{
    document.documentElement.dataset.theme=theme;
    localStorage.setItem("decorai-theme",theme);
  },[theme]);
  const toggleTheme=()=>setTheme(t=>t==="light"?"dark":"light");
  const value=useMemo(()=>({theme,setTheme,toggleTheme}),[theme]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
export const useTheme=()=>useContext(ThemeContext);
