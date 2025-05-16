import streamlit as st
from openai import OpenAI

# Show title and description.
# st.title("💬 Chatbot")
# st.write(
    
#     "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
#     "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
#     "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
# )

with open('./style.css') as f:
    css = f.read()

st.html(f'<style>{css}</style>')

st.html(
    """
    <div style="background-color: white; color: black;">
    
      <header class="nav_hidden">
        <a href="/"><img src="https://treedioms.web.app/icons/favicon/favicon1.svg" alt="Treedioms Favicon">
            <h1>Treedioms</h1>
            <span class="header_subtitle">online idiom dictionary</span>
        </a>

        <div id="nav_toggle_container">
            <button id="account_link"><a href="/account"><i class="fa-solid fa-user"></i></a></button>
            <button id="nav_toggle" aria-label="Toggle navigation bar"><i class="fa-solid fa-list-ul"></i></button>
        </div>
    </header>
    <nav></nav>

    <div class="search_box_container">
        <div id="search_box">
            <div id="search_autocomplete">
                <label>
                    <form autocomplete="off">
                        <input id="search" type="text" placeholder="Search idioms, music artist or category here...">
                    </form>
                </label>
            </div>
            <button id="clear" aria-label="Clear search value"> &times;</button>
        </div>
    </div>

    <div id="main_links">
        <div class="main_link_container">
            <a href="/library" rel="noopener noreferrer">
                <i class="fa-solid fa-sitemap"></i> Library
            </a>
        </div>
        <div class="main_link_container">
            <a href="/top_idioms" rel="noopener noreferrer">
                <i class="fa-solid fa-trophy"></i> Top idioms
            </a>
        </div>
        <div class="main_link_container">
            <a href="https://www.facebook.com/treedioms/" rel="noopener noreferrer" target="_new_tab_f">
                <i class="fa-brands fa-facebook"></i> Facebook
            </a>
        </div>
        <div class="main_link_container">
            <a href="https://www.instagram.com/treedioms/" rel="noopener noreferrer" target="_new_tab_i">
                <i class="fa-brands fa-instagram"></i> Instagram
            </a>
        </div>

    </div>

    <h2>💬 Treedioms Chatbot</h2>
    <p>Welcome to a Treedioms Chatbot, where you can learn about idioms</p>


    <div id="result"></div>

    </div>
    
    """
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ask anything related to idioms..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
