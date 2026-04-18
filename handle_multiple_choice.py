import re

def handle_multiple_choice_questions(all_text, qblock_end_marker):
    pattern = re.compile(r"^Heading\s+\d+\s+==>\s*multiple choice", re.IGNORECASE | re.MULTILINE)
    
    data = []
    for match in pattern.finditer(all_text):
        start_pos = match.end()
        end_pos = all_text.find(qblock_end_marker, start_pos)
        if end_pos == -1:
            end_pos = len(all_text)
        
        qblock = all_text[start_pos:end_pos]
        
        for q in filter(None, qblock.split("\n\n")):
            lines = list(filter(None, q.split("\n")))
            if not lines:
                continue
            
            correct_answer = None
            choices = []
            
            for l in lines[1:]:
                if l.startswith("***"):
                    correct_answer = l.replace("***", "").strip()
                    choices.append(correct_answer)
                else:
                    choices.append(l.strip())
            
            data.append({
                "question": lines[0],
                "choices": choices,
                "answer": correct_answer
            })
    
    return data