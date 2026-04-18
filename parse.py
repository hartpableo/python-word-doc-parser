from docx.api import Document
from handle_multiple_choice import handle_multiple_choice_questions

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

# Handle multiple choice questions
handle_multiple_choice_questions(all_text, qblock_end_marker)