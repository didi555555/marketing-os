from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from google import genai
from google.genai import errors as genai_errors
from core.utils import strip_markdown

bp = Blueprint('seo_suite', __name__, template_folder='templates',
               url_prefix='/plugin/seo-suite')

@bp.route('/')
@login_required
def index():
    return render_template('seo_index.html')

@bp.route('/audit', methods=['POST'])
@login_required
def audit():
    url = request.json.get('url', '')
    keywords = request.json.get('keywords', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'حلل SEO للموقع {url}. الكلمات المفتاحية: {keywords}. قدم تقريراً مفصلاً بالعربية يشمل: تحليل العنوان والوصف، الروابط، تحسين المحتوى، وسرعة الموقع، واقتراحات للتحسين. بدون تنسيق (لا نجوم، لا شرطات، لا أرقام).'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': strip_markdown(resp.text)})

@bp.route('/ai-seo', methods=['POST'])
@login_required
def ai_seo():
    content = request.json.get('content', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'حسّن المحتوى التالي لظهوره في محركات البحث الذكية (AI Search مثل ChatGPT, Perplexity). أضف هيكلة مناسبة وإجابات مباشرة. بدون تنسيق (لا نجوم، لا شرطات). المحتوى: {content}'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': strip_markdown(resp.text)})

@bp.route('/schema', methods=['POST'])
@login_required
def schema():
    page_type = request.json.get('page_type', 'Product')
    details = request.json.get('details', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'أنشئ كود JSON-LD Schema.org من نوع {page_type} بناءً على: {details}. أعد فقط كود JSON صالح.'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': strip_markdown(resp.text)})

def register(app):
    app.register_blueprint(bp)
