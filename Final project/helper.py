import re

def extract_characters_info(text):
    characters_info = {}
    pattern = r'([A-Za-z\s]+)\s*\(([^)]+)\)\s*Voiced by:\s*([^;]+?\([^)]*\))(.*?)(?=\n|$)'

    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        name, japanese_name, voice_actors, details = match
        characters_info[name.strip()] = {
            "Japanese Name": japanese_name.strip(),
            "Voice Actor": voice_actors.strip(),
            "Details": details.strip()
        }
    
    return characters_info

results = []
characters_info = extract_characters_info(results['Angel Beats!']['Characters'])
# print(characters_info)
for character, info in characters_info.items():
    print(f"Character: {character}")
    print(f"  Japanese Name: {info['Japanese Name']}")
    print(f"  Voice Actor: {info['Voice Actor']}")
    print(f"  Details: {info['Details']}")
    print("\n" + "-"*40 + "\n")  # Separator for readability