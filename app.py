import hashlib
import os

from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename, redirect
from pdf2image import convert_from_path
from pdf2docx import parse

app = Flask(__name__)
cors = CORS(app)

DIR = "./uploads/"


@app.route('/', methods=['POST'])
@cross_origin()
def pdf_word():
    upload_file = request.files['pdf-word']
    if upload_file.filename != '':
        docx_extension = ".docx"
        filename, file_extension = os.path.splitext(upload_file.filename)
        md5_obj = hashlib.md5()
        md5_obj.update(filename.encode('utf-8'))
        filename_hash = md5_obj.hexdigest()
        full_filename = secure_filename(filename_hash) + file_extension
        docx_filename = secure_filename(filename_hash) + docx_extension
        upload_file.save(os.path.join(DIR, full_filename))
        docx_url = DIR+filename_hash+docx_extension
        parse(os.path.join(DIR, full_filename), docx_url, start=0)
        return jsonify({
            'error': False,
            'file': url_for('uploaded_file', filename=docx_filename)
        })
    else:
        return jsonify({
            'error': True,
            'message': 'Please provide the file'
        })


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(DIR,
                               filename)


if __name__ == '__main__':
    app.run()
