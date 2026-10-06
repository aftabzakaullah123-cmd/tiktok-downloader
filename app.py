from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TikTok Downloader</title>

    <style>
        body {
            background: #080808;
            color: white;
            font-family: Arial;
            text-align: center;
            padding-top: 100px;
        }

        h1 {
            color: #ff2020;
            font-size: 45px;
        }

        input {
            width: 400px;
            padding: 15px;
            border: none;
            border-radius: 5px;
        }

        button {
            padding: 15px 25px;
            margin-left: 5px;
            background: #ff2020;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #cc0000;
        }

        .message {
            margin-top: 25px;
            color: #aaa;
        }
    </style>
</head>

<body>

    <h1>TIKTOK DOWNLOADER</h1>

    <p>Paste your video link below</p>

    <form method="POST">

        <input
            type="text"
            name="link"
            placeholder="Paste TikTok link here"
            required
        >

        <button type="submit">Download</button>

    </form>

    <div class="message">
        {{ message }}
    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        link = request.form.get("link")

        if not link:
            message = "Please enter a video link."

        else:

            try:

                options = {
                    "outtmpl": os.path.join(
                        DOWNLOAD_FOLDER,
                        "%(title)s.%(ext)s"
                    ),
                    "format": "best[ext=mp4]/best"
                }

                with yt_dlp.YoutubeDL(options) as ydl:

                    info = ydl.extract_info(link, download=True)

                    filename = ydl.prepare_filename(info)

                if os.path.exists(filename):

                    return send_file(
                        filename,
                        as_attachment=True
                    )

                else:
                    message = "Download file not found."

            except Exception as e:

                message = "Download failed. Please check the link."


    return render_template_string(
        HTML,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)