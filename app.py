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

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Set a timeout for subprocess to avoid indefinite hanging
        stdout, stderr = process.communicate(timeout=300)  # Set timeout (300s = 5 minutes)

        if process.returncode != 0:
            # Handle errors from FFmpeg
            return f"FFmpeg error: {stderr.decode()}", 500

        # If no errors, stream the output
        return Response(stdout, content_type='video/mp4')

    except subprocess.TimeoutExpired:
        return "FFmpeg transcoding timed out", 504  # Timeout error

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
