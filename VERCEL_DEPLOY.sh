#!/bin/bash

echo "🚀 Deploying ReHumanizer to Vercel (Everything in One Place)!"
echo "================================================"

# Change to frontend directory
cd frontend

echo "📦 Installing dependencies..."
npm install

echo "🔑 Setting up environment variables..."
echo "Please set your GEMINI_API_KEY in Vercel dashboard after deployment"

echo "🌐 Deploying to Vercel..."
npx vercel --prod

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🎉 Next Steps:"
echo "1. Copy your Vercel URL from above"
echo "2. Go to Vercel dashboard: https://vercel.com/dashboard"
echo "3. Find your project and go to Settings > Environment Variables"
echo "4. Add: GEMINI_API_KEY = your_gemini_api_key_here"
echo "5. Redeploy (or it will work on next request)"
echo ""
echo "🚀 Your app will be live at: https://your-project.vercel.app"
echo "📝 Test endpoint: https://your-project.vercel.app/api/health"
echo "🎯 Humanize page: https://your-project.vercel.app/humanize"
echo ""
echo "🎊 You're LIVE! Time to change the world!" 