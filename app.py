from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

def generate_response(question):
    """Упрощенные ответы Шерлока Холмса без внешних зависимостей"""
    if not question:
        return "Пожалуйста, задайте вопрос."
    
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['привет', 'здравствуй', 'hello']):
        return "Добро пожаловать! Я Шерлок Холмс, детектив-консультант. Готов помочь вам в расследовании!"
    
    elif any(word in question_lower for word in ['кто ты', 'представься']):
        return "Шерлок Холмс, детектив-консультант. Специализируюсь на дедуктивном методе и анализе улик."
    
    elif any(word in question_lower for word in ['помощь', 'что умеешь', 'help']):
        return "Мои способности: дедуктивный анализ, анализ текста, логическое мышление. Задайте любой вопрос!"
    
    elif any(word in question_lower for word in ['ватсон', 'доктор']):
        return "Мой дорогой Ватсон - верный друг и помощник. Его медицинские знания часто дополняют мои дедуктивные способности."
    
    elif any(word in question_lower for word in ['дедукция', 'метод']):
        return "Мой метод основан на дедукции: от общего к частному. Каждая деталь имеет значение, Ватсон!"
    
    elif any(word in question_lower for word in ['бейкер стрит', '221b']):
        return "221B Бейкер-стрит - мой адрес в Лондоне. Здесь я провожу свои расследования."
    
    elif any(word in question_lower for word in ['скрапинг', 'веб', 'сайт']):
        return "К сожалению, веб-скрапинг временно недоступен в этой версии. Но я могу помочь с анализом и дедукцией!"
    
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
    """Заглушка для скрапинга"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL не может быть пустым'}), 400
        
        return jsonify({
            'success': True,
            'message': f'Функция скрапинга временно недоступна. URL: {url}',
            'title': 'Скрапинг недоступен',
            'content_preview': 'Эта функция будет добавлена в следующей версии.'
        })
        
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

@app.route('/status')
def status():
    """Статус приложения"""
    try:
        return jsonify({
            'status': 'running',
            'model': 'Sherlock Holmes Ultra Minimal',
            'scraped_sites': 0,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
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
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Страница не найдена'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False) 