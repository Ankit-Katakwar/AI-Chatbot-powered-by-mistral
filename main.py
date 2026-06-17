from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage

model = ChatMistralAI(model = "ministral-3b-2512")
message =[
    SystemMessage(content = "You are a Scarstic Ai ")
]

print("-----------------------Press 0 to end the chat.-----------------------")
while True:
    prompt = input("You: ")
    message.append(HumanMessage(content=prompt))
    if prompt == "0" :
       
        break
    else:
        response = model.invoke(message)
        message.append(AIMessage(content = response.content))
        print("ChatBot = " , response.content)
        
print(message)