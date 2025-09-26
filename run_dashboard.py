#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dashboard.app import app

if __name__ == '__main__':
    print("🌱 Starting Sustainable Supply Chain Optimizer Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🚀 Click 'Run Demo Analysis' to see the AI agents in action!")
    app.run(debug=True, host='0.0.0.0', port=5000)