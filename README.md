
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


## Challenges Encountered
The development process involved several challenges, particularly in implementing real-time functionality using WebSockets. Managing the logic for updating the leaderboard and handling the timed question transitions was also complex. However, these challenges were overcome through persistent troubleshooting and leveraging Django Channels.Htmx websocket extensions also helped to solve the problem
## Further Improvements
- UI Enhancements: Improve the overall look and feel of the application.
- More Invitation Methods: Add options like QR codes for easier participant invites.
- Anti-Cheating Measures: Implement features to minimize cheating during quizzes.
- Enhanced User Experience: Continually improve the functionality and interaction of the app.
## Demo

https://youtu.be/Ei0Mk2KlE_o

