# Mental-Health-Tracker

A Flask-based web application for self-assessment of mental health indicators including anxiety, depression, and stress levels.

## Overview

Mental-Health-Tracker is a simple yet intuitive mental health screening tool that helps users understand their mental wellness through an interactive questionnaire. The app collects user information, presents a series of psychological assessment questions, and visualizes results in an easy-to-understand pie chart format.

**⚠️ Disclaimer:** This tool is for self-awareness and educational purposes only. It is NOT a substitute for professional mental health diagnosis or treatment. If you're experiencing mental health concerns, please consult with a qualified healthcare professional.

---

## Features

### 1. Login Page
The login page serves as the entry point to the application where users provide:
- **Name:** User's full name
- **Age:** User's age in years
- **Profession:** Selection from predefined categories:
  - School Student
  - College Student
  - IT Professional
  - Government Job
  - Education Sector
  - Executives
  - Other
- **State:** User's state of residence

This demographic information helps contextualize the user's responses and can be used for future analytics and personalization features.

### 2. Questionnaire (Demo Page)
After login, users proceed to the assessment page where they answer a series of mental health-related questions designed to evaluate:
- Anxiety levels
- Depression symptoms
- Stress indicators

Each question is carefully crafted to help users reflect on their mental state.

### 3. Results & Visualization
Upon completing the questionnaire, users receive:
- **Pie Chart Visualization:** A colorful pie chart breaking down their scores across three dimensions:
  - 🟡 **Anxiety** (Murky Yellow)
  - ⚫ **Depression** (Grey)
  - 🔴 **Stress** (Red)
- Proportional representation of how their responses map to each mental health dimension
- Clear visual feedback for quick understanding of their mental health profile

---

## Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3
- **Visualization:** Chart library (for pie chart rendering)
- **Deployment:** GitHub Pages (static assets)

---

## Project Structure

```
Mental-Health-Tracker/
├── app.py                 # Flask application and routes
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── login.html        # Login page
│   ├── demo.html         # Questionnaire page
│   └── result.html       # Results and pie chart page
└── static/                # Static assets
    └── style.css         # CSS styling
```

---

## Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/anusreejyaprakash67-hub/Mental-Health-Tracker.git
   cd Mental-Health-Tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

---

## User Flow

1. **Start:** User lands on the login page
2. **Register:** Fill in name, age, profession, and state
3. **Assess:** Answer questionnaire questions on the demo page
4. **Visualize:** View results with pie chart breakdown
5. **Understand:** See proportional representation of anxiety, depression, and stress

---

## Color Legend

| Metric | Color | Meaning |
|--------|-------|----------|
| Anxiety | Murky Yellow 🟡 | Tension, worry, apprehension |
| Depression | Grey ⚫ | Mood, sadness, hopelessness |
| Stress | Red 🔴 | Pressure, tension, overwhelm |

---

## Future Enhancements

- [ ] Data persistence (store user responses in database)
- [ ] Account system with login authentication
- [ ] Historical tracking (compare results over time)
- [ ] Export results as PDF
- [ ] Multi-language support
- [ ] Mobile-responsive design improvements
- [ ] Professional resources and hotline links
- [ ] Advanced scoring algorithm with clinical validation
- [ ] User progress dashboard
- [ ] Personalized recommendations based on scores

---

## Important Notes

### Privacy & Data Handling
- Currently, responses are not permanently stored
- All data entered is temporary for demonstration purposes
- When implementing persistent storage, ensure compliance with health data regulations (HIPAA, GDPR, etc.)

### Assessment Validity
- The current questionnaire is for demonstration purposes
- Future versions should incorporate validated psychological scales (PHQ-9 for depression, GAD-7 for anxiety, etc.)
- Professional review of assessment methodology is recommended

---

## Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

---

## License

This project is open source and available under the MIT License.

---

## Resources

- [Mental Health America](https://www.mhanational.org/)
- [SAMHSA National Helpline](https://www.samhsa.gov/find-help/national-helpline) - 1-800-662-4357
- [Crisis Text Line](https://www.crisistextline.org/) - Text HOME to 741741
- [International Association for Suicide Prevention](https://www.iasp.info/resources/Crisis_Centres/)

---

## Author

[@anusreejyaprakash67-hub](https://github.com/anusreejyaprakash67-hub)

---

*Last Updated: December 15, 2025*
