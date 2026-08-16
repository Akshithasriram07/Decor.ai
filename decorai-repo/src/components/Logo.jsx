import { Link } from "react-router-dom";

export default function Logo({ light=false }) {
  return (
    <Link className={`logo ${light ? "logo-light" : ""}`} to="/">
      <span className="logo-symbol">
        <svg viewBox="0 0 40 40" aria-hidden="true">
          <path d="M7 19.5 20 8l13 11.5" fill="none" stroke="currentColor" strokeWidth="1.7"/>
          <path d="M11 18.5V31h18V18.5M16 31V22h8v9" fill="none" stroke="currentColor" strokeWidth="1.7"/>
          <path d="M25.5 10.5c2.8-3.2 6.5-2.6 7.1.4-2.8.9-5 1-7.1-.4Z" fill="currentColor"/>
        </svg>
      </span>
      <span><b>Decor</b><i>AI</i></span>
    </Link>
  );
}
