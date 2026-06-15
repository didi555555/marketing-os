from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from core.config import Config
from core.database import db, User
from core.auth import auth_bp
from plugins import register_plugins, discover_plugins

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    root = Path(__file__).resolve().parent.parent
    app = Flask(__name__, template_folder=str(root / 'templates'), static_folder=str(root / 'static'))
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)

    register_plugins(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    @app.route('/dashboard')
    def dashboard():
        if not current_user.is_authenticated:
            return render_template('login.html')
        plugins = discover_plugins()

        weekdays = ['الأحد','الإثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت']
        today = datetime.now()
        weekly_activity = []
        for i in range(6, -1, -1):
            weekly_activity.append(hash(str(today.date() - timedelta(days=i))) % 10 + 1)

        stats = {
            'content_count': 12,
            'posts_count': 5,
            'keywords_count': 28,
            'weekly_activity': weekly_activity,
            'recent_activity': [
                {'text': 'تم إنشاء <strong>مقال جديد</strong> في أداة الكتابة', 'time': 'منذ ١٠ دقائق', 'color': 'gold'},
                {'text': 'تحليل <strong>SEO</strong> لصفحة المنتج', 'time': 'منذ ٣٠ دقيقة', 'color': 'green'},
                {'text': 'تم إنشاء <strong>صورة</strong> في استديو الوسائط', 'time': 'منذ ساعة', 'color': 'blue'},
            ]
        }
        return render_template('dashboard.html', plugins=plugins, stats=stats)

    return app
