# Ingredient Analyzer

**Ingredient Analyzer** is a web application that helps users analyze ingredients in food or skincare products by providing information about their potential health effects. The app uses AI, powered by OpenAI’s GPT-4, to identify harmful substances in ingredients and categorize them based on their health impact. The application displays real-time results with color-coded feedback for harmful, moderate, and safe ingredients, helping users make more informed decisions about the products they use.

## Key Features

- **AI-powered Ingredient Analysis**: Uses OpenAI's GPT-4 to analyze and identify harmful ingredients based on input.
- **Color-coded Feedback**: Ingredients are categorized as harmful, moderate, or safe, with results displayed using color-coded labels.
- **User-friendly Interface**: Built with Flask, the app features a simple and intuitive user interface using Bootstrap.
- **Real-time Results**: The tool provides instant feedback, offering users detailed explanations about each ingredient.
- **Responsive Design**: The app is designed to work well on both desktop and mobile devices.
- **Loading Indicators**: Shows a loading spinner while the analysis is being processed.

## Technologies Used

- **Flask**: A lightweight web framework for Python to build the backend.
- **OpenAI GPT-4**: Used for analyzing the ingredients and generating responses.
- **Bootstrap**: For creating a responsive and clean user interface.
- **JavaScript**: For handling dynamic interactions such as showing ingredient details.
- **CSS**: For styling the app with a modern look and feel.
- **HTML**: For structuring the content of the web pages.

## How to Run the Project Locally

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/ingredient-analyzer.git
   ```

2. Navigate to the project folder:
   ```bash
   cd ingredient-analyzer
   ```

3. Install the required Python libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run the Flask app:
   ```bash
   python app.py
   ```

6. Open your browser and visit `http://127.0.0.1:5000` to use the Ingredient Analyzer.

## Future Enhancements

- **Extended Ingredient Database**: Adding more ingredients to improve the analysis accuracy.
- **User Authentication**: Allow users to save their past ingredient analyses for later reference.
- **Multiple Language Support**: Translate the app to other languages to reach a broader audience.
- **Better Error Handling**: Improve error handling for larger input sizes or when the OpenAI API is unavailable.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
