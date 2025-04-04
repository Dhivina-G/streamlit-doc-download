import os
import openai
import streamlit as st

from weasyprint import HTML
from docx import Document
from config import Config


openai.api_key = Config.OPENAI_API_KEY


UPLOAD_FOLDER = "uploaded_files"
OUTPUT_FOLDER = "generated_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


current_directory = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_directory, 'templates', 'template.html')

st.title("File Upload, OpenAI & Convert to PDF")


UPLOAD_FOLDER = "uploaded_files"
OUTPUT_FOLDER = "generated_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


st.header("Generate Text with OpenAI")
prompt = st.text_area("Enter your prompt for OpenAI:", height=100)

if st.button("Generate Text"):
    if prompt:
        with st.spinner("Generating response..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = response.choices[0].message.content
            st.text_area("Generated Text:", value=generated_text, height=200)

            pdf_path = os.path.join(OUTPUT_FOLDER, "openai_generated.pdf")
            content_for_html = generated_text.replace('\n', '<br>')
            with open(template_path, "r") as file:
                html_template = file.read()
            html_content = html_template.replace("{content}", content_for_html)
            HTML(string=html_content).write_pdf(pdf_path)

            docx_path = os.path.join(OUTPUT_FOLDER, "openai_generated.docx")
            doc = Document()
            for line in generated_text.split("\n"):
                doc.add_paragraph(line)
            doc.save(docx_path)
            st.success("Files generated successfully!")

            col1, col2 = st.columns(2)

            with col1:
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download OpenAI PDF",
                        data=pdf_file,
                        file_name="openai_generated.pdf",
                        mime="application/pdf"
                    )

            with col2:
                with open(docx_path, "rb") as docx_file:
                    st.download_button(
                        label="Download OpenAI DOCX",
                        data=docx_file,
                        file_name="openai_generated.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
    else:
        st.warning("Please enter a prompt before generating.")

