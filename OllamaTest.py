from ollama import chat

stream = chat(
    model='gemma3',
    messages=[
    {'role': 'user', 
    'content': 'You will be given an instruction and decide on appropriate actions and times. Allowed actions: driveForward, driveBackward, strafeLeft, strafeRight, turnLeft, turnRight. Return ONLY a JSON in the following format: {action : time, action : time, action : time ...} where action is a string from the Allowed actions and time is the number of seconds to do the action for, each action time pair should be seperated by a comma and there should be as many action time pairs as necessary as per the instruction. THIS IS THE INSTRUCTION: go forward for a sec, turn right and go reverse for a three seconds'}],
    stream=True,
)


response = ""
for chunk in stream:
  response += (chunk['message']['content']).replace("}", "").replace("{", "").replace("\n", "").replace(":", " ").replace("```", "").replace("json", "")

print(response.split(","))
