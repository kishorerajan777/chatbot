# Symptoms Checker Bot

[MedTech Chatbot](https://medtecbot-3ryovtid4tji5trsty4hte.streamlit.app/)


## Overview

The **Symptoms Checker Bot** is an interactive web application built with Streamlit that analyzes user-provided symptoms to suggest possible diseases, provide precautions, and visualize data through interactive charts. Users can type queries such as "what are the symptoms of kidney stone" or "I want precaution of kidney stones" and, when at least three symptoms are entered, the bot displays visualization charts like matched symptom counts and symptom severity levels.

> **Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice.

## Project Purpose

The main goals of this project are to:
- **Provide initial medical insights**: By matching user-entered symptoms to potential diseases.
- **Offer preventive recommendations**: Delivering precautions related to the identified diseases.
- **Visualize symptom data**: Helping users understand the severity and frequency of symptoms through charts.

## Features

- **Symptom Analysis and Disease Prediction**  
  - Input queries like "symptoms of AIDS" or "i have thyroid disorder" to receive a list of possible diseases, complete with descriptions and matched symptom counts.
  
- **Precaution Suggestions**  
  - Ask for precautions (e.g., "precaution for kidney stones") to get preventive measures for the disease.
  
- **Interactive Visualizations**  
  - **Matched Symptom Count Chart:** Displays a bar chart of the top 3 diseases with the highest number of matching symptoms.
  - **Symptom Severity Chart:** Shows a bar chart of the severity levels for the symptoms provided.
  
- **Real-Time Chat Interface**  
  - Enjoy a conversational experience with typewriter effects and dynamic responses.

## Tech Stack

- **Python** – Core programming language.
- **Streamlit** – For building the interactive web application.
- **Pandas** – For data processing and manipulation.
- **Plotly Express** – For generating interactive visualizations.
- **Regular Expressions (re module)** – For parsing and cleaning user input.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/symptoms-checker-bot.git
   cd symptoms-checker-bot
   
2.**Create and activate a virtual environment (optional but recommended):**

bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

3.**Install dependencies:**

bash
Copy
Edit
pip install -r requirements.txt
Ensure your requirements.txt includes: streamlit, pandas, plotly, etc.

**Usage & Demo**

1.Run the Application:

bash
Copy
Edit
streamlit run bot2.py

Interact with the Bot:

2.Symptom Query: Type something like:

sql
Copy
Edit
what are the symptoms of kidney stone
The bot will return the symptoms, description, and the number of matched symptoms

Precaution Query: Type:

css
Copy
Edit
I want precaution of kidney stones
to get preventive measures.

Visualization: After entering at least three symptoms, additional buttons will appear:

"📊 See Matched Symptom Counts for Top 3 Diseases" – displays a bar chart of matched symptom counts.
"📊 See Symptom Severity Chart" – displays a bar chart of the severity levels of the symptoms.

Example Input:
vomiting, headache, nausea, spinning_movements, loss_of_balance, unsteadiness
The bot will list the top 3 possible diseases and, upon clicking the visualization buttons, show the corresponding charts.


**Project Demonstration Guide**

Step 1: Launch the app using the Streamlit command.
Step 2: In the chat interface, type your query (e.g., "what are the symptoms of AIDS" or "I have thyroid disorder").
Step 3: Review the bot's response with the predicted diseases, descriptions, and matched symptom counts.
Step 4: When additional buttons appear, click the visualization button(s) to view:
A bar chart showing the matched symptom counts for the top 3 predicted diseases.
A bar chart displaying the severity levels of the user-entered symptoms.
Step 5: Use the charts to better understand the symptom distribution and severity.

**Future Enhancements**
Improved NLP: Enhance parsing and intent recognition for better accuracy.
User Feedback: Implement a mechanism for users to provide feedback on the predictions.
Additional Visualizations: Introduce more advanced charts and graphs.
Integration with Medical Databases: Connect with real-world data sources for updated medical insights.
