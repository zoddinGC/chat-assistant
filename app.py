# Python libraries
import streamlit as st
import json
import html

# Local imports
from modules.indexing_data import IndexingData
from modules.get_data import *
from modules.video_processing import transcript_video
from modules.get_api_key import *

# Function to retrieve bot response
def bot_response(user_input: str) -> dict:
    """
        This function will retrieve the bot response based on the LangChain 
        indexer.

        :param user_input: A string representing the query/user input
        :return: A dict with the bot response
    """
    return st.session_state.index.retrieve_context(user_input, st.session_state.raw_data, threshold=0.4)

def display_chat(role: str, txt: str):
    """
        This function display on screen a simulation of a chat where user 
        input is on green background and assistant/bot is on a gray background.

        :param role: A string representing the sender role
        :param txt: A string representing the text to be displayed
    """
    if role == 'Assistant':
        role = 'TEACHER'
        # Escape HTML text to display it correctly to user instead of using the markdown itself
        txt = html.escape(str(txt["response"]))
        st.markdown(f'<div style="background-color:#f1f0f0; padding:10px; border-radius:10px; margin-bottom:5px; max-width:70%;"><b>{role}</b>: {txt}</div>', unsafe_allow_html=True)
    elif role == 'User':
        st.markdown(f'<div style="background-color:#dcf8c6; padding:10px; border-radius:10px; margin-bottom:5px; max-width:70%; text-align:right; margin-left:auto;"><b>YOU</b>: {txt}</div>', unsafe_allow_html=True)

def disable_tab(condition:bool=True):
    """
        This function set the session state StreamLit's variable 'disabled_tab' 
        to True or False.

        :param condition: A boolean that will be setted in the 'disabled_tab'
    """
    # If the condition changes, the tab must be re-rendered
    if st.session_state.disabled_tab != condition:
        st.session_state.disabled_tab = condition
        st.rerun()


# ====================
# CREATE STREAMLIT APP
# ====================

# Initial state
if 'disabled_tab' not in st.session_state:
    st.session_state.disabled_tab = True

# Sidebar with navigation
st.sidebar.title("Navigation")
tabs = ["API Key", "Load Data", "Chat"]
tab_choice = st.sidebar.radio(
    "Go to",
    tabs,
    label_visibility='hidden',
    disabled=st.session_state.disabled_tab
)

# This tab represents where the user will add an OpenAI API Key
if tab_choice == 'API Key':
    st.title('API Key Manager')

    # Explain what this tab does
    st.markdown('Add your API Key to the .env file. With an API Key, the Chat responses are going to be better.')
    st.markdown('You can pick-up your key [clicking here](https://platform.openai.com/api-keys)')
    st.markdown('The navigation tabs will only be **allowed after a valid OpenAI API key** is inserted.')

    # Initialize session state if not already initialized
    if 'api_key' not in st.session_state:
        st.session_state.api_key = get_API()

    # Get user API Key
    actual_api_key = st.text_input('Write your OpenAI Key', value=st.session_state.api_key)

    # Test if the API Key is valid
    if actual_api_key:
        valid, message = test_openai_api_key(actual_api_key)
        if not valid:
            st.warning('This key is not valid. ' + message)
            disable_tab(condition=True)
        else:
            st.success('This key is valid.')

    # Update the .env file and session state if the key is valid
    if actual_api_key and valid:
        st.session_state.api_key = actual_api_key
        write_API(actual_api_key)
        st.info('API key updated successfully in .env file.')
        disable_tab(condition=False)

# Load Data iformation in Data Tab
elif tab_choice == "Load Data":
    st.title("Load Data")

    # Explain to user what this tab does
    st.markdown('Select where the context is located in GitHub. **You can skip this tab**, because if no info is provided, it will load a pre-indexed data from [this link](https://github.com/grupo-a/challenge-artificial-intelligence/tree/main/resources).')

    # Create variables to display messages to user
    error_message = 'This is not a valid URL.'
    success_message = 'Loaded successfully'
    
    # Load text from a GitHub URL
    txt = st.text_input('What is the text context GitHub URL?', value=None)
    if txt:
        try:
            txt_content = get_text_from_github(txt)
            st.session_state.txt_url = txt
            st.success(success_message)
        except:
            st.warning(error_message)

    # Load PDF from a GitHub URL
    pdf = st.text_input('What is the PDF context GitHub URL?', value=None)
    if pdf:
        try:
            pdf_content = get_pdf_from_github(pdf)
            st.session_state.pdf_url = pdf
            st.success(success_message)
        except:
            st.warning(error_message)

    # Load video from a GitHub URL
    video = st.text_input('What is the video context GitHub URL?', value=None)
    if video:
        try:
            video_path = 'data/video/default_video.mp4'
            # Download and save video
            save_video_from_github(video, save_path=video_path)

            # Transcript the video to text
            video_content, segments = transcript_video(video_path, model_performance='balanced')
            st.session_state.video_url = video

            st.success(success_message)
        except Exception as e:
            st.warning(error_message)

    # Check if all variables are equal to None
    variables = [txt, pdf, video]

    # Disabled tabs with
    if any(variables) and not all(variables) and not st.session_state.disabled_tab:
        disable_tab(condition=True)
    elif all(variables) and 'video_url' in st.session_state:
        if video_content and segments:
            # Create data dict to insert into library
            data={
                txt_content['text']:'text',
                pdf_content['text']:'pdf',
                video_content:'video',
            }

            # Initialize Index class with api key if provided
            st.session_state.index = IndexingData(api_key=st.session_state.api_key)
            st.session_state.index.create_library(data)

            # Create a raw data variable to check where the information is located
            st.session_state.raw_data = {
                'text': txt_content,
                'pdf': pdf_content,
                'video': segments,
            }

            # Enable tab changing
            disable_tab(condition=False)

# Chat tab
elif tab_choice == "Chat":
    st.title("Teacher Assistant")

    # Show to user where the context is located
    if 'video_url' not in st.session_state:
        st.markdown('The Teacher Assistant context is based on [this link](https://github.com/grupo-a/challenge-artificial-intelligence/tree/main/resources)')
    else:
        st.markdown('The Teacher Assistant context is based on these links:')
        st.markdown(
            f'[Text Context]({st.session_state.txt_url}) | [PDF Context]({st.session_state.pdf_url}) | [Video Context]({st.session_state.video_url})'
        )

    # Check if Index was initialized
    if 'index' not in st.session_state:
        st.session_state.index = IndexingData(api_key=st.session_state.api_key, path='data/libraries/first_approach')

    if 'raw_data' not in st.session_state:
        # Load dictionary from a .json file
        with open('data/raw_data.json', 'r') as json_file:
            st.session_state.raw_data = json.load(json_file)
    
    # Display the chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        role = message['role'].title()
        display_chat(role=role, txt=message['message'])

    # Separate in two columns, one for user input and another to send button
    # This allows send button be in the same line of user input
    col1, col2 = st.columns([5,1], vertical_alignment='bottom')

    # User input
    with col1:
        # Input by user
        user_input = st.text_input("You: ", key="user_input")
    
    # Send button
    with col2:
        if st.button("Send"):
            if user_input:
                # Append user message to chat history
                st.session_state.messages.append({'role': 'user', 'message': user_input})

                # Generate bot response and append to chat history
                response = bot_response(user_input)
                st.session_state.messages.append({'role': 'assistant', 'message': response})
                
                # Clear input box
                user_input = None

                # Rerun to display messages
                st.rerun()
                