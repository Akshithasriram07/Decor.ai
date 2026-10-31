from app.db.session import Base, SessionLocal, engine
from app.models import Product, Worker, Design, User
from app.core.security import hash_password
from app.core.config import settings
from sqlalchemy import select

# Catalog is deliberately deterministic and idempotent: running seed.py repeatedly updates
# existing records instead of trying to insert duplicate primary keys.
PRODUCTS = [
("prod-01","Ivory Curve Sofa","Furniture",24999,"https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=90"),
("prod-02","Linen Cloud Sofa","Furniture",32990,"https://images.unsplash.com/photo-1550226891-ef816aed4a98?auto=format&fit=crop&w=1200&q=90"),
("prod-03","Oak Side Table","Furniture",11900,"https://images.unsplash.com/photo-1532372320572-cda25653a26d?auto=format&fit=crop&w=1200&q=90"),
("prod-04","Linen Accent Chair","Furniture",13990,"https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=1200&q=90"),
("prod-05","Walnut Console","Furniture",18990,"https://images.unsplash.com/photo-1551298370-9d3d53740c72?auto=format&fit=crop&w=1200&q=90"),
("prod-06","Cane Lounge Chair","Furniture",16490,"https://images.unsplash.com/photo-1567016432779-094069958ea5?auto=format&fit=crop&w=1200&q=90"),
("prod-07","Minimal TV Console","Furniture",22990,"https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=1200&q=90"),
("prod-08","Round Marble Coffee Table","Furniture",21990,"https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=1200&q=90"),
("prod-09","Oak Dining Table","Furniture",28990,"https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=90"),
("prod-10","Boucle Dining Chair","Furniture",7990,"https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=1200&q=90"),
("prod-11","Rattan Bar Stool","Furniture",6490,"https://images.unsplash.com/photo-1592078615290-033ee584e267?auto=format&fit=crop&w=1200&q=90"),
("prod-12","Compact Study Desk","Furniture",10990,"https://images.unsplash.com/photo-1518455027359-f3f8164ba6b1?auto=format&fit=crop&w=1200&q=90"),
("prod-13","Brass Arc Floor Lamp","Lighting",8490,"https://images.unsplash.com/photo-1540932239986-30128078f3c5?auto=format&fit=crop&w=1200&q=90"),
("prod-14","Stone Table Lamp","Lighting",5490,"https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=90"),
("prod-15","Opal Globe Pendant","Lighting",6990,"https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?auto=format&fit=crop&w=1200&q=90"),
("prod-16","Linear Dining Pendant","Lighting",9990,"https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=1200&q=90"),
("prod-17","Warm Wall Sconce","Lighting",4290,"https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1200&q=90"),
("prod-18","Paper Lantern Floor Light","Lighting",7290,"https://images.unsplash.com/photo-1513501170-6a5a6c1c0e47?auto=format&fit=crop&w=1200&q=90"),
("prod-19","Textured Ceramic Vase","Decor",2190,"https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=90"),
("prod-20","Travertine Tray","Decor",2890,"https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=90"),
("prod-21","Handloom Cushion Set","Decor",2490,"https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=1200&q=90"),
("prod-22","Neutral Area Rug","Decor",8990,"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=90"),
("prod-23","Abstract Wall Art","Decor",3990,"https://images.unsplash.com/photo-1577083288073-40892c0860a4?auto=format&fit=crop&w=1200&q=90"),
("prod-24","Terracotta Planter","Decor",1590,"https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=1200&q=90"),
("prod-25","Brass Urli Bowl","Decor",3490,"https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=1200&q=90"),
("prod-26","Wooden Mirror","Decor",5990,"https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=90"),
("prod-27","Fluted Bedside Table","Furniture",12990,"https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=90"),
("prod-28","Upholstered Bed","Furniture",34990,"https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=90"),
("prod-29","Floating Bedside Shelf","Furniture",4290,"https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=90"),
("prod-30","Arched Full-Length Mirror","Decor",8490,"https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=90"),
("prod-31","Marble Basin Stand","Furniture",11990,"https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1200&q=90"),
("prod-32","Brass Bathroom Shelf","Decor",3290,"https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=90"),
("prod-33","Cotton Bath Mat","Decor",1290,"https://images.unsplash.com/photo-1584622781867-7f8a0a8c3f22?auto=format&fit=crop&w=1200&q=90"),
("prod-34","Oak Pooja Console","Furniture",15990,"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=90"),
("prod-35","Carved Brass Diya Set","Decor",1890,"https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=1200&q=90"),
("prod-36","Cane Balcony Chair","Furniture",7990,"https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=90"),
("prod-37","Outdoor Side Table","Furniture",4990,"https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=1200&q=90"),
("prod-38","Indoor Olive Tree","Decor",3990,"https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1200&q=90"),
("prod-39","Jute Pendant","Lighting",5890,"https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?auto=format&fit=crop&w=1200&q=90"),
("prod-40","Fluted Ceramic Lamp","Lighting",4790,"https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=90"),
("prod-41","Indian Handloom Throw","Decor",3290,"https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1200&q=90"),
("prod-42","Teak Bench","Furniture",14990,"https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=90"),
("prod-43","Statement Pendant Cluster","Lighting",12990,"https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=1200&q=90"),
("prod-44","Sculptural Ceramic Set","Decor",2790,"https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=90"),
("prod-45","Compact Accent Ottoman","Furniture",6990,"https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=1200&q=90"),
("prod-46","Minimal Bookshelf","Furniture",9990,"https://images.unsplash.com/photo-1594620302200-9a762244a156?auto=format&fit=crop&w=1200&q=90"),
("prod-47","Linen Curtains","Decor",5490,"https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?auto=format&fit=crop&w=1200&q=90"),
("prod-48","DecorAI Signature Mirror","Decor",7490,"https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=90"),
]

