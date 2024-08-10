
# Trivia Trek

Trivia Trek is a quiz website where users can host quizzes, add their own questions, and invite participants via a unique link. The quizzes feature a timer and multiple-choice questions (MCQs). Admins have access to the leaderboard and can create a buzzer quiz with special functionalities for buzzer timing and ranking.


## Author

- [@Harsh Mohta](https://www.github.com/Harsh-Mohta9163)


## Features

- Host Quizzes: Create and manage quizzes with custom questions.
- Invite Participants: Participants can join via an invite link.
- Timed Questions: Each question has a timer, and the page automatically updates when time runs out.
- Leaderboard: Admins can view and manage the leaderboard.
- Buzzer Quiz: Special quizzes where participants can buzz in, with rankings based on buzzer timing.


## Tech Stack

**Client:** HTML,CSS,Java Script

**Server:** Django,Java Script

**Real Time Communication:** Django Channels,HTMX
## Run Locally

Clone the project

```bash
  git clone https://github.com/Harsh-Mohta9163/TriviaTrek.git
```

Go to the project directory

```bash
  cd TriviaTrek
```
Create a virtual environment and activate it:
```bash
 python -m venv venv
 venv\Scripts\activate
```
Install the required packages:

```bash
  pip install -r requirements.txt
```

Start the server

```bash
 python manage.py runserver
```


## Methodology
The project was developed using Django Channels to handle real-time communication between the server and multiple clients. The methodology for implementing the core functionalities, including room creation, member management, quiz instructions, real-time answer submissions, and buzzer functionality, is outlined below:

#### Room Creation and Member Management:
- The application allows users to create quiz rooms where they can add members by sharing an invite link.
- Each room is identified by a unique code, and members join the room using this code.
- The admin of the room has control over starting the quiz, sending instructions, and managing the quiz flow.
#### Real-Time Instruction Delivery:
- When the admin sends an instruction (e.g., starting the quiz, or removing a user), it is broadcasted to all members of the room using Django Channels.
- WebSocket connections are established for each member to ensure instant delivery of these instructions.
#### Answer Submission and Score Updates:
- During the quiz, participants select their answers, which are immediately sent to the server through WebSocket channels.
- The server receives the answer and processes it to determine if it's correct.
- Scores are updated in real time and displayed in the leaderboard available to the admin.The scores are dependent on time so user with fastest response gets the max score.
#### Score Formula:-
- score = max score per question+ time taken

#### Buzzer Functionality:
- For buzzer-style questions, the system listens for the first buzz from any participant.
- The first user to press the buzzer sends a signal through the WebSocket channel.
- The server captures this signal and broadcasts the name of the user who buzzed in first to all members, displaying it prominently on the admin screen.
- This ensures that the buzzer functionality is fair and that  the first response is at the top.

## Challenges Encountered
The development process involved several challenges, particularly in implementing real-time functionality using WebSockets. Managing the logic for updating the leaderboard and handling the timed question transitions was also complex. However, these challenges were overcome through persistent troubleshooting and leveraging Django Channels.Htmx websocket extensions also helped to solve the problem
## Further Improvements
- UI Enhancements: Improve the overall look and feel of the application.
- More Invitation Methods: Add options like QR codes for easier participant invites.
- Anti-Cheating Measures: Implement features to minimize cheating during quizzes.
- Enhanced User Experience: Continually improve the functionality and interaction of the app.
## Demo

https://youtu.be/Ei0Mk2KlE_o

