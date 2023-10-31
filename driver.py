import os
import json
import sys
from cli.bedrock.bedrock import run_model, parse_output

# Setting the AWS_PROFILE to use 'test-acc'
os.environ['AWS_PROFILE'] = 'insert_aws_profile'

def get_code_summary(prompt):
    fileList = [f.split('.')[0] for f in os.listdir('./model_configs')]
    
    for cnt, fileName in enumerate(fileList, 0):
        sys.stdout.write("[%d] %s\n\r" % (cnt, fileName))
    choice = int(input("Select model you would like to run[0-%s]: " % cnt))

    model = fileList[choice]

    # Load model information
    with open( f'./model_configs/{model}.json', 'r') as f:
        model_information = json.load(f)

    # Find and replace prompt placeholder
    summary_request_prompt = "Please summarize the following code: \n" + prompt
    for key, value in model_information["parameters"].items():
        if str(value).find("__PROMPT__") != -1:
            model_information["parameters"][key] = model_information["parameters"][key].replace("__PROMPT__", summary_request_prompt)
            break

    model_response = run_model(model_information, prompt)
    responseOutput = parse_output(model_information.get("response"), model_response)
    
    filename = f"{model}.md"
    fileLocation = os.getcwd()
    print(f"The following output will be written to file {fileLocation}/{filename}:\n" + responseOutput)
    
    with open(filename, 'w') as f:
        f.write(responseOutput)

# Example usage
if __name__ == "__main__":
    prompt = input("Enter a prompt: ")
    get_code_summary(prompt)
