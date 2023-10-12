import ast
from mccabe import get_code_complexity
import spacy
from transformers import pipeline

# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load the question-answering model
qa_model = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# ...

# Function to analyze a Python file including NLP analysis and question-answering
def analyze_python_file(file_path, question=None):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        # Parse the code using the Abstract Syntax Tree (AST)
        parsed_code = ast.parse(code)

        # Get comments and docstrings
        doc = nlp(code)
        comments = [token.text for token in doc if token.is_comment]
        docstrings = [node.value.s for node in ast.walk(parsed_code) if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)]

        # Create a dictionary with analysis results as before
        analysis_result = {
            "Total Lines": total_lines,
            "Number of Functions": num_functions,
            "Function Names": functions,
            "Code Complexity": complexity,
            "Comments": comments,
            "Docstrings": docstrings
        }

        if question:
            # Use the question-answering model to answer the user's question
            answer = qa_model(question=question, context=code)
            analysis_result["Answer"] = answer["answer"]

        return analysis_result
    except Exception as e:
        return {"Error": str(e)}

# ...

# Example of how to ask a question about the code
if __name__ == "__main__":
    file_path = "your_python_file.py"  # Replace with the path to your Python file
    analysis_result = analyze_python_file(file_path, question="What does the function 'example_function' do?")
    print(analysis_result)
