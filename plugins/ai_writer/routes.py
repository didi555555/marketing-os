from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from google import genai
from google.genai import errors as genai_errors
from core.utils import strip_markdown

ai_writer_bp = Blueprint('ai_writer', __name__, template_folder='templates',
                         url_prefix='/plugin/ai-writer')

@ai_writer_bp.route('/')
@login_required
def index():
    return render_template('ai_writer_index.html')

@ai_writer_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    prompt = request.json.get('prompt', '')
    mode = request.json.get('mode', 'copywriting')
    api_key = current_app.config.get('GEMINI_API_KEY', '')

    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط. أضفه في ملف .env'}), 400

    system_prompts = {
        'copywriting': 'أنت كاتب إعلانات محترف. اكتب نصاً تسويقياً مقنعاً بدون استخدام أي تنسيق (لا نجوم، لا شرطات، لا علامات).',
        'editing': 'أنت محرر نصوص محترف. راجع النص التالي وحسّنه بدون استخدام أي تنسيق (لا نجوم، لا شرطات، لا علامات).',
        'strategy': 'أنت خبير استراتيجية محتوى. اكتب خطة محتوى كاملة بدون استخدام أي تنسيق (لا نجوم، لا شرطات، لا علامات).',
    }

    client = genai.Client(api_key=api_key)
    full_prompt = f"{system_prompts.get(mode, system_prompts['copywriting'])}\n\n{prompt}"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=full_prompt
        )
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500

    result = strip_markdown(response.text)
    return jsonify({'result': result})

def register(app):
    app.register_blueprint(ai_writer_bp)
