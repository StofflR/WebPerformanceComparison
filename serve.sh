#!/bin/bash
# Script to run HTTP servers for both optimized and unoptimized versions

echo "Starting HTTP servers for performance comparison..."
echo ""
echo "=================================================="
echo "OPTIMIZED version:   http://localhost:8080"
echo "UNOPTIMIZED version: http://localhost:8081"
echo "=================================================="
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $PID1 $PID2 2>/dev/null
    exit
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Start optimized server on port 8080 with gzip and brotli compression
npx http-server output/optimized/ -p 8080 --gzip -c86400 --cors --brotli --no-dotfiles -d=false &
PID1=$!

# Start unoptimized server on port 8081 with no cache and no directory listing
npx http-server output/unoptimized/ -p 8081 -c-1 --cors -d=false &
PID2=$!

# Wait for both processes
wait
