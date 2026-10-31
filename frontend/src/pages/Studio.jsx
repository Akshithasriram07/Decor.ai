import {useRef,useState} from "react";
import {Upload,Lock,FileText,Sparkles,CheckCircle2,Eye,AlertCircle,Palette,ArrowRight} from "lucide-react";
import AppShell from "../components/AppShell";
import {api} from "../lib/api";

const styles=["Warm Modern","Quiet Luxury","Japandi","Contemporary","Minimal","Organic","Modern Indian","Indian Contemporary","Kerala Traditional","Chettinad Heritage","Rajasthani Haveli","South Indian Minimal"];
const rooms=["Living Room","Bedroom","Kitchen","Dining","Home Office","Bathroom","Puja Room","Balcony"];

export default function Studio(){
 const inputRef=useRef();
 const [file,setFile]=useState(null),[image,setImage]=useState(""),[room,setRoom]=useState("Living Room"),[style,setStyle]=useState("Warm Modern"),[prompt,setPrompt]=useState("");
 const [analysis,setAnalysis]=useState(null),[busy,setBusy]=useState(false),[error,setError]=useState("");
 const onUpload=e=>{const f=e.target.files?.[0];if(f){setFile(f);setImage(URL.createObjectURL(f));setAnalysis(null);setError("")}};
 const analyze=async()=>{
   if(!file)return setError("Upload a room photo first.");
   setBusy(true);setError("");
   try{
     const fd=new FormData();fd.append("image",file);fd.append("room",room);fd.append("style",style);fd.append("prompt",prompt);
     const d=await api("/api/designs/analyze",{method:"POST",body:fd});setAnalysis(d);
   }catch(err){setError(err.message)}finally{setBusy(false)}
 };
 return <AppShell title="AI Design Studio" eyebrow="CREATE YOUR SPACE">
  <div className="studio-grid studio-grid-pro">
   <section className="studio-controls card">
    <div className="studio-panel-heading"><div><span className="eyebrow">YOUR INPUT</span><h2>Design brief</h2></div><span className="studio-free-badge">Free analysis</span></div>

    <Step n="01" title="Room photo" text="Upload the actual room. Gemini will analyse the visible space, not just the selected room label."/>
    <button className="upload-zone studio-upload" onClick={()=>inputRef.current?.click()}>
      <input ref={inputRef} hidden type="file" accept="image/jpeg,image/png,image/webp" onChange={onUpload}/>
      {image?<><img src={image} alt="Uploaded room"/><span className="upload-change">Change photo</span></>:<><Upload size={23}/><b>Upload your room</b><span>JPG, PNG or WEBP · up to 10 MB</span></>}
    </button>

    <Step n="02" title="Room type" text="Use this as context; the uploaded image remains the primary source for visual understanding."/>
    <div className="choice-grid studio-choice-grid">{rooms.map(x=><button type="button" key={x} className={room===x?"choice active":"choice"} onClick={()=>setRoom(x)}>{x}</button>)}</div>

    <Step n="03" title="Design direction" text="Choose the visual language for the recommendations."/>
    <div className="style-grid studio-style-grid">{styles.map(x=><button type="button" key={x} className={style===x?"style-choice active":"style-choice"} onClick={()=>setStyle(x)}><b>{x}</b><span>{styleDescription(x)}</span></button>)}</div>

    <label className="prompt-field"><span>What should we consider?</span><textarea value={prompt} onChange={e=>setPrompt(e.target.value)} placeholder="Example: keep the sofa, add warmer lighting and more storage…"/></label>
    {error&&<p className="form-error studio-error">{error}</p>}
    <button className="button dark full generate studio-analyse-button" onClick={analyze} disabled={busy}><FileText size={17}/>{busy?"Analysing the actual room…":"Analyse room & get suggestions"}</button>
   </section>

   <section className="studio-result studio-result-pro">
    <div className="studio-locked-strip"><div className="studio-lock-icon"><Lock size={15}/></div><div><b>AI image generation</b><span>Upgrade to unlock</span></div><span className="studio-lock-note">Locked</span></div>

    <div className="result-top studio-result-top"><div><span className="eyebrow">AI DESIGN ASSISTANT</span><h2>{analysis?.title||"Your room, understood"}</h2><p className="studio-result-subtitle">DecorAI reads the uploaded image first, then turns what it sees and what you asked for into practical modifications.</p></div><span className="result-status">{analysis?<><CheckCircle2 size={12}/> Analysis ready</>:"Free analysis"}</span></div>

    <div className="analysis-preview studio-analysis-preview">{image?<img src={image} alt="Room submitted for analysis"/>:<div className="generation-state"><div className="generation-orb"><Sparkles/></div><b>Start with your room</b><span>Upload a photo and DecorAI will understand the existing space before suggesting changes.</span></div>}</div>

    <div className="analysis-copy studio-analysis-copy">
      <div className="analysis-copy-head"><div><span className="eyebrow">TEXT ANALYSIS</span><h2>Room analysis & modifications</h2></div>{analysis&&<span className="result-status"><CheckCircle2 size={12}/> AI analysed the image</span>}</div>
      {analysis? <>
        <p className="analysis-summary">{analysis.summary}</p>
        {analysis.caption&&<div className="analysis-observation"><span><Eye size={11}/> WHAT DECORAI SEES</span><p>{analysis.caption}</p></div>}
        <div className="studio-insight-grid">
          <Insight icon={<CheckCircle2/>} title="What's working" items={analysis.strengths||[]}/>
          <Insight icon={<AlertCircle/>} title="Areas to improve" items={analysis.improvements||[]}/>
          <Insight icon={<Palette/>} title="Design direction" items={analysis.style_notes||[`${analysis.style} direction`]}/>
        </div>
        <div className="studio-modification-head"><div><span className="eyebrow">PERSONALISED PLAN</span><h3>Modification suggestions</h3></div><span>{analysis.suggestions?.length||0} recommendations</span></div>
        <div className="suggestion-list studio-suggestion-list">{(analysis.suggestions||[]).map((s,i)=><article key={i}><span>{String(i+1).padStart(2,"0")}</span><div><b>{s.title}</b><p>{s.detail}</p></div><ArrowRight size={15}/></article>)}</div>
      </>:<div className="analysis-empty studio-analysis-empty"><FileText size={21}/><div><b>Your personalised modifications will appear here</b><p>After analysis, DecorAI will explain what is actually visible in the room and give specific changes for your selected style and requirements.</p></div></div>}
    </div>
   </section>
  </div>
  <div className="studio-note"><Sparkles size={17}/><span>Free: image understanding and written recommendations. AI image generation stays locked until an image-generation provider is configured.</span></div>
 </AppShell>
}
function Insight({icon,title,items}){return <div className="studio-insight-card"><div className="studio-insight-title">{icon}<b>{title}</b></div>{items?.length?<ul>{items.slice(0,4).map((item,i)=><li key={i}>{item}</li>)}</ul>:<p>No additional points returned.</p>}</div>}
function Step({n,title,text}){return <div className="studio-step"><span>{n}</span><div><b>{title}</b><small>{text}</small></div></div>}
function styleDescription(x){return ({"Warm Modern":"soft oak · linen · layered light","Quiet Luxury":"stone · brass · tailored neutrals","Japandi":"calm woods · tactile minimalism","Contemporary":"clean geometry · refined contrast","Minimal":"quiet palette · essential forms","Organic":"natural textures · earthy softness","Modern Indian":"teak · brass · warm neutral textiles","Indian Contemporary":"clean lines · Indian craft accents","Kerala Traditional":"wood · cane · earthy heritage details","Chettinad Heritage":"rich wood · patterned craft · brass","Rajasthani Haveli":"warm plaster · carved wood · artisan colour","South Indian Minimal":"quiet neutrals · wood · local craft"})[x]||"balanced materials · practical styling"}
