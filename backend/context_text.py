# access the message.txt file
with open('message.txt', 'r') as file:
    content = file.readlines()


# access the first one and topic.content_text
INSTRUCTION_MESSAGE = content[0]

print(INSTRUCTION_MESSAGE)
