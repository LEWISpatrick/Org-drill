import re
import pdfplumber


# Step 1: Extract and save raw text for analysis
def extract_text_from_pdf(pdf_path, output_path="raw_text.txt"):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    
    # Save the raw text to a file for analysis
    with open(output_path, 'w') as file:
        file.write(text)
    
    print(f"Raw text extracted and saved to {output_path}.")
    return text


# Step 2: Split text into sections (Exercises, Hints, Solutions)
def split_into_sections(text):
    # Use section headers to divide the text
    sections = re.split(r"(Exercises.*?|Hints.*?|Solutions.*?)\n", text, flags=re.DOTALL)
    sections_dict = {"exercises": "", "hints": "", "solutions": ""}
    current_section = None

    for section in sections:
        section_lower = section.lower()
        if "exercises" in section_lower:
            current_section = "exercises"
        elif "hints" in section_lower:
            current_section = "hints"
        elif "solutions" in section_lower:
            current_section = "solutions"
        else:
            if current_section:
                sections_dict[current_section] += section.strip() + "\n"

    return sections_dict


# Step 3: Extract numbered entries (Questions, Hints, Solutions)
def extract_numbered_entries(section_text):
    pattern = r"(\d+(\.\d+)?[a-zA-Z]?\. .*?(?:\n\s{2,}.*?)*)(?=\n\d+|\Z)"  # Matches numbered entries
    entries = re.findall(pattern, section_text, re.DOTALL)
    return [entry[0].strip() for entry in entries]  # Return the matched text


# Step 4: Link questions with hints and solutions
def link_questions_hints_answers(exercises, hints, solutions):
    data = []

    for idx, question in enumerate(exercises):
        question_number = re.match(r"\d+(\.\d+)?[a-zA-Z]?", question)  # Extract question number
        if question_number:
            question_number = question_number.group()
        else:
            question_number = f"{idx + 1}"  # Fallback to sequential indexing

        # Match hints and solutions by question number
        hint = next((h for h in hints if h.startswith(question_number)), "n/a")
        solution = next((s for s in solutions if s.startswith(question_number)), "n/a")

        data.append({"question": question, "hint": hint, "answer": solution})

    return data


# Step 5: Generate Org-Drill file
def generate_org_file(data, output_path):
    with open(output_path, 'w') as file:
        for idx, item in enumerate(data, 1):
            file.write(f"* Question {idx}\n")
            file.write(f"** Question\n{item['question']}\n")
            file.write(f"** Hint\n{item['hint']}\n")
            file.write(f"** Answer\n{item['answer']}\n\n")


# Main Function
def main(pdf_path, output_path="output.org"):
    # Extract raw text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Split text into sections
    sections = split_into_sections(text)
    exercises = extract_numbered_entries(sections["exercises"])
    hints = extract_numbered_entries(sections["hints"])
    solutions = extract_numbered_entries(sections["solutions"])

    # Link questions with hints and solutions
    data = link_questions_hints_answers(exercises, hints, solutions)

    # Generate Org-Drill file
    generate_org_file(data, output_path)
    print(f"Org-Drill file created at: {output_path}")


if __name__ == "__main__":
    pdf_path = "Anany Levitin - Introduction to The Design and Analysis of Algorithms Solution Manual (2012) (2).pdf"
    main(pdf_path)
