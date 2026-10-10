# AI Quiz Generator 🤖

An AI-powered quiz generation web application built using Python, Flask, and Google's Gemini API.

## Features

- Generate 5 multiple-choice questions on any topic.
- Four options for each question.
- Submit answers and calculate your score.
- Display score, percentage, and feedback.
- Simple and responsive web interface.

## Technologies Used

- Python
- Flask
- Google Gemini API
- HTML
- CSS

## How to Run Locally

1. Clone this repository.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project folder and add your Gemini API key:

   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Security

Keep your API key private. Never upload your `.env` file to GitHub.

## Author

Developed as a Python and Generative AI learning project.
