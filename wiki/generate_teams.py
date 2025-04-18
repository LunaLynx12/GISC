import os

teams = {
    "Splunk": [
        "Jarcau Stefan-Cristan",
        "Oprea Ionut-Alexandru",
        "Popa Ana Maria",
        "Stanculescu Daniel",
        "Gavrila Iulian-Gabriel",
        "Andrei Mihai Alexandru",
        "Micu Raluca",
        "Patrascu Nicolae Adrian"
    ],
    "Attack Scripts": [
        "Petre Radu Catalin",
        "Ginerica Alexandru",
        "Maftei David",
        "Posea Alina",
        "Andrei Chiper",
        "Jose Zamora",
        "Beatrice Kateule",
        "Caprarin Radu"
    ],
    "Infrastructure": [
        "Spunei Razvan-Sorin",
        "Grigorescu Stefan",
        "Cucu Antonia",
        "Neagu Alexandra",
        "Mitirita George-Claudiu",
        "Ciubotaru Radu Stefan",
        "Stefan Marian",
        "Raul Andreeas Horvat"
    ]
}

base_path = "./wiki"

notes_content = "# Notes\n\nThis file contains general notes for the task."
research_content = "# Research\n\nThis file contains research summaries and references."

for team_name, members in teams.items():
    team_path = os.path.join(base_path, team_name)
    os.makedirs(team_path, exist_ok=True)
    
    for member in members:
        member_path = os.path.join(team_path, member)
        os.makedirs(member_path, exist_ok=True)

        notes_path = os.path.join(member_path, "notes.md")
        research_path = os.path.join(member_path, "research.md")

        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(notes_content)

        with open(research_path, "w", encoding="utf-8") as f:
            f.write(research_content)

print("Folders and files created successfully.")
