import os
import openai
import PyPDF2

# Set your OpenAI API key
openai.api_key = '<open-ai-key>'

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)  # Use PdfReader instead of PdfFileReader
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def generate_summary(text):
    prompt = f"Summarize the business analysis of the given document:\n{text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return summary

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_file_path = os.path.join(script_dir, "Zomato.pdf")  # Replace with your PDF file name
    document_text = read_pdf(pdf_file_path)

    if document_text:
        summary = generate_summary(document_text)
        print("Business Analysis Summary:")
        print(summary)
    else:
        print("Error reading the PDF file.")

if __name__ == "__main__":
    main()
