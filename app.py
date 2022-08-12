from flask import Flask, render_template, request, redirect, send_file
import stt
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    value = ""
    error = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            msl = int(request.form['min_silence_len'])
            st = int(request.form['silence_thresh'])
            ks = int(request.form['keep_silence'])
            lang = str(request.form['lang'])
            value = stt.get_large_audio_transcription(file, msl, st, ks, lang)
            error = stt.errorcount
            with open('transcriber.txt', 'w') as f:
                f.write(value)

    return render_template('index.html', transcript=value, error=error)


@app.route('/download')
def download_file():
    path = "transcriber.txt"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
