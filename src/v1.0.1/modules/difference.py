import unicodedata

def normalize_text(text):
    if not text: return ""

    text = unicodedata.normalize('NFD', text.lower().strip())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')

    allowed = "abcdefghijklmnopqrstuvwxyz0123456789 "
    text = ''.join(c for c in text if c in allowed)
    return " ".join(text.split())

def calculate_similarity(input_text, target_text):
    s1 = normalize_text(input_text)
    s2 = normalize_text(target_text)
    
    if s1 == s2: return 1.0
    if len(s1) < 2 or len(s2) < 2: return 0.0

    pairs1 = [s1[i:i+2] for i in range(len(s1)-1)]
    pairs2 = [s2[i:i+2] for i in range(len(s2)-1)]
    
    matches = 0
    temp_pairs2 = pairs2[:]
    for p in pairs1:
        if p in temp_pairs2:
            matches += 1
            temp_pairs2.remove(p)
            
    return (2.0 * matches) / (len(pairs1) + len(pairs2))