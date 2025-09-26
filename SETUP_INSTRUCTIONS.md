# 🚀 Setup Instructions

## ⚠️ **Strands SDK Note**
The Strands SDK is not available in PyPI. The code includes fallback implementations that work without it.

## 📦 **Installation Steps**

### 1. Install Dependencies
```bash
cd sustainable-supply-chain-optimizer
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies (for MCP Server)
```bash
npm install
```

### 3. Set Environment Variables
```bash
# Windows
set AWS_ACCESS_KEY_ID=your-access-key
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AWS_DEFAULT_REGION=us-east-1
set STRANDS_API_KEY=your-strands-key  # Optional

# Linux/Mac
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
export STRANDS_API_KEY=your-strands-key  # Optional
```

## 🧪 **Testing Steps**

### 1. Test Phase 1 (Data Generation)
```bash
python test_mcp.py
```

### 2. Test Phase 2 (Analysis Agents)
```bash
python test_orchestration.py
```

### 3. Test Strands Integration (with fallback)
```bash
python test_strands_integration.py
```

### 4. Test Complete Integration
```bash
python test_integration.py
```

### 5. Start API Server
```bash
python api_endpoint.py
```

### 6. Test API Endpoints
```bash
# In new terminal
python test_api.py
```

## ✅ **Expected Results**
- ✅ All tests pass with fallback implementations
- ✅ API server runs on http://localhost:5000
- ✅ Strands features work in fallback mode
- ✅ Complete pipeline from data generation to analysis

## 🔧 **Troubleshooting**

### If MCP import fails:
```bash
pip install mcp
```

### If AWS credentials fail:
```bash
aws configure
```

### If Strands features needed:
Contact your team for actual Strands SDK package or API access.

**The system works fully without Strands SDK using intelligent fallbacks!**