# Chat Assistant
Welcome to Chat Assistant with context. This repository is part of a challenge.


# Installation
Copy the files to your local machine
`git clone https://github.com/zoddinGC/chat-assistant`

Create a virtual environment using **Python 3.9.13**
`python -m venv env`

Activate the virtual environment
`env/Scripts/activate.ps1`

Install the required dependencies
`pip install -r requirements.txt`

After this, all required files will be available on your machine and local repository. Remember to select the right intrepeter in your IDE.

# How to Run
To run the application, all you need is to use this command in the IDE terminal:
`streamlit run app.py`

Then, the application will be running in your **default browser**.

# How to Use
The application has 3 navigation tabs:

 - API Key -> **required**
 - Load Data -> *optional*
 - Chat -> use

## API Key
The first tab is where you have to insert your OpenAI API Key available on [OpenAI Platform](https://platform.openai.com/api-keys).

After getting your key and inserting it in the application, a function will be called to check if the given key is valid or not. You will **only access** other tabs if a **valid key** is **inserted**.

## Load Data
This tab is optional. If you give any URL, you must enter all other 2 URLs in order to proceed to other tabs.

After giving a URL, the application will download the data to use in Chat tab.

**Only GitHub URL are allowed.**

## Chat
This tab is where you will use the Chat Bot. Powered with OpenAI most recent model, the appication will answer the questions based on the context provided by the URL content.