EXPLORE = [
("catalog-explore-01","Warm Modern Indian Hall","Living Room","Modern Indian","https://images.unsplash.com/photo-1600607688969-a5bfcd646154?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-02","Quiet Luxury Living","Living Room","Quiet Luxury","https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-03","Contemporary Family Living","Living Room","Contemporary","https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-04","Soft Neutral Bedroom","Bedroom","Minimal","https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-05","Warm Textured Bedroom","Bedroom","Warm Modern","https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-06","Modern Indian Bedroom","Bedroom","Indian Contemporary","https://images.unsplash.com/photo-1617104678098-de229db51175?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-07","Stone & Oak Kitchen","Kitchen","Contemporary","https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-08","Bright Minimal Kitchen","Kitchen","Minimal","https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-09","Indian Wood Kitchen","Kitchen","Modern Indian","https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-10","Calm Spa Bathroom","Bathroom","Quiet Luxury","https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-11","Warm Modern Bathroom","Bathroom","Warm Modern","https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-12","Minimal Marble Bathroom","Bathroom","Minimal","https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-13","Natural Wood Dining","Dining","Warm Modern","https://images.unsplash.com/photo-1745794621090-d856c53b0cc2?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-14","Elegant Contemporary Dining","Dining","Contemporary","https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-15","Japandi Home Office","Home Office","Japandi","https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-16","Minimal Study Room","Home Office","Minimal","https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1800&q=90"),
("catalog-explore-17","Backlit Indian Puja Room","Puja Room","Indian Contemporary","https://img.interiorcompany.com/interior/webproduct/white-and-wood-modern-pooja-room-design-with-backlit-jali-and-matte-finish-cabinets-img.png?aio=w-768%3B"),
("catalog-explore-18","Traditional Puja Corner","Puja Room","Traditional Indian","https://img.staticmb.com/mbcontent/images/crop/uploads/ver2/XIwvQlc61t8ZIpanz4mAnTU2nJ5n26mFArYGT8vnFhK-0w/Glass-Enclosed-Serenity-Pooja-Room-Design_0_1200.jpg"),
("catalog-explore-19","Urban Balcony Lounge","Balcony","Contemporary","https://www.proiectari.md/wp-content/uploads/2024/01/balcoane-moderne-3.jpg"),
("catalog-explore-20","Green Balcony Retreat","Balcony","Organic","https://aderadizain.com/product_images/tiara_twinmax_photo_01.webp"),
("catalog-explore-21","Pastel Kids Bedroom","Kids Room","Modern","https://www.rehome.com.tr/cdn/shop/articles/blog-cover_fdf5aeb8-e68a-4cb5-a856-60fedaf9539c.jpg?v=1777021158"),
("catalog-explore-22","Playful Kids Room","Kids Room","Organic","https://casolia.com/wp-content/uploads/2025/01/image0_cool-kids-bedroom-ideas_cool-kids-bedroom-ideas-1024x683.jpg"),
("catalog-explore-23","Warm Wood Entryway","Entryway","Warm Modern","https://cdn6.ep.dynamics.net/s3/rw-propertyimages/4b08-H3464974-188652549__1771904805-71777-163ALandells008.jpg?format=jpg&maxheight=2841&maxwidth=2841&quality=90&scale=down"),
("catalog-explore-24","Panoramic Villa Lounge","Villa","Luxury","https://storage.googleapis.com/ic-property-thumb/BZJAAP1758_51083_1300_V0_82EB.jpg"),
]


