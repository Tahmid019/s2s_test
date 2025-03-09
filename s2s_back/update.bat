echo "🔍 Detecting new dependencies..."
python auto_requirements.py

echo "📦 Installing dependencies..."
python requirements.py

echo "✅ All dependencies are up to date!"
