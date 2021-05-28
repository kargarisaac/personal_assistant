import yaml

data = yaml.safe_load(open('nlu/train.yaml').read())

commands = data['commands']
print(commands)