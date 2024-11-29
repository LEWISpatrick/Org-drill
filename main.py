import pdfplumber
import re

# Step 1: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'  # Accumulate text from each page
    return text

# Step 2: Identify questions, hints, and answers
def extract_questions_hints_answers(text):
    # Define refined regex patterns to capture questions, hints, and answers
    question_pattern = r"\d+\.\s?([a-zA-Z0-9\s]+(?:\s[a-zA-Z0-9\s]+)?)"  # Captures questions like 1., 2., 3.a, 4.b
    hint_pattern = r"Hint[:]*\s*(.*?)(?=\n|$)"  # Captures Hint: followed by any hint text
    answer_pattern = r"(Answer|Solution)[:]*\s*(.*?)(?=\n|$)"  # Captures Answer or Solution with the answer text
    
    # Extracting questions, hints, and answers
    questions = re.findall(question_pattern, text)
    hints = re.findall(hint_pattern, text) or ["n/a"] * len(questions)  # Default to 'n/a' if no hints
    answers = re.findall(answer_pattern, text) or ["n/a"] * len(questions)  # Default to 'n/a' if no answers
    
    # Structuring the data into a list of dictionaries containing question, hint, and answer
    data = []
    for q, h, a in zip(questions, hints, answers):
        data.append({"question": q.strip(), "hint": h.strip(), "answer": a[1].strip() if isinstance(a, tuple) else a.strip()})

    return data

# Step 3: Generate Org file from structured data
def generate_org_file(data, output_path):
    with open(output_path, 'w') as file:
        for idx, item in enumerate(data, 1):
            # Write each question, hint, and answer in the Org file format
            file.write(f"* Question {idx}\n")
            file.write(f"** Question\n{item['question']}\n")
            file.write(f"** Hint\n{item['hint']}\n")
            file.write(f"** Answer\n{item['answer']}\n\n")

# Main function to execute the steps
def main(pdf_path, output_path):
    # Step 1: Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Extract questions, hints, and answers
    data = extract_questions_hints_answers(text)
    
    # Step 3: Generate the Org file
    generate_org_file(data, output_path)

# Run the program with the provided PDF
if __name__ == "__main__":
    pdf_path = "Anany Levitin - Introduction to The Design and Analysis of Algorithms Solution Manual (2012) (2).pdf"  # Replace with the actual PDF path
    output_path = "output.org"  # Replace with the desired output file path
    main(pdf_path, output_path)
