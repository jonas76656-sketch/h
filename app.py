from flask import Flask, request, jsonify, render_template
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
    
    if not video_url:
        return jsonify({'success': False, 'error': 'URL လိုအပ်ပါသည်'})

    # yt-dlp options
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # ဒေါင်းလုဒ်ဆွဲရန် Link ရှာဖွေခြင်း
            video_link = info.get('url') or info.get('formats')[0].get('url')
            title = info.get('title', 'video')
            thumbnail = info.get('thumbnail', '')

            return jsonify({
                'success': True,
                'title': title,
                'thumbnail': thumbnail,
                'download_url': video_link
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Railway အတွက် Port သတ်မှတ်ခြင်း
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
