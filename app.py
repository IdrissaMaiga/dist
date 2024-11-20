from flask import Flask, request, Response, jsonify
import subprocess

app = Flask(__name__)

@app.route('/transcoded/', methods=['GET'])
def transcode():
    source_url = request.args.get('url')
    if not source_url:
        # Return a JSON error response
        return jsonify({"error": "Source URL is required"}), 400

    # Use FFmpeg to transcode
    command = [
        'ffmpeg', '-loglevel', 'debug', '-i', source_url, '-c:v', 'libx264', '-f', 'mp4', 'pipe:1'
    ]

    try:
        # Run FFmpeg process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Set a timeout for subprocess to avoid indefinite hanging
        stdout, stderr = process.communicate(timeout=300)  # Set timeout (300s = 5 minutes)

        if process.returncode != 0:
            # If FFmpeg returns an error, show the error in a structured format
            error_message = stderr.decode()
            return jsonify({
                "error": "FFmpeg transcoding failed",
                "details": error_message
            }), 500

        # If no errors, stream the output (video)
        return Response(stdout, content_type='video/mp4')

    except subprocess.TimeoutExpired:
        # Handle timeout error
        return jsonify({
            "error": "FFmpeg transcoding timed out",
            "details": "The transcoding process took too long and was stopped."
        }), 504  # Timeout error

    except Exception as e:
        # Catch any other unexpected errors
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
