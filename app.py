import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun , DuckDuckGoSearchRun  , PubmedQueryRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper , PubMedAPIWrapper
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

pumed_wrapper = PubMedAPIWrapper(top_k_results=1, doc_content_chars_max=200)
pubmed = PubmedQueryRun(api_wrapper = pumed_wrapper)


search = DuckDuckGoSearchRun(name = "Search")

st.title("🔎 LangChain - Chat with search")
"""
This app uses a LangChain agent to answer questions using multiple search tools.
"""

## sidebar settings
st.sidebar.markdown("### ⚙️ Settings")
st.sidebar.markdown("---")

# API Key input with better styling
st.sidebar.markdown("#### 🔐 API Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API key:" , type = "password", help="Your API key is required to use the AI assistant")

# Clear chat button with better spacing
st.sidebar.markdown("---")
st.sidebar.markdown("#### 💬 Chat Management")
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]
    
    st.rerun()

# Status indicators
st.sidebar.markdown("---")
st.sidebar.markdown("#### 📊 Status")

if api_key:
    st.sidebar.success("✅ API key validated! Ready to chat.")
else:
    st.sidebar.warning("⚠️ Please enter your API key to start.")

# Additional info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("#### ℹ️ About")
st.sidebar.markdown("""
This AI assistant uses:
- **GPT-4** for intelligent responses
- **Multi-source search** for accurate information
- **Real-time data** from trusted sources
""")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 💡 Tips")
st.sidebar.markdown("""
- Ask questions in natural language
- Request specific sources if needed
- Use clear and concise queries
- Try different phrasings for better results
""")


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
        tools=[search,arxiv,wiki , pubmed]

        search_agents = initialize_agent(tools , llm , agent = AgentType.OPENAI_FUNCTIONS , handling_parsing_errors=True)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts = False)
            response = search_agents.run(st.session_state.messages , callbacks = [st_cb])
            st.session_state.messages.append({"role" : "assistant" , "content" : response})
            st.write(response)

