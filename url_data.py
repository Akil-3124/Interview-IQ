import requests
from bs4 import BeautifulSoup
import streamlit as st
import os
import google.generativeai as genai

def app():

    st.title("Generative AI for Technical Interview Preparation from URL")
    data=st.text_input("Enter")

    def extract_data(url):
        if data=="":
            st.write("")
        else:
            with st.spinner('Extracting data...'):
                response = requests.get(url)
                response.raise_for_status()  
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                # st.write(paragraphs)
                for para in paragraphs:
                    return(para.get_text())
                code_elements = soup.find_all('code')
                for code in code_elements:
                    return(code.get_text())

    ex_data=extract_data(data)
    # st.write(ex_data)
    # user_input=st.text_input("content")
    st.write(ex_data)

    # # genai.configure(api_key='AIzaSyARRLeR7znnU8USoqfYiBPMuH_8Yafpiqk')
    # model = genai.GenerativeModel("gemini-1.5-flash")
    # chat = model.start_chat(
    #     history=[
    #         {"role": "user", "parts": "Hello"},
    #         {"role": "model", "parts":pt},
    #     ]
    # )
    # response = chat.send_message(in_data)
    # st.write(response.text)


    genai.configure(api_key='AIzaSyARRLeR7znnU8USoqfYiBPMuH_8Yafpiqk')

    model = genai.GenerativeModel("gemini-1.5-flash")

    def create_prompt_template():
        
        return f""" You are a technical assistant designed to provide short and accurate answers to technical questions for interview preparation. 
        Your goal is to deliver concise, clear, and precise responses that directly address the user's query without unnecessary detail. 
        Focus on accuracy and brevity, ensuring the information is directly relevant to the question asked. The answers should be in elaborately in point.
        Help the user with the syntax to understand more effectively And Generate a example  code for  the topic.
        content={ex_data}
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



    if data=="":
        st.write("Enter url")
    else:
        with st.spinner('Extracting data...'):
            prompt = create_prompt_template()

            response = chat.send_message(prompt)

            st.write(response.text)

