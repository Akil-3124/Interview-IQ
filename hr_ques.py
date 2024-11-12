import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from crewai import Crew, Process, Agent, Task

def app():
    # Replace 'YOUR_API_KEY' with your actual API key
    genai.configure(api_key='AIzaSyBqlzrpUhy9ojFvG7YseCNB6Tq2f9mg8pY')

    # Create a generative model instance
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Upload either an image or a PDF file
    uploaded_file = st.file_uploader("Upload an image or a PDF", type=["jpg", "jpeg", "png", "pdf"])
    
    # Initialize response to avoid UnboundLocalError
    response = None

    if uploaded_file:
        # Determine the file type based on the file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Prepare the prompt
        prompt = (
        "Extract the text from the provided {file_type}."
        " Present in a summarised point-by-point format:"
        )

        if file_extension in [".jpg", ".jpeg", ".png"]:
            # Save the uploaded image temporarily
            temp_file_path = "temp_image.jpg"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Upload the image to the generative model
            uploaded_file_path = genai.upload_file(temp_file_path)
            
            # Generate content based on the image and prompt
            response = model.generate_content([
                uploaded_file_path,
                "\n\n",
                prompt.format(file_type="image")
            ])

        elif file_extension == ".pdf":
            # Save the uploaded PDF temporarily
            temp_file_path = "temp_pdf.pdf"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Upload the PDF to the generative model
            uploaded_file_path = genai.upload_file(temp_file_path)
            
            # Generate content based on the PDF and prompt
            response = model.generate_content([
                uploaded_file_path,
                "\n\n",
                prompt.format(file_type="PDF")
            ])
    
    # Check if response contains data before accessing it
    if response:
        # st.write(response.text)
        pdf_data = response.text
    else:
        pdf_data = None
        st.write("No file was uploaded or there was an error processing the file.")
    
    # If pdf_data is not None, generate HR questions
    if pdf_data:
        goole_llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            verbose=True,
            temperature=0.5,
            google_api_key='AIzaSyBqlzrpUhy9ojFvG7YseCNB6Tq2f9mg8pY'
        )

        hr_agent = Agent(
            role='Hiring Agent',
            goal='Conduct a structured interview based on extracted skills from a resume',
            backstory='The Hiring Agent has over 10 years of experience in talent acquisition across various industries...',
            llm=goole_llm,
            memory=True,
            verbose=True,
        )

        hr_questions_task = Task(
            description=f"Generate a list of HR interview questions for the role: {pdf_data}. Focus on evaluating skills, experience, and cultural fit.",
            expected_output=f"A set of interview questions tailored to the role of {pdf_data}.",
            agent=hr_agent,
            asyn_execution=False
        )

        crew = Crew(
            agents=[hr_agent],
            tasks=[hr_questions_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        st.write(result.raw)
    else:
        st.write("Please upload a valid file to begin the learning process.")
