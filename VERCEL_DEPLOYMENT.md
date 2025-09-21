# Vercel Deployment Guide for iZonehub Backend

## 🚀 Quick Deployment Steps

### 1. Prerequisites
- Install Vercel CLI: `npm install -g vercel`
- Have a Vercel account at [vercel.com](https://vercel.com)
- Set up a PostgreSQL database (recommended: [Neon](https://neon.tech), [Supabase](https://supabase.com), or [Railway](https://railway.app))

### 2. Deploy to Vercel

```bash
# From the backend directory
cd backend
vercel login
vercel --prod
```

Or use the deployment script:
```bash
# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Windows PowerShell
.\deploy.ps1
```

### 3. Configure Environment Variables

In your Vercel dashboard, add these environment variables:

```env
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-super-secure-32-character-minimum-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=izonemakers@gmail.com
SMTP_PASSWORD=kmub uxpm bhsw qnkd
DEBUG=False
VERCEL=1
```

### 4. Database Setup

**Option A: Neon (Recommended)**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Add it to Vercel as `DATABASE_URL`

**Option B: Supabase**
1. Sign up at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the connection string
5. Add it to Vercel as `DATABASE_URL`

### 5. Update Frontend

Update your frontend API URL to point to your Vercel deployment:

```typescript
// src/services/api.ts
const API_BASE_URL = 'https://your-backend.vercel.app/api';
```

## 📋 Deployment Architecture

```
Frontend (Vercel/Netlify) ← → Backend (Vercel) ← → Database (Neon/Supabase)
```

## ⚠️ Important Notes

### Limitations of Vercel for FastAPI:
1. **Serverless Functions**: Each request is a separate function call
2. **Cold Starts**: First request may be slower
3. **File Storage**: No persistent file system (use cloud storage for uploads)
4. **Database**: SQLite doesn't work well (use PostgreSQL)

### Files Created for Vercel:
- `vercel.json` - Vercel configuration
- `api/index.py` - Vercel handler
- `deploy.sh` / `deploy.ps1` - Deployment scripts

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**
   - Make sure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Database Connection**
   - Verify `DATABASE_URL` format
   - Ensure database is accessible from Vercel

3. **CORS Issues**
   - Add your frontend domain to `allowed_origins`
   - Check Vercel function logs

4. **File Upload Issues**
   - Vercel has no persistent storage
   - Consider using AWS S3 or Cloudinary for file uploads

### View Logs:
```bash
vercel logs your-project-url
```

## 🌐 Alternative Deployment Options

If Vercel proves challenging, consider:
- **Railway**: Better for traditional apps
- **DigitalOcean App Platform**: Full-stack support
- **Heroku**: Classic PaaS option
- **AWS Elastic Beanstalk**: Enterprise option

## 🎯 Production Checklist

- [ ] Database migrated to PostgreSQL
- [ ] Environment variables configured
- [ ] CORS origins updated
- [ ] File upload strategy decided
- [ ] Frontend updated with new API URL
- [ ] SSL certificate verified
- [ ] Performance testing completed