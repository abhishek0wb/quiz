# Quiz App

Welcome to the Quiz App, an interactive web application that lets users test their knowledge across multiple categories in a sleek and responsive interface. Built using Flask, this project is perfect for demonstrating dynamic web development and creating engaging user experiences.

## Features

- **Category-Based Quiz**: Choose from multiple categories and answer tailored questions
- **Dynamic Scoring**: Real-time score calculation based on selected answers
- **Improved UI/UX**: Modern design with enhanced responsiveness and intuitive navigation
- **Customizable Questions**: Easily add or update questions using a structured .txt file
- **Hosted Online**: Deployed using Vercel for seamless accessibility

## Demo

Check out the live version here: [Quiz App on Vercel](#)

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **Data Management**: Plaintext .txt file for dynamic questions and answers

## Setup

### Prerequisites

- Python 3.8+
- Git installed on your system

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abhishek0wb/quiz.git
   cd quiz
   ```

2. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the .env File**
   Add the SECRET_KEY for the Flask app:
   ```env
   SECRET_KEY=<your-generated-secret-key>
   ```

4. **Run the App Locally**
   ```bash
   python app.py
   ```

5. **Access the App**
   Open `http://127.0.0.1:5000` in your browser.

## Usage

1. Navigate to the home page and select a quiz category
2. Answer questions by selecting one option per question
3. Submit your answers to view your score and feedback
4. Use the "Back to Home" button to return to the main page and try another quiz!

## Contribution

Contributions are welcome! To contribute:

1. **Fork the Repository**

2. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**
   ```bash
   git commit -m "Add your message here"
   ```

4. **Push the Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request**

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Developed with ❤️ by Abhishek.
