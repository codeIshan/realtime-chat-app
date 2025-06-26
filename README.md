# Real-Time Chat Application

A modern real-time chat application built with Flask-SocketIO and JavaScript. Chat with friends in real-time!

## Features

- 💬 Real-time messaging with WebSockets
- 👤 User avatars and profiles
- ⌨️ Live typing indicators
- ✅ Read receipts
- 👥 Online user list
- 📱 Responsive design (works on mobile)
- 🎨 Modern dark theme UI

## Quick Start for Testing with Friends

### Option 1: Using ngrok (Quick & Easy)

1. **Clone and setup locally:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   pip install -r requirements.txt
   python server.py
    ```
2. **Install ngrok:**

- Download from ngrok.com
- Sign up for free account
- Get your auth token and run: 
```bash 
    ngrok config add-authtoken YOUR_TOKEN
```

3. **Share with friends:**
### bash
- In a new terminal (keep server.py running)
```bash 
ngrok http 5000
```
- Share the https://abc123.ngrok.io URL with your friends
- Everyone can join and chat instantly!



**Local Development**

1. Clone the repository:
bashgit clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

    cd YOUR_REPO_NAME

2. Setup virtual environment (recommended):
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
bashpip install -r requirements.txt

4. Run the server:
bashpython server.py

5. Open in browser: 

    Go to http://localhost:5000
Choose a username and avatar
Start chatting!



## How to Use

1. Join the chat: Enter your username and pick an avatar
2. Send messages: Type in the input box and press Enter
3. See who's online: Check the sidebar for active users
4. Watch typing indicators: See when others are typing
5. Read receipts: Small avatars show who has read your messages

## Live Demo

![alt text](<Screenshot 2025-06-26 182340.png>)
- Registration Page

![alt text](<Screenshot 2025-06-26 182443.png>)
- Chat Room

![alt text](<Screenshot 2025-06-26 182634.png>)
- User joining

![alt text](<Screenshot 2025-06-26 182842.png>)

## Project Structure
```bash
chat-app/
├── server.py              # Flask-SocketIO backend
├── templates/
│   └── index.html        # Frontend with real-time features
├── static/
│   └── avatars/          # User avatar images
├── requirements.txt      # Python dependencies
├── Procfile             # For deployment
└── README.md           # This file
```
## Tech Stack

- Backend: Python, Flask, Flask-SocketIO
- Frontend: HTML, CSS, JavaScript
- Real-time: WebSockets via Socket.IO

## Troubleshooting
**Can't connect to server?**

- Make sure Flask server is running on port 5000
- Check firewall settings
- For ngrok: ensure both Flask and ngrok are running

**Friends can't join?**

- Share the ngrok HTTPS URL (not the Flask localhost URL)
- Make sure ngrok session hasn't expired
- Try refreshing the ngrok tunnel

**Missing avatars?**

- Add PNG images to static/avatars/ folder
- Name them avatar1.png through avatar8.png
- Include group.png for the chat header

## Contributing

- Fork the repository
- Create a feature branch
- Make your changes
- Submit a pull request

## License
This project is open source and available under the MIT License.

Made with ❤️ for chatting with friends!
Star ⭐ this repo if you found it useful!
