from random import choice

def generateID(id_lenght):
	alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	id = ""
	for i in range(id_lenght):
		id += choice(alphabet)
	return id
