import json

# data = open("C:/Users/Orz/Desktop/1.json")
#
# json = json.dumps(data)
with open("C:/Users/Orz/Desktop/1.json","r",encoding="utf-8") as f:
	data = json.load(f)
print(data)