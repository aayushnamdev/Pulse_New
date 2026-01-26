#!/bin/bash
# PULSE GitHub Push Script
# Replace YOUR_USERNAME with your actual GitHub username below

echo "🚀 Pushing PULSE to GitHub..."
echo ""

# STEP 1: Replace YOUR_USERNAME with your GitHub username
GITHUB_USERNAME="aayushnamdev"

# STEP 2: Set up remote
git remote add origin "https://github.com/aayushnamdev/Pulse.git"

# STEP 3: Push to GitHub
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub"
echo "🔗 View it at: https://github.com/aayushnamdev/Pulse"
