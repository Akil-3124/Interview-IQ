from langchain_google_genai import GoogleGenerativeAI
from crewai import Crew, Process, Agent, Task
import streamlit as st

def app():
    # Initialize the LLM
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        verbose=True,
        temperature=0.5,
        google_api_key='AIzaSyBqlzrpUhy9ojFvG7YseCNB6Tq2f9mg8pY' )

    topic = st.chat_input("Enter the topic you want to learn about:")
    st.info(topic)


    # Define the learning agent
    learning_agent = Agent(
        role="Learning Specialist",
        goal="Teach users about the given topic in a simple, clear, and engaging manner. The agent aims to simplify complex concepts, use relatable examples, and ensure the user understands key points through interactive learning techniques.",
        verbose=True,
        memory=True,
        backstory="You are an expert in teaching and explaining topics in a way that's easy to understand. Equipped with a knack for breaking down complex information, you excel at making learning enjoyable and accessible for everyone. Your primary mission is to empower users by delivering easy-to-digest educational content.",
        llm=llm,
        allow_delegation=False
    )

    # Define the tasks for the LearningAgent
    explain_concepts_task = Task(
        description=f"Explain the key concepts of the topic: {topic} in simple and clear terms.",
        expected_output=f"Basic explanation of {topic} that is easy to understand.",
        agent=learning_agent,
        asyn_execution=False
    )

    provide_examples_task = Task(
        description=f"Provide easy-to-understand examples related to {topic} to help illustrate key concepts.",
        expected_output=f"Examples that make the concepts of {topic} more relatable and understandable.",
        agent=learning_agent,
        asyn_execution=False
    )

    interactive_quiz_task = Task(
        description=f"Create an interactive quiz to reinforce learning about {topic}.",
        expected_output=f"A short quiz with questions that test understanding of {topic}.",
        agent=learning_agent,
        asyn_execution=False
    )

    simplified_summary_task = Task(
        description=f"Generate a simplified summary of {topic} to help reinforce learning.",
        expected_output=f"A brief summary of {topic} covering the most important points.",
        agent=learning_agent,
        asyn_execution=False
    )

    # Initialize the Crew with the LearningAgent and tasks
    crew = Crew(
        agents=[learning_agent],
        tasks=[
            explain_concepts_task,
            provide_examples_task,
            interactive_quiz_task,
            simplified_summary_task
        ],
        verbose=True,
        process=Process.sequential
    )

    # Execute the Crew's kickoff process only if a topic has been provided
    if topic:
        result = crew.kickoff()
        st.write(result.raw)
    else:
        st.write("Please enter a topic to begin the learning process.")


