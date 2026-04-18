from docx.api import Document
from handle_multiple_choice import handle_multiple_choice_questions
from handle_definition import handle_definition_questions
import json

doc = Document("sample.docx")

final_data = {
    "multiple_choice": [],
    "definition": [],
    "essay": [],
    "true/false": []
}

# Merge all text as string
qblock_end_marker = "<!--qblock--!>"
all_text = []
for para in doc.paragraphs:
    text = para.text
    if para.style.name.startswith("Heading"):
        text = qblock_end_marker + "\n" + para.style.name + " ==> " + para.text
    all_text.append(text)
all_text = "\n".join(all_text)

# Handle multiple choice questions
final_data["multiple_choice"] = handle_multiple_choice_questions(all_text, qblock_end_marker)

# Handle definition
final_data["definition"] = handle_definition_questions(all_text, qblock_end_marker)

# TODO: Handle essay
# TODO: Handle true/false

# Write to JSON
with open("final-data.json", "w") as f:
    json.dump(final_data, f, indent=4)

print("Data written to JSON")