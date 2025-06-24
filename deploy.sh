#!/bin/bash

echo "🚀 Подготовка к развертыванию на Vercel..."

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI не установлен. Установите его: npm i -g vercel"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py не найден. Убедитесь, что вы в правильной директории."
    exit 1
fi

# Check if requirements file exists
if [ ! -f "requirements_vercel_minimal.txt" ]; then
    echo "❌ requirements_vercel_minimal.txt не найден."
    exit 1
fi

# Check if vercel.json exists
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json не найден."
    exit 1
fi

echo "✅ Все файлы на месте"

# Deploy to Vercel
echo "🌐 Развертывание на Vercel..."
vercel --prod

echo "✅ Развертывание завершено!"
echo "🔗 Проверьте ваш сайт на Vercel" 