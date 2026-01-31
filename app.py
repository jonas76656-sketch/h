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
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # ဒေါင်းလုဒ်ဆွဲရန် တိုက်ရိုက် Link ကို ရှာဖွေခြင်း
            video_link = info.get('url') or info.get('formats')[0].get('url')
            return jsonify({
                'success': True,
                'title': info.get('title', 'video'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': video_link
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ဤ Route က 425 bytes ပြဿနာကို ဖြေရှင်းပေးမည်ဖြစ်သည်
@app.route('/proxy-download')
def proxy_download():
    target_url = request.args.get('url')
    if not target_url:
        return "URL missing", 400
        
    # Backend ကနေ ဗီဒီယိုကို Stream လုပ်ပြီး Client ထံသို့ တိုက်ရိုက်ပို့ပေးခြင်း
    r = requests.get(target_url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
    
    def generate():
        for chunk in r.iter_content(chunk_size=1024*1024):
            yield chunk
            
    return Response(generate(), 
                    content_type=r.headers.get('Content-Type', 'video/mp4'),
                    headers={"Content-Disposition": "attachment; filename=video.mp4"})

if __name__ == '__main__':
    # Railway ၏ Port သတ်မှတ်ချက်အတိုင်း Run ခြင်း
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
