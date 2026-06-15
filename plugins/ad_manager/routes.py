from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from google import genai
from google.genai import errors as genai_errors

bp = Blueprint('ad_manager', __name__, template_folder='templates',
               url_prefix='/plugin/ad-manager')

@bp.route('/')
@login_required
def index():
    return render_template('ad_index.html')

@bp.route('/strategy', methods=['POST'])
@login_required
def strategy():
    platform = request.json.get('platform', 'facebook')
    product = request.json.get('product', '')
    budget = request.json.get('budget', '500')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'قدم استراتيجية إعلانات متكاملة لمنصة {platform} للمنتج: {product}. الميزانية: {budget}. بالعربية: الجمهور المستهدف، أنواع الإعلانات، نصائح للاستهداف، تحسين الحملة.'
    try:
        resp = client.models.generate_content(model='gemini-2.5-flash-lite', contents=prompt)
    except genai_errors.ClientError as e:
        if hasattr(e, 'code') and e.code == 429:
            return jsonify({'error': 'وصلت للحد المسموح من الطلبات. انتظر دقيقة وحاول مرة أخرى.', 'retry_after': 30}), 429
        return jsonify({'error': f'خطأ في Gemini API: {str(e)[:100]}'}), 500
    except Exception as e:
        return jsonify({'error': f'حدث خطأ في الاتصال بـ Gemini API: {str(e)[:100]}'}), 500
    return jsonify({'result': resp.text})

@bp.route('/copy', methods=['POST'])
@login_required
def copy():
    platform = request.json.get('platform', 'facebook')
    product = request.json.get('product', '')
    offer = request.json.get('offer', '')
    api_key = __import__('flask').current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'مفتاح Gemini API غير مضبوط'}), 400

    client = genai.Client(api_key=api_key)
    prompt = f'اكتب 3 نصوص إعلانية (Ad Copy) بالعربية لمنصة {platform} للمنتج: {product}. العرض: {offer}. كل نص يشمل: عنوان، وصف، دعوة للإجراء (CTA).'
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
