# Lockin - Distraction Monitoring System

Lockin is a productivity application designed to monitor user engagement and minimize distractions. Using advanced technologies like OpenCV, Pygame, and modular input tracking, Lockin provides real-time feedback to keep users focused on their tasks.

## Features

- **Face and Eye Detection**: Utilizes OpenCV to monitor user presence and detect attention levels through facial and eye recognition.
- **Keyboard & Mouse Activity Tracking**: Tracks user input to identify periods of inactivity.
- **Customizable Alert System**: Provides dynamic distraction alerts through animated popups built with Pygame.
- **Real-time Monitoring**: Combines multiple input streams for comprehensive focus monitoring.

## Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - OpenCV for face and eye detection
  - Pygame for interactive alerts
  - PyAutoGUI and other modules for input tracking
- **Version Control**: Git and GitHub

## How It Works

1. **Attention Detection**:
   - OpenCV processes webcam input to detect facial and eye features.
   - Absence of detection triggers an inactivity state.

2. **Input Tracking**:
   - Keyboard and mouse inputs are continuously monitored.
   - Lack of activity is logged for distraction analysis.

3. **Distraction Alerts**:
   - Pygame generates animated popups to re-engage users during periods of inactivity.
   - Alerts are customizable based on user preferences.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aaryan-Biradar/lockin.git
   cd lockin
   ```
   
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Run the application:
   ```bash
   python main.py
   ```
