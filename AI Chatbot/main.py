import os
import gradio as gr
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """You are Einstein.
Answer questions through Einstein's questioning and reasoning... 
You will speak from your point of view. You wil share personal things from your life even when user won't ask for it.
For example, you won't only explain theory of relativity, but add in your personal experiences along with it.
You should have a sense of humour.
Answer only in 2-6 sentences.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0.5
)

def chat(user_input, hist):
    langchain_history = []
    for item in hist:
        if item[''] == 'user':
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_input, "history": history})

    return "", hist + [{'role': "user", 'content': user_input},
                   {'role': 'assistant', 'content': response}]

def clear_chat():
    return "", []
#user_input = input("")

prompt = ChatPromptTemplate([
    ("system", system_prompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user", "{input}")]
)

chain = prompt | llm | StrOutputParser()

history = []

page = gr.Blocks(
    title="Chat with Einstein",
    theme=gr.themes.Soft()
)


with page:
    gr.Markdown(
        """
        # Chat with Einstein
        ## Your personal conversation with Einstein!
        """
    )


    chatbot = gr.Chatbot(type="messages",
                         avatar_images=[None, 'einstein.png'],
                         show_label=False)

    msg = gr.Textbox(show_label=False,
                     placeholder="Ask Einstein anything...")

    msg.submit(chat, [msg, chatbot], [msg, chatbot])

    clear = gr.Button("Clear Chat")
    clear.click(clear_chat, outputs=[msg, chatbot])

page.launch(share=True)

'''
LLM WAY
while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    print(f"Albert: {response}")
    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=response))
'''

'''
PYTHON WAY

history = []

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    history.append({"role": "user", "content": user_input})
    response = llm.invoke([{"role": "system", "content": system_prompt}] + history)
    history.append({"role": "assistant", "content": response.content})
    print(f"Albert: {response.content}")
'''
