import requests
import ast
from driver import get_code_summary

# 1. Fetching the File:
def fetch_file_from_github(repo_owner, repo_name, branch, file_path):
    base_url = "https://raw.githubusercontent.com"
    file_url = f"{base_url}/{repo_owner}/{repo_name}/{branch}/{file_path}"
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error {response.status_code}: Unable to fetch the file.")
        return None

# 2. Splitting the File:
def extract_functions_from_code(code_content):
    tree = ast.parse(code_content)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    function_bodies = [code_content[node.lineno - 1:node.end_lineno] for node in functions]
    return function_bodies

# 3. Summarizing using the AI model:
def ai_summarizer(content):
    summary = get_code_summary(content)
    return summary

def summarize_large_file(code_content):
    functions = extract_functions_from_code(code_content)
    summaries = [mock_ai_summarizer(func) for func in functions]
    return summaries

# 4. Aggregating Summaries:
def aggregate_summaries(summaries):
    return " | ".join(summaries)

# Parsing GitHub URL:
def parse_github_url(url):
    segments = url.split('/')
    if 'github.com' not in segments or len(segments) < 6:
        print("Invalid GitHub URL.")
        return None, None, None, None

    repo_owner = segments[3]
    repo_name = segments[4]
    branch = segments[6]
    file_path = "/".join(segments[7:])
    
    return repo_owner, repo_name, branch, file_path

# Main execution:
def main():
    url = input("Please enter the GitHub URL of the file: ")
    repo_owner, repo_name, branch, file_path = parse_github_url(url)

    if not repo_owner or not repo_name or not branch or not file_path:
        print("Failed to parse the provided URL.")
        return

    code_content = fetch_file_from_github(repo_owner, repo_name, branch, file_path)
    if code_content:
        # Summarize the fetched code content using AWS Bedrock AI
        summary = get_code_summary(code_content)
        print(f"Summary: {summary}")
    else:
        print("Failed to fetch the file content.")

if __name__ == "__main__":
    main()
