import re

def handle_definition_questions(all_text, qblock_end_marker):
    pattern = re.compile(r"^Heading\s+\d+\s+==>\s*definition", re.IGNORECASE | re.MULTILINE)
    
    data = []
    for match in pattern.finditer(all_text):
        start_pos = match.end()
        end_pos = all_text.find(qblock_end_marker, start_pos)
        if end_pos == -1:
            end_pos = len(all_text)
        
        qblock = all_text[start_pos:end_pos]
        
        for q in filter(None, qblock.split("\n")):
            data.append({
                "question": q,
            })
    
    return data