import { useEffect, useState } from "react";
import { BarChart3, Check, Eye, EyeOff, Package, ShieldCheck, ShoppingBag, Users, X } from "lucide-react";
import { api } from "../lib/api";
import AppShell from "../components/AppShell";

const money = (v) => `₹${Number(v || 0).toLocaleString("en-IN")}`;

export default function Admin() {
  const [overview, setOverview] = useState(null);
  const [users, setUsers] = useState([]);
  const [designs, setDesigns] = useState([]);
  const [orders, setOrders] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [applications, setApplications] = useState([]);
  const [tab, setTab] = useState("overview");
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const [o,u,d,ord,w,a] = await Promise.all([
        api("/api/admin/overview"), api("/api/admin/users"), api("/api/admin/designs"),
        api("/api/admin/orders"), api("/api/admin/workers"), api("/api/admin/worker-applications")
      ]);
      setOverview(o); setUsers(u); setDesigns(d); setOrders(ord); setWorkers(w); setApplications(a);
      setError("");
    } catch (e) { setError(e.message); }
  };
  useEffect(() => { load(); }, []);

  const toggleDesign = async (id, publicValue) => { await api(`/api/admin/designs/${id}/visibility?public=${!publicValue}`, {method:"PATCH"}); await load(); };
  const setOrder = async (id, status) => { await api(`/api/admin/orders/${id}/status?status=${encodeURIComponent(status)}`, {method:"PATCH"}); await load(); };
  const setWorker = async (id, value) => { await api(`/api/admin/workers/${id}/availability?available=${value}`, {method:"PATCH"}); await load(); };
  const setApplication = async (id, status) => { await api(`/api/admin/worker-applications/${id}?status=${status}`, {method:"PATCH"}); await load(); };

  return <AppShell title="Admin Control Center" eyebrow="DECORAI ADMIN">
    <div className="admin-hero card">
      <div><span className="eyebrow">OPERATIONS</span><h2>Keep every part of DecorAI moving.</h2><p>Manage members, designs, commerce, workers and moderation from one calm workspace.</p></div>
      <ShieldCheck size={48}/>
    </div>
    {error && <div className="form-error">{error}</div>}
    {overview && <div className="admin-stats">
      <Stat icon={Users} label="Users" value={overview.users}/><Stat icon={BarChart3} label="Designs" value={overview.designs}/>
      <Stat icon={ShoppingBag} label="Orders" value={overview.orders}/><Stat icon={Package} label="Revenue" value={money(overview.revenue)}/>
    </div>}
    <div className="admin-tabs">{[["overview","Overview"],["users","Users"],["designs","Designs"],["orders","Orders"],["workers","Workers"],["applications","Applications"]].map(([id,label])=><button className={tab===id?"admin-tab active":"admin-tab"} onClick={()=>setTab(id)} key={id}>{label}</button>)}</div>
    <div className="admin-panel card">
      {tab === "overview" && overview && <div className="admin-overview-grid">
        <Metric label="Verified users" value={overview.verified_users}/><Metric label="Public designs" value={overview.public_designs}/><Metric label="Products" value={overview.products}/><Metric label="Active workers" value={overview.workers}/><Metric label="Pending worker applications" value={overview.pending_worker_applications}/><Metric label="Paid orders" value={overview.paid_orders}/>
      </div>}
      {tab === "users" && <Table headers={["Name","Email","Role","Verified","Joined"]}>{users.map(x=><tr key={x.id}><td>{x.name}</td><td>{x.email}</td><td><Badge>{x.role}</Badge></td><td>{x.verified?"Yes":"No"}</td><td>{new Date(x.created_at).toLocaleDateString()}</td></tr>)}</Table>}
      {tab === "designs" && <Table headers={["Design","Room","Style","Public","Action"]}>{designs.map(x=><tr key={x.id}><td>{x.title}</td><td>{x.room}</td><td>{x.style}</td><td><Badge>{x.public?"Public":"Private"}</Badge></td><td><button className="icon-button" title="Toggle visibility" onClick={()=>toggleDesign(x.id,x.public)}>{x.public?<EyeOff size={15}/>:<Eye size={15}/>}</button></td></tr>)}</Table>}
      {tab === "orders" && <Table headers={["Order","Customer","Amount","Status","Update"]}>{orders.map(x=><tr key={x.id}><td>{x.id.slice(0,8)}</td><td>{x.shipping_name}</td><td>{money(x.total)}</td><td><Badge>{x.status}</Badge></td><td><select className="admin-select" value={x.status} onChange={e=>setOrder(x.id,e.target.value)}><option>pending</option><option>paid</option><option>processing</option><option>shipped</option><option>delivered</option><option>cancelled</option></select></td></tr>)}</Table>}
      {tab === "workers" && <Table headers={["Worker","Role","Location","Rating","Available"]}>{workers.map(x=><tr key={x.id}><td>{x.name}</td><td>{x.role}</td><td>{x.location}</td><td>{x.rating}</td><td><button className="status-toggle" onClick={()=>setWorker(x.id,!x.available)}>{x.available?<><Check size={13}/> Available</>:<><X size={13}/> Offline</>}</button></td></tr>)}</Table>}
      {tab === "applications" && <Table headers={["Applicant","Role","Location","Experience","Status","Review"]}>{applications.map(x=><tr key={x.id}><td>{x.user_id.slice(0,8)}</td><td>{x.role}</td><td>{x.location}</td><td>{x.experience}</td><td><Badge>{x.status}</Badge></td><td>{x.status==="pending"&&<div className="admin-actions"><button className="button dark" onClick={()=>setApplication(x.id,"approved")}>Approve</button><button className="button outline" onClick={()=>setApplication(x.id,"rejected")}>Reject</button></div>}</td></tr>)}</Table>}
    </div>
  </AppShell>;
}

function Stat({icon:Icon,label,value}){return <div className="stat-card"><Icon size={16}/><span>{label}</span><strong>{value}</strong></div>}
function Metric({label,value}){return <div className="admin-metric"><span>{label}</span><b>{value}</b></div>}
function Badge({children}){return <span className="admin-badge">{children}</span>}
function Table({headers,children}){return <div className="admin-table-wrap"><table className="admin-table"><thead><tr>{headers.map(h=><th key={h}>{h}</th>)}</tr></thead><tbody>{children}</tbody></table></div>}
