import requests
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    
    ydl_opts = {'format': 'best', 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_link = info.get('url') or info.get('formats')[0].get('url')
            return jsonify({
                'success': True,
                'title': info.get('title', 'video'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': video_link
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ဖိုင်ကို တိုက်ရိုက်ဒေါင်းလုဒ်ဆွဲပေးမည့် Proxy Route
@app.route('/proxy-download')
def proxy_download():
    url = request.args.get('url')
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), 
                    content_type=r.headers['Content-Type'],
                    headers={"Content-Disposition": "attachment; filename=video.mp4"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
