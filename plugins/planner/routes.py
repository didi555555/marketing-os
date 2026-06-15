from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from google import genai
from google.genai import errors as genai_errors

bp = Blueprint('planner', __name__, template_folder='templates',
               url_prefix='/plugin/planner')

@bp.route('/')
@login_required
def index():
    return render_template('planner_index.html')

@bp.route('/marketing-plan', methods=['POST'])
@login_required
def marketing_plan():
    business = request.json.get('business', '')
    budget = request.json.get('budget', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'ضع خطة تسويقية شاملة بالعربية للbusiness: {business} والميزانية: {budget}. شمل: الأهداف، الجمهور المستهدف، القنوات، خطة المحتوى، الميزانية، والجدول الزمني.'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': resp.text})

@bp.route('/product-market', methods=['POST'])
@login_required
def product_market():
    product = request.json.get('product', '')
    features = request.json.get('features', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'حلل وضع المنتج التالي: {product}. المميزات: {features}. قدم بالعربية: تحديد الجمهور المستهدف (ICP)، التمركز (Positioning)، البيان القيمي (Value Proposition).'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': resp.text})

@bp.route('/brainstorm', methods=['POST'])
@login_required
def brainstorm():
    topic = request.json.get('topic', '')
    goal = request.json.get('goal', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'نفذ جلسة عصف ذهني للموضوع: {topic}. الهدف: {goal}. قدم 10 أفكار إبداعية بالعربية مع شرح مختصر لكل فكرة.'
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
