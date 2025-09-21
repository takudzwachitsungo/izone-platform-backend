# Vercel serverless handler
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app for Vercel (without lifespan to avoid issues)
app = FastAPI(
    title="iZonehub API",
    version="1.0.0",
    description="API for iZonehub Makerspace - Zimbabwe's innovation hub"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include ALL routers for full functionality
try:
    from routers import (
        auth, users, communities, projects, events, blog, store, 
        gallery, contact, upload, event_registrations, partners, team_members
    )
    
    # Include all routers
    app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
    app.include_router(users.router, prefix="/api/users", tags=["users"])
    app.include_router(communities.router, prefix="/api/communities", tags=["communities"])
    app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
    app.include_router(events.router, prefix="/api/events", tags=["events"])
    app.include_router(blog.router, prefix="/api/blog", tags=["blog"])
    app.include_router(store.router, prefix="/api/store", tags=["store"])
    app.include_router(gallery.router, prefix="/api/gallery", tags=["gallery"])
    app.include_router(contact.router, prefix="/api/contact", tags=["contact"])
    app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
    app.include_router(event_registrations.router, prefix="/api/event-registrations", tags=["event_registrations"])
    app.include_router(partners.router, prefix="/api/partners", tags=["partners"])
    app.include_router(team_members.router, prefix="/api/team-members", tags=["team_members"])
    
    # Add admin routes
    try:
        from routers.admin import dashboard, admin_events, admin_blog, admin_gallery, admin_projects, admin_store, admin_communities, admin_users, admin_partners, admin_team_members, admin_contact
        
        app.include_router(dashboard.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_events.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_blog.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_gallery.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_projects.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_store.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_communities.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_users.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_partners.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_team_members.router, prefix="/api/admin", tags=["admin"])
        app.include_router(admin_contact.router, prefix="/api/admin", tags=["admin"])
    except ImportError as e:
        print(f"Admin routes import error: {e}")
        
except ImportError as e:
    print(f"Router import error: {e}")

@app.get("/")
async def root():
    return {
        "message": "Welcome to iZonehub API - Full Functionality", 
        "status": "running",
        "environment": "vercel" if os.getenv("VERCEL") else "local",
        "features": ["Events", "Blog", "Store", "Gallery", "Communities", "Admin Panel", "QR Codes", "Excel Export"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working with full functionality!"}

# Initialize database for Vercel
if os.getenv("VERCEL"):
    try:
        from database import engine, Base
        from sqlalchemy.orm import sessionmaker
        from models import User, Event, BlogPost, Partner, TeamMember
        from auth import get_password_hash
        import datetime
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Create session and add test data
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if admin user exists
        try:
            admin_user = db.query(User).filter(User.email == "admin@izonedevs.com").first()
            if not admin_user:
                # Create admin user
                admin_user = User(
                    email="admin@izonedevs.com",
                    username="admin",
                    full_name="Admin User",
                    hashed_password=get_password_hash("admin123"),
                    role="admin",
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                db.refresh(admin_user)
                
                # Add sample event
                sample_event = Event(
                    title="Welcome to iZonehub",
                    description="Test event for Vercel deployment",
                    content="This is a test event created automatically for Vercel testing.",
                    start_date=datetime.datetime(2025, 1, 1, 10, 0),
                    end_date=datetime.datetime(2025, 1, 1, 17, 0),
                    location="Virtual",
                    max_participants=50,
                    registration_fee=0.0,
                    status="upcoming",
                    is_featured=True
                )
                db.add(sample_event)
                
                # Add sample blog post
                sample_blog = BlogPost(
                    title="Welcome to iZonehub API",
                    content="This API is now running on Vercel with in-memory SQLite for testing!",
                    excerpt="Testing the deployment...",
                    status="published",
                    is_featured=True,
                    author_id=admin_user.id
                )
                db.add(sample_blog)
                
                # Add sample partner
                sample_partner = Partner(
                    name="Test Partner",
                    description="Sample partner for testing",
                    website="https://example.com",
                    logo_url="/uploads/default-partner.png",
                    is_active=True
                )
                db.add(sample_partner)
                
                # Add sample team member
                sample_member = TeamMember(
                    name="Test Member",
                    role="Developer",
                    bio="Sample team member for testing",
                    image_url="/uploads/default-member.png",
                    email="test@izonedevs.com",
                    is_active=True
                )
                db.add(sample_member)
                
                db.commit()
        except Exception as e:
            print(f"Error setting up test data: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Export the app for Vercel
handler = app