import os
import sys

# 獲取執行檔的基礎路徑（適用於 PyInstaller 打包）
def get_base_path():
    if getattr(sys, 'frozen', False):
        # 在 PyInstaller 打包的環境中
        return sys._MEIPASS
    else:
        # 在開發環境中
        return os.path.dirname(os.path.abspath(__file__))

# 設定基礎路徑
BASE_PATH = get_base_path()

# 確保 src 模組可以被正確導入
sys.path.insert(0, BASE_PATH)

from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp
from src.routes.xml_generator import xml_bp

# 設定 Flask 應用程式，指定 static 資料夾路徑
static_path = os.path.join(BASE_PATH, 'static')
app = Flask(__name__, static_folder=static_path)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(xml_bp, url_prefix='/api')

# 設定資料庫路徑
database_path = os.path.join(BASE_PATH, 'src', 'database', 'app.db')
# 確保資料庫目錄存在
os.makedirs(os.path.dirname(database_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    # 在打包後建議關閉 debug 模式
    debug_mode = not getattr(sys, 'frozen', False)
    app.run(host='0.0.0.0', port=5001, debug=debug_mode)