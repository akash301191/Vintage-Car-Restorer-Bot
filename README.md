# Vintage Car Restorer Bot

Vintage Car Restorer Bot is a Streamlit-powered automotive companion that interprets vintage car visuals, highlights historical significance, and helps you reimagine each ride with restoration tips and sourcing options. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot provides a beautifully structured report to guide your restoration journey.

## Folder Structure

```
Vintage-Car-Restorer-Bot/
├── vintage-car-restorer-bot.py
├── README.md
└── requirements.txt
```

* **vintage-car-restorer-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Car Image Upload & Restoration Preferences**  
  Upload an image of your vintage car and select your preferred restoration style and design approach.

* **Model Recognition & Visual Analysis**  
  The `Car Historian` agent identifies the likely make, model, and decade based on exterior design cues.

* **Cultural & Historical Context**  
  The `Design Context Agent` explains the historical and cultural impact of the car and its place in automotive heritage.

* **Restoration Style Suggestions**  
  The `Restoration Stylist` recommends paint schemes, trim treatments, interior options, and upgrade ideas based on your preferences.

* **Parts & Accessories Recommendations**  
  The `Parts Finder Agent` searches the web for matching restoration parts using SerpAPI and delivers real links to help complete the build.

* **Structured Markdown Output**  
  Your restoration guide is delivered in clean, readable markdown with sections, tables, and bullet points.

* **Download Option**  
  Save the entire report as a `.md` file for your records, inspiration board, or restoration garage.

* **Clean Streamlit UI**  
  Built with Streamlit to offer an intuitive, focused, and visually appealing experience for restorers and collectors.

## Prerequisites

* Python 3.11 or higher  
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

```bash
   git clone https://github.com/akash301191/Vintage-Car-Restorer-Bot.git
   cd Vintage-Car-Restorer-Bot
```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run vintage-car-restorer-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and SerpAPI keys in the sidebar.
   * Upload a photo of the vintage car you want to restore.
   * Choose your restoration preferences (authentic, modernized, or blended).
   * Click **🔧 Generate Car Restoration Report**.
   * View and download your AI-powered restoration report.

3. **Download Option**
   Use the **📥 Download Restoration Report** button to save your full guide as a `.md` file.

## Code Overview

* **`render_car_restoration_preferences()`**: Collects uploaded image and restoration preferences.
* **`render_sidebar()`**: Manages API key inputs and stores them in Streamlit session state.
* **`generate_restoration_report()`**:

  * Uses the `Car Historian` agent to identify model and features.
  * Sends results to the `Design Context Agent`, `Restoration Stylist`, and `Parts Finder Agent` to create a full restoration guide.
* **`main()`**: Orchestrates the UI layout, user inputs, report generation, and markdown display.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report issues, or open a pull request. Please ensure your changes are well-tested, clearly documented, and in line with the project's theme.
