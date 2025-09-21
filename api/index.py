# Vercel-specific configuration for serverless deployment
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import your existing app
from main import app

# For Vercel testing with in-memory SQLite, auto-create tables and seed data
if os.getenv("VERCEL"):
    from database import create_tables
    from sqlalchemy.orm import Session
    from database import get_db, User, Event, BlogPost
    from auth import get_password_hash
    
    # Create tables on startup
    create_tables()
    
    # Add some test data for in-memory database
    def seed_test_data():
        db = next(get_db())
        try:
            # Check if admin user exists
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
                
                # Add sample event
                sample_event = Event(
                    title="Welcome to iZonehub",
                    description="Test event for Vercel deployment",
                    content="This is a test event created automatically for Vercel testing.",
                    start_date="2025-01-01T10:00:00",
                    end_date="2025-01-01T17:00:00",
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
                    author_id=admin_user.id if hasattr(admin_user, 'id') else 1
                )
                db.add(sample_blog)
                
                db.commit()
        except Exception as e:
            print(f"Error seeding data: {e}")
        finally:
            db.close()
    
    # Seed test data
    seed_test_data()

# Configure CORS for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For Vercel, we need to handle static files differently
# Remove static file mounting if it exists
try:
    # This will fail in serverless environment, which is expected
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except:
    pass  # Ignore in serverless environment

# Export for Vercel
app = app