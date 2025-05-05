from flask import Flask, request, jsonify
import random

app = Flask(__name__)
url_map = {}
used_codes = set()

def generate_short_code():
    """يولد كودًا قصيرًا عشوائيًا مكونًا من 4 أرقام."""
    code = str(random.randint(1000, 9999))
    while code in used_codes:
        code = str(random.randint(1000, 9999))
    used_codes.add(code)
    return code

def shorten_url(long_url):
    """يقوم بإنشاء رابط مختصر من رابط طويل باستخدام 4 أرقام."""
    short_code = generate_short_code()
    short_url = f"192.168.1.6:5000/{short_code}"
    url_map[short_url] = long_url
    return short_url

@app.route('/')
def home():
    """صفحة رئيسية بسيطة."""
    return "API لاختصار الروابط يعمل!"

@app.route('/shorten')
def shorten():
    """يستقبل رابطًا طويلاً كمعامل GET ويعيد رابطًا مختصرًا."""
    long_url = request.args.get('url')
    if long_url:
        shortened = shorten_url(long_url)
        return jsonify({"link": shortened}), 200
    else:
        return jsonify({"error": "يرجى توفير معامل 'url' في عنوان URL."}), 400

@app.route('/<short_code>')
def redirect_url(short_code):
    """يقوم بإعادة التوجيه إلى الرابط الأصلي."""
    short_url = f"192.168.1.6:5000/{short_code}"
    if short_url in url_map:
        return f'<script>window.location.href = "{url_map[short_url]}";</script>'
    else:
        return jsonify({"error": "الرابط المختصر غير موجود."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
