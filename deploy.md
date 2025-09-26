# 🚀 Phase 3: Deployment Guide

## Quick Local Demo

```bash
python run_dashboard.py
```
Visit: http://localhost:5000

## Deploy to Vercel (Recommended)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
vercel --prod
```

3. **Generate QR Code**
```bash
# Update URL in generate_qr.py with your Vercel URL
python generate_qr.py
```

## Deploy to Netlify

1. **Connect GitHub repo to Netlify**
2. **Build settings**: Use `netlify.toml` configuration
3. **Deploy automatically on push**

## Deploy to AWS (Alternative)

```bash
# Using AWS App Runner or Elastic Beanstalk
pip install awsebcli
eb init
eb create supply-chain-optimizer
eb deploy
```

## 📱 Demo Access

After deployment:
1. Update URL in `generate_qr.py`
2. Run `python generate_qr.py`
3. Share `demo_qr_code.png` for mobile access
4. Use `demo_access.html` for presentation

## 🎯 Demo Flow

1. **Landing Page**: Clean dashboard interface
2. **Click "Run Demo"**: Triggers AI agent orchestration
3. **Real-time Analysis**: Shows loading state
4. **Results Display**: 
   - Sustainability grade (A-D)
   - Carbon footprint breakdown
   - Supplier scores chart
   - Top 5 recommendations

## 📊 Key Metrics Displayed

- **Sustainability Grade**: A+ to D rating
- **Carbon Footprint**: Total tons CO2
- **Suppliers Analyzed**: Count of processed suppliers
- **Routes Optimized**: Transportation routes analyzed
- **Interactive Charts**: Doughnut + Bar charts
- **Actionable Recommendations**: Top 5 AI-generated suggestions