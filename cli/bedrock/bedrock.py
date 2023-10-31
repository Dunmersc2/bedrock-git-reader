import boto3 , json
import sys
sys.path.append("/home/sforde/Bedrock")
from cli.bedrock import create_sdk_client

# Function to print all Bedrock FMs
def print_all_models():
  client = create_sdk_client("bedrock")
  modelsReponse = client.list_foundation_models()
  for model in modelsReponse['modelSummaries']:
    print(model['modelArn'], model['providerName'])

# Specific function to run the titan text model - left here to show evolution of our approach here
def run_model_titan(model: str, prompt: str, textGenerationConfig) -> str:
  runtime_client = create_sdk_client("bedrock-runtime")  
  requestBody = json.dumps({
        "inputText": f"{prompt}",
        "textGenerationConfig": textGenerationConfig
  })
  modelResponse=runtime_client.invoke_model(
    body=requestBody,
    modelId=model, 
    accept="application/json", 
    contentType="application/json")

  responseBody = json.loads(modelResponse.get("body").read())
  responseOutput = responseBody.get("results")[0].get("outputText")
  return responseOutput

#  Function to run any model, based on the model information and prompt
def run_model(model_information: dict, prompt: str) -> str:
  # Construct API call to Bedrock
  request_body = json.dumps(model_information.get("parameters"))
  # print(request_body)
  runtime_client = create_sdk_client("bedrock-runtime")
  model_response=runtime_client.invoke_model(
    modelId = model_information.get("modelId"),
    accept = "application/json",
    contentType = "application/json",
    body = request_body)

  return model_response

def parse_output(responseItems, model_response):
  responseBody = json.loads(model_response.get("body").read())
  responseItems = responseItems.split(',')
  for key in responseItems:
    if isinstance(responseBody, dict):
        responseBody = responseBody.get(key)
    elif isinstance(responseBody, list): 
        responseBody = responseBody[int(key)]
  return responseBody

# Example API calls for each FM

#  Claude
#   Some of the AWS info differs slightly
# {
#   "modelId": "anthropic.claude-v2",
#   "contentType": "application/json",
#   "accept": "*/*",
#   "body": {
#     "prompt": "\n\nHuman: Hello world\n\nAssistant:",
#     "max_tokens_to_sample": 300,
#     "temperature": 0.5,
#     "top_k": 250,
#     "top_p": 1,
#     "stop_sequences": [
#       "\\n\\nHuman:"
#     ],
#     "anthropic_version": "bedrock-2023-05-31"
#   }
# }

# Titan text
# {
#   "modelId": "amazon.titan-text-express-v1",
#   "contentType": "application/json",
#   "accept": "*/*",
#   "body": {
#    "inputText": "this is where you place your input text",
#    "textGenerationConfig": {
#       "maxTokenCount": 8192,
#       "stopSequences": [],
#       "temperature":0,
#       "topP":1
#      }
#    } 
# }

#  Jurassic 2
# {
#   "modelId": "ai21.j2-ultra-v1",
#   "contentType": "application/json",
#   "accept": "*/*",
#   "body": "{"prompt":"this is where you place your input text","maxTokens":200,"temperature":0,"topP":250,"stop_sequences":[],"countPenalty":{"scale":0},"presencePenalty":{"scale":0},"frequencyPenalty":{"scale":0}}"  
# }
