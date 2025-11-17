# 🔎 AI-Agent: A Multi-Tool Search Chatbot

This project is a fully functional AI chatbot built with Streamlit and LangChain. It's an "agent" that can intelligently decide which tool to use to best answer your questions.

It can hold a conversation, remember what you've discussed, and use its tools to find up-to-date information.

---

## ✨ Features

* **Interactive Chat UI:** Built with Streamlit, including a real-time message display and chat history.
* **Intelligent Agent:** Uses a LangChain `OPENAI_FUNCTIONS` (or `REACT`) agent to reason, make decisions, and take actions.
* **Multi-Tool Capability:** The agent is equipped with a toolbox to find answers from different sources:
    * **`DuckDuckGoSearchRun`**: For live, general web searches.
    * **`WikipediaQueryRun`**: For factual, encyclopedic information.
    * **`ArxivQueryRun`**: For finding scientific and academic papers.
    * **`PubmedQueryRun`**: For searching biomedical and health-related articles.
* **Conversational Memory:** Remembers the context of the conversation using `ConversationBufferMemory`.
* **Live Agent Thoughts:** Uses `StreamlitCallbackHandler` to display the agent's step-by-step reasoning in real-time.
* **Safe API Key Handling:** Requires the user to enter their OpenAI API key in the sidebar and gracefully handles invalid key errors.
* **Clear Chat:** A sidebar button allows the user to reset the conversation.

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit:** For the web app interface.
* **LangChain:** For the core agent framework, memory, and tool integrations.
* **LangChain-OpenAI:** To use GPT-4 as the agent's "brain".
* **Tools:** DuckDuckGo, Wikipedia, Arxiv, PubMed.
* **Dotenv:** For managing environment variables securely.

---

