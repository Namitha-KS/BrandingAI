from flask import Flask, render_template, request, redirect, url_for
import os
import openai
import PyPDF2

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '<key>'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text


def generate_summary(text):
    prompt1 = f"Summarize the business analysis of the given document:\n{text}"
    prompt2 = f"Business Objectives and Goals of the given document:\n{text}"
    prompt3 = f"Target Audience and Buyer Personas of the given document:\n{text}"
    prompt4 = f"Competitive Landscape of the given document:\n{text}"
    prompt5 = f"SWOT Analysis of the given document:\n{text}"
    prompt6 = f"Budget and Resources of the given document:\n{text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()

    response1 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt1,
        max_tokens=200,
        temperature=0.7,
    )

    audience = response.choices[0].text.strip()

    response2 = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt2,
        max_tokens=200,
        temperature=0.7,
    )

    landscape = response.choices[0].text.strip()

    # summary = ' this is the summary '
    return summary, audience, landscape


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            document_text = read_pdf(file_path)

            if document_text:
                summary = generate_summary(document_text)
                return render_template(summary=summary)
            else:
                return render_template('error.html', message="Error reading the PDF file.")

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
