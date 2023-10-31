import click
from cli.bedrock.bedrock import print_all_models, run_model

@click.group()
def cli():
  pass

@cli.command()
# @click.option("--list-all-models")
def list_all_models():
  print_all_models()

@cli.command()
def invoke_model():
  print(run_model("amazon", "What is this code doing at this URL - https://github.com/dbarnett/python-helloworld?"))

cli.add_command(list_all_models)
cli.add_command(invoke_model)

if __name__ == "__main__":
  cli()
