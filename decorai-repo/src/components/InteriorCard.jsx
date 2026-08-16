import { motion } from "framer-motion";

export default function InteriorCard({ item, tall=false }) {
  return (
    <motion.article
      className={`interior-card ${tall ? "tall" : ""}`}
      whileHover={{ y:-5 }}
      transition={{ duration:.25 }}
    >
      <img src={item.image} alt={item.title}/>
      <div className="image-shade"/>
      <div className="interior-card-copy">
        <span>{item.room}</span>
        <h3>{item.title}</h3>
        <small>{item.style}</small>
      </div>
    </motion.article>
  );
}
