from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json

app = Flask(__name__)

# Remove global state - use session or database in production
# For now, we'll use a simple in-memory storage that resets on each function call
def get_scraped_content():
    """Get scraped content from environment or return empty list"""
    try:
        content = os.environ.get('SCRAPED_CONTENT', '[]')
        return json.loads(content)
    except:
        return []

def set_scraped_content(content):
    """Set scraped content in environment"""
    try:
        os.environ['SCRAPED_CONTENT'] = json.dumps(content)
    except:
        pass  # Ignore if we can't set environment

def generate_response(question):
    """Упрощенные ответы Шерлока Холмса"""
    if not question:
        return "Пожалуйста, задайте вопрос."
    
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['привет', 'здравствуй', 'hello']):
        return "Добро пожаловать! Я Шерлок Холмс, детектив-консультант. Готов помочь вам в расследовании!"
    
    elif any(word in question_lower for word in ['кто ты', 'представься']):
        return "Шерлок Холмс, детектив-консультант. Специализируюсь на дедуктивном методе и анализе улик."
    
    elif any(word in question_lower for word in ['помощь', 'что умеешь', 'help']):
        return "Мои способности: дедуктивный анализ, веб-скрапинг, анализ текста. Задайте любой вопрос или предоставьте URL для анализа!"
    
    elif any(word in question_lower for word in ['ватсон', 'доктор']):
        return "Мой дорогой Ватсон - верный друг и помощник. Его медицинские знания часто дополняют мои дедуктивные способности."
    
    elif any(word in question_lower for word in ['дедукция', 'метод']):
        return "Мой метод основан на дедукции: от общего к частному. Каждая деталь имеет значение, Ватсон!"
    
    elif any(word in question_lower for word in ['бейкер стрит', '221b']):
        return "221B Бейкер-стрит - мой адрес в Лондоне. Здесь я провожу свои расследования."
    
    else:
        responses = [
            "Интересное наблюдение! Позвольте мне проанализировать детали.",
            "Хм, это требует более глубокого анализа, Ватсон.",
            "Элементарно, дорогой Ватсон!",
            "Интересная загадка! Давайте разберем её по частям.",
            "Позвольте мне применить дедуктивный метод к этому вопросу.",
            "Каждая деталь важна в расследовании.",
            "Это напоминает случай с... но позвольте мне сосредоточиться на вашем вопросе.",
            "Мой опыт подсказывает, что здесь есть что-то интересное."
        ]
        import random
        return random.choice(responses)

def scrape_website(url):
    """Упрощенный скрапинг с улучшенной обработкой ошибок"""
    try:
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit content size for Vercel
        content = text[:500] if len(text) > 500 else text
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else url,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
    except requests.exceptions.Timeout:
        return {'error': 'Превышено время ожидания при загрузке сайта'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Ошибка при загрузке сайта: {str(e)}'}
    except Exception as e:
        return {'error': f'Неожиданная ошибка: {str(e)}'}

@app.route('/')
def index():
    """Главная страница"""
    try:
        return render_template('vercel_ultra_minimal.html')
    except Exception as e:
        return f"Ошибка загрузки страницы: {str(e)}", 500

@app.route('/chat', methods=['POST'])
def chat():
    """Обработка чата"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Сообщение не может быть пустым'}), 400
        
        response = generate_response(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

@app.route('/scrape', methods=['POST'])
def scrape():
    """Обработка скрапинга"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL не может быть пустым'}), 400
        
        scraped_data = scrape_website(url)
        
        if 'error' in scraped_data:
            return jsonify({'error': scraped_data['error']}), 400
        
        # Store in environment (simplified for Vercel)
        current_content = get_scraped_content()
        current_content.append(scraped_data)
        set_scraped_content(current_content)
        
        return jsonify({
            'success': True,
            'message': f'Сайт {url} успешно проанализирован!',
            'title': scraped_data['title'],
            'content_preview': scraped_data['content'][:100] + '...'
        })
        
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

@app.route('/status')
def status():
    """Статус приложения"""
    try:
        scraped_content = get_scraped_content()
        return jsonify({
            'status': 'running',
            'model': 'Sherlock Holmes Ultra Minimal',
            'scraped_sites': len(scraped_content),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health():
    """Простая проверка здоровья приложения"""
    return jsonify({'status': 'healthy'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Страница не найдена'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False) 