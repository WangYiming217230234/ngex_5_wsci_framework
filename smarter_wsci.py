from pathlib import Path
from ollama import chat
import json



question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

## WRITE ##
service_status = {
    "wifi": "operational"
}

state = {
    "problem": question,
    "wi_fi status": "operational",
    "wi-fi_check": True
}

with open("state.json", "w") as file:
    json.dump(
        state,
        file,
        indent=2
    )

with open("state.json", "r") as file:
    state = json.load(file)

print(state)


## SELECT CONTEXT FILES BASED ON QUESTION
## Create the function that takes the student's question, takes some keywords and chooses the relevant files from the knowledge base. Return a list of the selected files.
## For example, if the question has the kyeword "print" or "printer", then the function should return the file "knowledge/printer_setup.txt" in a list.
def select_context(question):
    files_to_read = []
    q = question.lower()
    if "wi_fi" in q or "wifi" in q:
        files_to_read.append("knowledge/wifi_setup.txt")
        files_to_read.append("knowledge/service_status.txt")
    if "password" in q:
        files_to_read.append("knowledge/password_changes.txt")
    return list(set(files_to_read)) 


selected_files = select_context(question)

## READ SELECTED FILES and add their contents to the context variable.
context = ""
for file in selected_files:
    file_path = Path(file)
    if file_path.exists():
        with open(file_path, "r") as f:
            context += f.read() + "\n"
    else:
        print(f"File {file} does not exist.")


## 
## COMPRESS CONTEXT
## Add logic to compress the context from above by calling Qwen with "context" and the "question" as the parameter
## The response from Qwen should be the compressed context. Store it in a variable called "compressed_context" 

def compress_context(context, question):
    compass_prompt = f"Compress the following context while retaining the essential information relevant to the student's problem.\n\nContext:\n{context}\n\nStudent Problem:\n{question}"
    response = chat(
        model="qwen3:8b",
        messages=[{"role": "user", "content": compass_prompt}],
    )
    return response.message.content



## Print the length of the compressed context
compressed_context = compress_context(context, question)
print(len(compressed_context))

## Now, call Qwen again with the compressed context and the student's question. Store the response in a variable called "response" and print the response from Qwen.
## Ensure the model produces a structured output 
final_prompt = f"""
System State:
Wi-Fi Service Status: {state.get('wi_fi status')}

Relevant Information:
{compressed_context}

Student Problem:
{question}

Please provide a structured solution to the student.
"""

response = chat(
    model="qwen3:8b",
    messages=[{"role": "user", "content": final_prompt}],
)



## WRITE the above output in an artifact called "state"
print("\nFinal Output:")
print(response.message.content)
## Update the rest of the code so that it uses the "state" artifact as part of the context. 
## It is important to ensure that the model uses only the relevant parts from the "state" artifact and not the entire artifact.
## For this, you may have to think of a good structure for the "state" artifact and how to use it in the context.


