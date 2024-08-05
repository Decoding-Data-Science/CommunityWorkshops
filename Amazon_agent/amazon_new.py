import streamlit as st
import requests

API_KEY = "MXmLRX26EZVO0qcgxcE4Wtjlac5sXREZ"
EXTERNAL_USER_ID = "66a88d40ffe7964099ac3934"

def create_chat_session():
    response = requests.post(
        'https://api.on-demand.io/chat/v1/sessions',
        headers={'apikey': API_KEY},
        json={'pluginIds': [], 'externalUserId': EXTERNAL_USER_ID}
    )
    return response.json()['data']['id']

def submit_query(session_id, query):
    response = requests.post(
        f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query',
        headers={'apikey': API_KEY},
        json={
            'endpointId': 'predefined-openai-gpt4o',
            'query': query,
            'pluginIds': ['plugin-1716334779'],
            'responseMode': 'sync'
        }
    )
    return response.json()

def prompt_engineering(user_query):
    return f"You are an Amazon shopping assistant. The user query is: {user_query}. Provide detailed product recommendations, including name, price, RAM, storage, rating, and a correct Amazon product link."

def main():
    st.markdown("<h1 style='text-align: center;'>Amazon Shopping Assistant</h1>", unsafe_allow_html=True)

    # Create session ID in the background
    if 'session_id' not in st.session_state:
        try:
            st.session_state['session_id'] = create_chat_session()
        except Exception as e:
            st.error(f"Error creating chat session: {str(e)}")
            return

    # Layout: large images on the left, chat on the right
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("amazon_logo.png", width=200)  # Ensure the image is in the project folder
        st.image("your_image.png", width=200)
        st.image("dds_logo.png", width=200)
        

    with col2:
        user_query = st.text_input("Enter your shopping query", key="query_input", on_change=lambda: submit_on_enter())

        def submit_on_enter():
            if user_query:
                with st.spinner("Submitting query..."):
                    try:
                        engineered_query = prompt_engineering(user_query)
                        response = submit_query(st.session_state['session_id'], engineered_query)
                        answer = response.get('data', {}).get('answer', 'No answer found.')
                        st.markdown(answer, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error submitting query: {str(e)}")
            else:
                st.warning("Please enter a shopping query.")

        if st.button("Submit Query"):
            submit_on_enter()

if __name__ == "__main__":
    main()
