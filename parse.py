from docx.api import Document
import re, json

doc = Document("sample.docx")

# Merge all text as string
qblock_end_marker = "<!--qblock--!>"
all_text = []
for para in doc.paragraphs:
    text = para.text
    if para.style.name.startswith("Heading"):
        text = qblock_end_marker + "\n" + para.style.name + " ==> " + para.text
    all_text.append(text)
all_text = "\n".join(all_text)

# Find "Multiple Choice" questions block
multiple_choice_start_pos = re.search(r"^Heading\s+\d+\s+==>\s*multiple choice", all_text, re.IGNORECASE | re.MULTILINE).end()
multiple_choice_end_pos = all_text.find(qblock_end_marker, multiple_choice_start_pos)
qblock = all_text[multiple_choice_start_pos:multiple_choice_end_pos]
qblock = filter(None, qblock.split("\n\n"))

# Save data
data = {
    "multiple_choice": []
}
correct_answer = None
for q in qblock:
    lines = list(filter(None, q.split("\n")))
    correct_answer = None
    choices = []
    
    for l in lines[1:]:
        if l.startswith("***"):
            correct_answer = l.replace("***", "").strip()
            choices.append(correct_answer)
        else:
            choices.append(l.strip())
            
    data["multiple_choice"].append({
        "question": lines[0],
        "choices": choices,
        "answer": correct_answer
    })

# Write to JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)  

print("Data written to JSON")