from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

scraped_content = []

def generate_response(question):
    """Упрощенные ответы Шерлока Холмса"""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['привет', 'здравствуй', 'hello']):
        return "Добро пожаловать! Я Шерлок Холмс."
    
    elif any(word in question_lower for word in ['кто ты', 'представься']):
        return "Шерлок Холмс, детектив-консультант."
    
    elif any(word in question_lower for word in ['помощь', 'что умеешь']):
        return "Дедуктивный анализ, веб-скрапинг. Задайте вопрос!"
    
    elif any(word in question_lower for word in ['ватсон', 'доктор']):
        return "Мой дорогой Ватсон - верный друг."
    
    else:
        responses = [
            "Интересное наблюдение!",
            "Хм, это требует анализа.",
            "Элементарно!",
            "Интересная загадка!",
            "Позвольте мне проанализировать."
        ]
        import random
        return random.choice(responses)

def scrape_website(url):
    """Упрощенный скрапинг"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else url,
            'content': text[:300],
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Ошибка скрапинга: {e}")
        return None

@app.route('/')
def index():
    return render_template('vercel_ultra_minimal.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Сообщение не может быть пустым'})
        
        response = generate_response(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка'})

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL не может быть пустым'})
        
        scraped_data = scrape_website(url)
        
        if scraped_data:
            scraped_content.append(scraped_data)
            
            return jsonify({
                'success': True,
                'message': f'Сайт {url} проанализирован!',
                'title': scraped_data['title']
            })
        else:
            return jsonify({'error': 'Не удалось обработать URL'})
        
    except Exception as e:
        return jsonify({'error': 'Произошла ошибка'})

@app.route('/status')
def status():
    return jsonify({
        'status': 'running',
        'model': 'Sherlock Ultra Minimal',
        'scraped_sites': len(scraped_content)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 