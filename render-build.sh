#!/usr/bin/env bash

set -e  # ❌ Detiene el script si cualquier comando falla

echo "📦 Updating apt and installing ffmpeg..."
apt-get update -y
apt-get install -y ffmpeg

# ✅ Verifica que ffmpeg está instalado correctamente
if ! command -v ffmpeg > /dev/null; then
  echo "❌ FFmpeg is not installed correctly."
  exit 1
fi

echo "✅ FFmpeg installed successfully."

# Instala dependencias de Python
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Build completed."