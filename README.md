# PROJECT STRUCTURE
All of the dependencies are in the requirements.txt file. This project needs an initialized virtual environment to house all the dependencies. The file that runs the robot is GPIOTest.py (NOT main.py, this was a cleaner work in progress that I stopped working on to get the project working in time for my school presentation). 


# EXPLANATION
When the project runs, the terminal prompts you asking you to enter a command. Once you enter a simple instruction for the robot in English, you will see text saying "initializing path...", which will be replaced with "done" once the robot is done making the path. When this happens, the robot will physically perform the task you gave it and then ask you to enter a command again.
When you enter your English command, it is fed into a prompt in the gemma3 open source AI model. My prompt instructs it to break the command into a json structure with the key being a keyword associated with an action and the value being a number for how long the command should be performed. This way, chaining commands can be easily achieved by the LLM simply adding more key-value pairs for each part of the instruction. For example, telling the robot to "drive forward for a second, turn around and then back up for a while" may return the following json-style string:
{
  "driveForward": 1,
  "rotateRight": 3,
  "driveBackwards": 10
}

They prompt includes a specific set of keywords that the LLM MUST choose from for each action, and each of these keywords correspond to a movement method that controls the robot with GPIO pins. Sending different combinations of HIGH and LOW signals to each pin on each motor achieves different directions. For more info, look up "mecanum wheel direction charts". All of the AI computation takes place onboard the Raspberry Pi 5, which is why I used the lightweight gemma3 model. 
This is a crude and simple first attempt at an idea like this. I have more planned. 
