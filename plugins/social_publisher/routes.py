from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from google import genai
from google.genai import errors as genai_errors

bp = Blueprint('social_publisher', __name__, template_folder='templates',
               url_prefix='/plugin/social-publisher')

@bp.route('/')
@login_required
def index():
    return render_template('social_index.html')

@bp.route('/generate', methods=['POST'])
@login_required
def generate():
    topic = request.json.get('topic', '')
    platform = request.json.get('platform', 'facebook')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    platform_names = {'facebook': 'فيسبوك', 'twitter': 'تويتر/X', 'linkedin': 'لينكدإن', 'instagram': 'إنستغرام', 'tiktok': 'تيك توك'}
    client = genai.Client(api_key=api_key)
    prompt = f'اكتب منشور تسويقي احترافي لمنصة {platform_names.get(platform, platform)} بالعربية. الموضوع: {topic}'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': resp.text})

def register(app):
    app.register_blueprint(bp)
