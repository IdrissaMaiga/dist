from flask import Flask, request, Response
import subprocess

app = Flask(__name__)

@app.route('/transcoded/', methods=['GET'])
def transcode():
    source_url = request.args.get('url')
    if not source_url:
        return "Source URL is required", 400

    # Use FFmpeg to transcode
    command = [
        'ffmpeg', '-i', source_url, '-c:v', 'libx264', '-f', 'mp4', 'pipe:1'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return Response(process.stdout, content_type='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
