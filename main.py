from flask import Flask, request, jsonify, send_file
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)


def trim_mp3(file_input, time_start_ms, time_end_ms):
    audio = AudioSegment.from_file(file_input, format="mp3")
    audio_trimmed = audio[time_start_ms:-time_end_ms]
    return audio_trimmed


@app.route('/trim', methods=['POST'])
def trim_audio():
    try:
        # Check if audiofile is in request.files
        if 'audiofile' not in request.files:
            return jsonify({'error': 'No audiofile part'}), 400

        # Check if start is in request.files and is not empty
        if 'start' not in request.form:
            text = f'No stat time in data. The data received: {request.form}'
            print(text)
            return jsonify({'error': text}), 400
        elif request.form['start'] == '':
            text = f'There is nothing stat. The data received: {request.form}'
            print(text)
            return jsonify({'error': text}), 400
        
        # Check if stop is in request.files and is not empty
        if 'stop' not in request.form:
            text = f'No stop time in data. The data received: {request.form}'
            print(text)
            return jsonify({'error': text}), 400
        elif request.form['stop'] == '':
            text = f'There is nothing stop. The data received: {request.form}'
            print(text)
            return jsonify({'error': text}), 400
        
        # Extract time start and time stop
        time_start_ms = int(request.form.get('start'))
        time_end_ms = int(request.form.get('stop'))
        
        # extract file
        file_input = request.files['audiofile']

        # Create the trimmed audio 
        audio_trimmed = trim_mp3(file_input, time_start_ms, time_end_ms)

        # Load trimmed audio to buffer
        audio_buffer = BytesIO()
        audio_trimmed.export(audio_buffer, format="mp3")
        audio_buffer.seek(0)

        # Send trimmed audio back
        return send_file(audio_buffer, as_attachment=True, download_name="file_trimmed.mp3")

    except Exception as e:
        return jsonify({'Server error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
