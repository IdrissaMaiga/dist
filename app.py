from flask import Flask, request, Response, jsonify, stream_with_context
import subprocess

app = Flask(__name__)

@app.route('/transcoded/', methods=['GET'])
def transcode():
    source_url = request.args.get('url')
    if not source_url:
        return jsonify({"error": "Source URL is required"}), 400

    # FFmpeg command for live transcoding
    command = [
        'ffmpeg', '-loglevel', 'error', '-i', source_url, '-c:v', 'libx264',
        '-preset', 'ultrafast', '-f', 'mp4', 'pipe:1'
    ]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**6)

        def generate():
            try:
                while True:
                    chunk = process.stdout.read(1024 * 64)  # Read in 64KB chunks
                    if not chunk:
                        break
                    yield chunk
            finally:
                process.stdout.close()
                process.terminate()

        return Response(stream_with_context(generate()), content_type='video/mp4')

    except Exception as e:
        return jsonify({"error": "FFmpeg transcoding failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
