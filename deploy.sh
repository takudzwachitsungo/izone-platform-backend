#!/bin/bash

# Vercel Deployment Script for iZonehub Backend

echo "🚀 Preparing iZonehub Backend for Vercel Deployment"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

echo "✅ Backend directory confirmed"

# Check for required files
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

echo "✅ Required files found"

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "🎉 Deployment complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Set up environment variables in Vercel dashboard:"
echo "   - DATABASE_URL (PostgreSQL connection string)"
echo "   - SECRET_KEY (32+ character random string)"
echo "   - SMTP_PASSWORD (your app password)"
echo ""
echo "2. Update your frontend to use the new API URL"
echo "3. Configure your database on a cloud provider"
echo ""
echo "🔗 Visit your Vercel dashboard to see the deployment URL"