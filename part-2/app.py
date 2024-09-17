import streamlit as st
from dotenv import load_dotenv
import os
import requests


from pydantic_models import QueryRequest
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor
from gpt_utils import *
from prompt import *

# Load environment variables
load_dotenv()

# Initialize Streamlit app
st.title("Streamlit Chatbot with PDF and Web Search")

# Setup API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Google Search Tool

# uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
# url = st.sidebar.text_input("Enter URL")

with st.sidebar:
    file_uploader=st.file_uploader("Upload your file:", type=["pdf"])
    url=st.text_input("Enter URL")
    if file_uploader is not None and "upload_pdf" not in st.session_state:
        response=requests.post(f"http://127.0.0.1:8000/add_pdf/",files={"file":file_uploader})
        if response.status_code==200:
            st.success("Messages added successfully")
        st.session_state.upload_pdf="positive"

    elif url and "url" not in st.session_state:
        # url='https://blog.futuresmart.ai/guide-to-langsmith'
        # file_path = './handbook.pdf'

        # with open(file_path, 'rb') as file:
        if not url.startswith(('http://', 'https://')):
            st.error("Invalid URL format. Please ensure the URL starts with 'http://' or 'https://'.")
    
        else:
            response = requests.post(f"http://127.0.0.1:8000/scrape_webdata/", json={"url": url})

        if response.status_code == 200:
            st.success("Blog Extracted")
        else:
            print(f"Failed to add messages. Status code: {response.status_code}")
            print("Response content:", response.text)
        st.session_state.url="Positive"


# if "pdf_search" not in st.session_state:
# st.session_state.
pdf_tool=pdf_tool()

# if "web_tool" not in st.session_state:
# st.session_state.
web_tool=web_tool()

# if "google_tool" not in st.session_state:
    # st.session_state.
google_tool=google_tool()

# if "prompt" not in st.session_state:
    # st.session_state.
prompt=get_prompt()

# Create the LangChain agent

# if "agent_executor" not in st.session_state:
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
agent = create_openai_tools_agent(llm, [google_tool, pdf_tool, web_tool],prompt)
    # st.session_state.
agent_executor = AgentExecutor(agent=agent, tools=[google_tool,pdf_tool, web_tool], verbose=True, handle_parsing_errors=True, max_iterations=5)
    # st.session_state.agent="available"
# Streamlit interface

if "messages" not in st.session_state:
   st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown (message["content"])

if query := st.chat_input("Enter your query:"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            messages = st.session_state.messages
            messages_str = ""
            for message in messages:
                if message["role"] == "user":
                    messages_str += f"User: {message['content']}///"
                elif message["role"] == "assistant":
                    messages_str += f"Assistant: {message['content']}///"
            print(messages_str)
            # refined_prompt=get_query_refiner_prompt(messages_str,query)
            # with st.expander("Refined_Prompt"):
            #     st.write(refined_prompt)
            
            result = agent_executor.invoke({"input": query})
            st.markdown(result['output'])
            st.session_state.messages.append({"role": "assistant", "content": result['output']})
            # st.write(result['output'])
