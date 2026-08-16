import { createContext, useContext, useMemo, useState } from "react";

const DesignContext = createContext(null);
const KEY = "decorai-designs-v2";

const starterDesigns = [
  {
    id: "warm-modern",
    title: "Warm Modern",
    room: "Living Room",
    style: "Warm Modern",
    image: "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1400&q=85",
    saved: true
  },
  {
    id: "quiet-luxury",
    title: "Quiet Luxury",
    room: "Bedroom",
    style: "Quiet Luxury",
    image: "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1400&q=85",
    saved: true
  }
];

export function DesignProvider({ children }) {
  const [designs, setDesigns] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(KEY));
      return saved?.length ? saved : starterDesigns;
    } catch {
      return starterDesigns;
    }
  });

  const [savedProducts, setSavedProducts] = useState(() => {
    try { return JSON.parse(localStorage.getItem("decorai-wishlist-v2")) || []; }
    catch { return []; }
  });

  const saveDesign = (design) => {
    setDesigns(prev => {
      const next = [{ ...design, saved: true }, ...prev.filter(x => x.id !== design.id)];
      localStorage.setItem(KEY, JSON.stringify(next));
      return next;
    });
  };

  const toggleProduct = (product) => {
    setSavedProducts(prev => {
      const exists = prev.some(x => x.id === product.id);
      const next = exists ? prev.filter(x => x.id !== product.id) : [...prev, product];
      localStorage.setItem("decorai-wishlist-v2", JSON.stringify(next));
      return next;
    });
  };

  const value = useMemo(() => ({
    designs, saveDesign, savedProducts, toggleProduct
  }), [designs, savedProducts]);

  return <DesignContext.Provider value={value}>{children}</DesignContext.Provider>;
}

export const useDesigns = () => useContext(DesignContext);
