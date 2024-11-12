import pdfplumber
import streamlit as st
import docx2txt
import google.generativeai as genai

def app():

    st.title("Generative AI for Technical Interview Preparation from PDF")

    def read_pdf_with_pdfplumber(file):
        with pdfplumber.open(file) as pdf:
            page = pdf.pages[0]
            return page.extract_text()
        
    st.subheader("DocumentFiles")
    def pdf_ex():
        docx_file = st.file_uploader("Upload File", type=['txt', 'docx', 'pdf'])
        if docx_file is not None:
            file_details = {"Filename": docx_file.name, "FileType": docx_file.type, "FileSize": docx_file.size}
            # st.write(file_details)

            if docx_file.type == "text/plain":
                raw_text = str(docx_file.read(), "utf-8")
                st.write(raw_text)

            elif docx_file.type == "application/pdf":
                try:
                    text = read_pdf_with_pdfplumber(docx_file)
                    st.write(text)
                except:
                    st.write("Error reading PDF file")

            elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                raw_text = docx2txt.process(docx_file)
                return(raw_text)


    pdf_data=pdf_ex()

    genai.configure(api_key='AIzaSyARRLeR7znnU8USoqfYiBPMuH_8Yafpiqk')

    model = genai.GenerativeModel("gemini-1.5-flash")

    def create_prompt_template():
        
        return f""" You are a technical assistant designed to provide short and accurate answers to technical questions for interview preparation. 
        Your goal is to deliver concise, clear, and precise responses that directly address the user's query without unnecessary detail. 
        Focus on accuracy and brevity, ensuring the information is directly relevant to the question asked. The answers should be in elaborately in point.
        Help the user with the syntax to understand more effectively And Generate a example  code for  the topic.

        content={pdf_data}

        Generate 10 MCQ questions for the user with answers and explanations. Don't repeat the same question.
                    Question:
                    Answer:
                    """


 
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "you are Interview trainer bot in Technical method"},
        ]
    )
    if not pdf_data:
        st.write("upload File")
    else:
        with st.spinner('Extracting data from pdf...'):
            prompt = create_prompt_template()

            response = chat.send_message(prompt)

            st.write(response.text)
