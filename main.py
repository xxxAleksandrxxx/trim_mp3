from flask import Flask, request, jsonify, send_file
from pydub import AudioSegment

app = Flask(__name__)

def trim_mp3(file_input, time_start_ms, time_end_ms):
    audio = AudioSegment.from_file(file_input, format="mp3")
    audio_trimmed = audio[time_start_ms:-time_end_ms]
    return audio_trimmed

@app.route('/trim', methods=['POST'])
def trim_audio():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file_input = request.files['file']
        time_start_ms = int(request.form.get('time_start_ms', 0))
        time_end_ms = int(request.form.get('time_end_ms', len(file_input)))

        # Create the trimmed audio in-memory
        audio_trimmed = trim_mp3(file_input, time_start_ms, time_end_ms)

        # Save the trimmed audio to a new file
        base_name = file_input.filename.split('.')[0]
        trimmed_filename = f"{base_name}_trimmed.mp3"
        audio_trimmed.export(trimmed_filename, format="mp3")

        # Return the trimmed audio file as a response
        return send_file(trimmed_filename, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
