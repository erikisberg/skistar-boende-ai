import streamlit as st
import openai
from openai import OpenAI, AssistantEventHandler

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=st.secrets["openai_api_key"])

# App title
st.title('POC - Skistar Boende AI')

# Text input
user_input = st.text_input("Beskriv vilket boende du är ute efter:")

# Function to handle responses from the assistant
class EventHandler(AssistantEventHandler):
    def on_text_created(self, text):
        st.write(f"Assistant: {text}")

    def on_text_delta(self, delta, snapshot):
        st.write(delta.value, end="")

    def on_tool_call_created(self, tool_call):
        st.write(f"Tool call: {tool_call.type}")

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            st.write("\n\nOutput: ", end="")
            for output in delta.code_interpreter.outputs:
                if output.type == "logs":
                    st.write(output.logs)

# Button to send the text to the API
if st.button('Skicka'):
    if user_input:
        # Create a Thread
        thread = client.beta.threads.create()

        # Add a Message to the Thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Create and Stream a Run
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id="asst_6yua7Cz9m55zZ0NEBWZp5BDw",  # Use your Assistant ID
            instructions="Provide accommodation options",
            event_handler=EventHandler()
        ) as stream:
            stream.until_done()
    else:
        st.error("Please enter some text before sending.")