WORKERS = [
("worker-01","Ravi Kumar","Carpenter","Guntur",4.8,120,"https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=700&q=90"),
("worker-02","Sandeep Painters","Painter","Vijayawada",4.9,180,"https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=700&q=90"),
("worker-03","Ananya Interiors","Interior Designer","Hyderabad",5.0,74,"https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=700&q=90"),
("worker-04","Kiran Electricals","Electrician","Vijayawada",4.7,95,"https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=700&q=90"),
("worker-05","Meera Woodworks","Carpenter","Hyderabad",4.9,142,"https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=700&q=90"),
("worker-06","Arjun Space Studio","Interior Designer","Guntur",4.8,91,"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=700&q=90"),
]

def upsert(db, model, ident, values):
    item = db.get(model, ident)
    if item is None:
        item = model(id=ident, **values)
        db.add(item)
    else:
        for key, value in values.items():
            setattr(item, key, value)
    return item

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # System account is never exposed as a real login account.
        system = upsert(db, User, "system", {
            "name":"DecorAI","email":"system@decorai.com","password_hash":hash_password("system-seed-only"),
            "email_verified":True,"role":"system","plan":"System","location":"India"
        })

        admin_email = settings.admin_email.lower().strip()
        admin = db.scalar(select(User).where(User.email == admin_email))
        if not admin:
            admin = User(id="admin",name="DecorAI Admin",email=admin_email,password_hash=hash_password(settings.admin_password),
                         email_verified=True,role="admin",plan="Admin",location="India")
            db.add(admin)
        else:
            admin.role="admin"; admin.email_verified=True

        demo = db.get(User, "demo-user") or db.scalar(select(User).where(User.email == "demo@decorai.com"))
        legacy = db.scalar(select(User).where(User.email == "demo@decorai.local"))
        if demo is None:
            demo = User(id="demo-user",name="Demo User",email="demo@decorai.com",password_hash=hash_password("DemoOnly123!"),
                        email_verified=True,role="user",plan="Free",location="India")
            db.add(demo)
        else:
            demo.email="demo@decorai.com"; demo.email_verified=True; demo.role="user"; demo.plan="Free"
        if legacy is not None and legacy.id != demo.id:
            # Keep the old row harmless but give it a valid response-safe email.
            legacy.email="legacy-demo@decorai.com"

        for ident,name,category,price,image in PRODUCTS:
            upsert(db, Product, ident, {"name":name,"category":category,"price":price,"image":image,
                "description":f"Curated {category.lower()} piece for premium residential interiors.",
                "brand":"DecorAI Select","rating":4.8,"available":True})

        for ident,name,role,location,rating,jobs,image in WORKERS:
            upsert(db, Worker, ident, {"name":name,"role":role,"location":location,"rating":rating,"jobs":jobs,"image":image,
                "description":f"Experienced {role.lower()} available for residential projects across {location}.",
                "phone":"+91 90000 00000","email":f"{ident}@decorai.com","available":True})

        for ident,title,room,style,image in EXPLORE:
            upsert(db, Design, ident, {"user_id":"system","title":title,"room":room,"style":style,"image":image,
                "status":"completed","is_public":True,
                "description":f"A full-room {style.lower()} {room.lower()} concept with layered materials, lighting and considered styling."})

        db.commit()
        print("DecorAI production catalog seeded successfully.")
        print(f"Products added/updated: {len(PRODUCTS)}")
        print(f"Explore designs added/updated: {len(EXPLORE)}")
        print(f"Local workers added/updated: {len(WORKERS)}")
        print("Demo account: demo@decorai.com")
        print("Demo password: DemoOnly123!")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
