from pathlib import Path
from ollama import chat


question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

selected_files = [
    ##Use only the files that are relevant to the question.
    "knowledge/wifi_setup.txt",
    "knowledge/password_changes.txt",
    "knowledge/service_status.txt"
]


context = ""

## Write a for loop to go through all the files in selected_files and read their contents into the context variable.
for file in selected_files:
    file_path = Path(file)
    if file_path.exists():
        with open(file_path, "r") as f:
            context += f.read() + "\n"
    else:
        print(f"File {file} does not exist.")

## Call Qwen with the student's question and the context you created above.
promot = f"Based on the following university information, solve the student's problem.\n\nUniversity Information:\n{context}\n\nStudent Problem:\n{question}"
response = chat(
    model="qwen3:8b",
    messages=[{"role": "user", "content": promot}],
)


print(
    "Context characters:",
    len(context)
)
print(response.message.content)