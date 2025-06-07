from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Instagram Reel Downloader API is running.'

@app.route('/download', methods=['GET'])
def download_reel():
    instagram_url = request.args.get('url')
    if not instagram_url:
        return jsonify({'error': 'يرجى إرسال رابط Instagram عبر المعامل ?url='})

    api_url = "https://instagram-reel-api.onrender.com/"
    try:
        response = requests.get(api_url, params={"url": instagram_url})
        response.raise_for_status()
        data = response.json()
        download_link = data.get("download_link")

        if download_link:
            return jsonify({
                'success': True,
                'download_link': download_link
            })
        else:
            return jsonify({
                'success': False,
                'message': 'لم يتم العثور على رابط التحميل.'
            })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})
