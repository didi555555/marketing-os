from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from google import genai
from google.genai import errors as genai_errors

bp = Blueprint('analytics', __name__, template_folder='templates',
               url_prefix='/plugin/analytics')

@bp.route('/')
@login_required
def index():
    return render_template('analytics_index.html')

@bp.route('/competitor', methods=['POST'])
@login_required
def competitor():
    competitors = request.json.get('competitors', '')
    industry = request.json.get('industry', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'حلل المنافسين التاليين في مجال {industry}: {competitors}. قدم تحليلاً بالعربية يشمل: نقاط القوة والضعف، استراتيجيات التسويق، الجمهور المستهدف، وفرص التميز.'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': resp.text})

@bp.route('/psychology', methods=['POST'])
@login_required
def psychology():
    product = request.json.get('product', '')
    audience = request.json.get('audience', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'قدم تحليل سيكولوجي تسويقي للمنتج: {product} والجمهور: {audience}. اشرح بالعربية: المحفزات النفسية المؤثرة، التحيزات المعرفية، وكيفية تطبيق مبادئ الإقناع (Cialdini).'
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
