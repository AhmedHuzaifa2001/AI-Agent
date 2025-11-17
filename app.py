import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun , DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain.agents import initialize_agent , AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os
from dotenv import load_dotenv
load_dotenv()


## Arxiv and wikipedia Tools
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki=WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

search = DuckDuckGoSearchRun(name = "Search")

st.title("🔎 LangChain - Chat with search")
"""
This app uses a LangChain agent to answer questions using multiple search tools.
"""

## sidebar settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your api key: " , type = "password")

if api_key:
    st.sidebar.success("API key is ok! You can now chat. 👍")
else:
    st.sidebar.warning("Please enter your API key to start. 🔑")


if api_key:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role" : "assistant" , "content" : "Hi,I'm a chatbot who can search the web. How can I help you?"}
        ]


    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    if prompt:= st.chat_input(placeholder = "what is machine Learning?"):
        st.session_state.messages.append({"role":"user" , "content":prompt})
        st.chat_message("user").write(prompt)

        llm = ChatOpenAI(api_key = api_key , model = "gpt-4" , streaming = True)
        tools=[search,arxiv,wiki]

        search_agents = initialize_agent(tools , llm , agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION , handling_parsing_errors=True)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts = False)
            response = search_agents.run(st.session_state.messages , callbacks = [st_cb])
            st.session_state.messages.append({"role" : "assistant" , "content" : response})
            st.write(response)

