import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { Upload, Sparkles, Save, RotateCcw, ArrowRight } from "lucide-react";
import AppShell from "../components/AppShell";
import { useDesigns } from "../context/DesignContext";

const styles=["Warm Modern","Quiet Luxury","Japandi","Contemporary","Minimal","Organic"];
const rooms=["Living Room","Bedroom","Kitchen","Dining","Home Office","Bathroom"];

export default function Studio(){
  const inputRef=useRef(); const {saveDesign}=useDesigns();
  const [image,setImage]=useState(""); const [room,setRoom]=useState("Living Room"); const [style,setStyle]=useState("Warm Modern"); const [status,setStatus]=useState("ready"); const [result,setResult]=useState(null);

  const onUpload=e=>{const f=e.target.files?.[0]; if(f) setImage(URL.createObjectURL(f));};
  const generate=()=>{
    setStatus("analyzing");
    setTimeout(()=>setStatus("composing"),900);
    setTimeout(()=>{
      const concept = {id:crypto.randomUUID(),title:style,room,style,image:image||"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1400&q=90",saved:true};
      setResult(concept);setStatus("done");
    },2200);
  };
  const save=()=>{if(result)saveDesign(result)};
  return <AppShell title="AI Design Studio" eyebrow="CREATE YOUR SPACE">
    <div className="studio-grid">
      <section className="studio-controls card">
        <Step n="01" title="Room photo" text="Start with a clear view of the space."/>
        <button className="upload-zone" onClick={()=>inputRef.current?.click()}>
          <input ref={inputRef} hidden type="file" accept="image/*" onChange={onUpload}/>
          {image?<img src={image} alt="Uploaded room"/>:<><Upload size={22}/><b>Upload your room</b><span>JPG or PNG · up to 10 MB</span></>}
        </button>
        <Step n="02" title="Room type" text="Tell us what we're designing."/>
        <div className="choice-grid">{rooms.map(x=><button key={x} className={room===x?"choice active":"choice"} onClick={()=>setRoom(x)}>{x}</button>)}</div>
        <Step n="03" title="Design direction" text="Choose the feeling you want."/>
        <div className="style-grid">{styles.map(x=><button key={x} className={style===x?"style-choice active":"style-choice"} onClick={()=>setStyle(x)}><b>{x}</b><span>{styleDescription(x)}</span></button>)}</div>
        <button className="button dark full generate" onClick={generate} disabled={status==="analyzing"||status==="composing"}><Sparkles size={16}/>{status==="ready"?"Generate concept":status==="done"?"Generate another":status==="analyzing"?"Analyzing room…":"Composing your concept…"}</button>
      </section>

      <section className="studio-result">
        <div className="result-top"><div><span className="eyebrow">AI CONCEPT</span><h2>{result?.title||"Your next room"}</h2></div><span className="result-status">{status==="done"?"Concept ready":"Ready"}</span></div>
        <div className="result-canvas">
          {status==="analyzing"||status==="composing" ? <GenerationState step={status}/> :
           <motion.img key={result?.id||"default"} initial={{opacity:0,scale:1.04}} animate={{opacity:1,scale:1}} transition={{duration:.8}} src={result?.image||"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1500&q=90"} alt="AI interior concept"/>}
        </div>
        <div className="result-meta"><div><b>{result?.style||"Warm Modern"}</b><span>{result?.room||"Living Room"} · natural textures · layered light</span></div><div className="result-actions"><button className="icon-button" onClick={()=>setResult(null)} title="Reset"><RotateCcw size={17}/></button><button className="button outline" disabled={!result} onClick={save}><Save size={15}/> Save</button></div></div>
      </section>
    </div>
    <div className="studio-note"><Sparkles size={17}/><span>Production connection point: replace the generation function with your FastAPI/image-generation endpoint when the backend is ready.</span><ArrowRight size={15}/></div>
  </AppShell>
}
function Step({n,title,text}){return <div className="studio-step"><span>{n}</span><div><b>{title}</b><small>{text}</small></div></div>}
function styleDescription(x){return ({'Warm Modern':'Natural wood and soft neutrals','Quiet Luxury':'Stone, linen and refined detail','Japandi':'Calm forms and tactile materials','Contemporary':'Clean lines and statement pieces','Minimal':'Clarity, light and restraint','Organic':'Earth tones and natural texture'})[x]}
function GenerationState({step}){return <div className="generation-state"><motion.div className="generation-orb" animate={{scale:[1,1.15,1],rotate:360}} transition={{duration:2.4,repeat:Infinity,ease:"easeInOut"}}><Sparkles/></motion.div><b>{step==="analyzing"?"Understanding your room":"Composing your design"}</b><span>{step==="analyzing"?"Mapping light, proportions and existing space.":"Applying the selected style and visual language."}</span><div className="generation-bar"><motion.i initial={{width:"8%"}} animate={{width:"92%"}} transition={{duration:1.8}}/></div></div>}
