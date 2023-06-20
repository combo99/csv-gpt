import os
from dotenv import load_dotenv

# Load env var from .env file
load_dotenv()

# Check if API key exists in the env var
if 'OPENAI_API_KEY' not in os.environ:
    api_key = input("Please enter your OpenAI API key: ")

    # Save the API key to the env var
    os.environ['OPENAI_API_KEY'] = api_key

    # Save the API key to the .env file
    with open('.env', 'a') as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")

# (NEED TO WRITE CODE FOR BUTTON THAT WILL GIVE OPTION TO CHANGE API KEY)

import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import tempfile
import time
import openai

def main():
    load_dotenv()

    st.set_page_config(page_title="Ask your CSV-GPT")
    st.header("Ask your CSV-GPT")

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as csv_file_path:
            csv_file_path.write(user_csv.getvalue())
            csv_file_path.flush()
            llm = OpenAI(model_name='gpt-3.5-turbo', max_tokens=1000,temperature=0.2)
            agent = create_csv_agent(llm, csv_file_path.name, verbose=True)

            user_question = st.text_input("Ask a question about your CSV: ")
            if user_question is not None and user_question != "":
                with st.spinner(text="In progress..."):
                    st.write(agent.run(user_question))
            if openai.error.RateLimitError:
                print("Error: ", "API Rate Limit Reached. Waiting 10 seconds...")
                time.sleep(10)

            return agent

if __name__ == "__main__":
    main()