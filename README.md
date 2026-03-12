# Fake Buster – Advanced Fake News & Snippet Detection Tool

## 📄 Abstract
**Fake Buster** is an intelligent, high-precision fake news detection system designed to combat the global rise of misinformation. Utilizing **Machine Learning (ML)** and **Natural Language Processing (NLP)**, it specializes in classifying news headlines, social media posts, and short **news snippets** as **REAL** or **FAKE**.

Developed as part of the JRM Infotech Internship Program software development task, this tool provides a robust, automated solution for identifying deceptive content with high confidence, offering real-time analysis for journalists, researchers, and the general public.

---

## 🎯 How It Works
Users can input a headline, article, or news snippet into the web interface. The system analyzes the content and provides a prediction along with a probability score indicating how likely the news is to be fake. The tool is useful for journalists, fact-checkers, researchers, and the general public.

---

## 🚀 Key Features
*   **Snippet-Level Analysis**: Specifically optimized to handle short news snippets, headlines, and telegraphic social media updates.
*   **Image Snippet Support (OCR)**: Built-in analysis for screenshots of news articles or social media posts using Optical Character Recognition.
*   **Multi-Model Intelligence**: Supports multiple state-of-the-art algorithms including Logistic Regression, Naive Bayes, SVM, and Random Forest.
*   **Dynamic Probability Scores**: Provides precise confidence percentages for both "Reality" and "Deception" scores.
*   **Modern Glassmorphic UI**: A premium user interface built with React, featuring sleek animations and a responsive design system.
*   **Scalable Backend**: Powered by Django REST Framework with a modular architecture for easy model swapping.

---

## 🔍 What is a News Snippet?
In the context of **Fake Buster**, a *snippet* refers to the news content provided for verification, which can be submitted either as **normal text** or extracted from **news sent as images**. Since misinformation often spreads through these different formats (like text messages, social media posts, or image screenshots), our tool is specifically tuned to analyze both normal text inputs and text extracted from images to determine authenticity.

---

## 🛠️ Technology Stack
### **Backend**
*   **Framework**: Django & Django REST Framework (DRF)
*   **ML Engine**: Scikit-learn (TF-IDF Vectorization + Classification)
*   **NLP Tools**: NLTK (Advanced text preprocessing)
*   **Data Handling**: Pandas & NumPy

### **Frontend**
*   **Framework**: React.js (Vite)
*   **Styling**: Vanilla CSS (Custom Design System)
*   **UI Patterns**: Glassmorphism, Micro-animations, Responsive Layouts

---

## 📂 Project Structure
```text
Detection/
├── backend/               # Django API & ML Infrastructure
│   ├── detector/          # Core API App (Views, Serializers, URLs)
│   ├── fakebuster_api/    # Project configuration and settings
│   ├── train_model.py     # End-to-end ML Training Pipeline
│   ├── test_model.py      # Console-based testing suite
│   ├── model.pkl          # Trained model binary
│   ├── vectorizer.pkl     # TF-IDF Vectorizer state
│   └── requirements.txt   # Python dependency list
├── frontend/              # React-based User Interface
│   ├── src/               # React components, assets, and design tokens
│   ├── public/            # Static assets
│   └── package.json       # Node.js dependencies
├── README.md              # Project documentation
└── package.json           # Root scripts for project management
```

---

## ⚙️ Installation & Usage

### **1. Backend Setup**
Navigate to the backend directory and install dependencies:
```powershell
cd backend
pip install -r requirements.txt
```
Train the ML model:
```powershell
python train_model.py
```
Start the API server:
```powershell
python manage.py runserver
```

### **2. Frontend Setup**
Navigate to the frontend directory and launch the UI:
```powershell
cd ../frontend
npm install
npm run dev
```

---

## 📊 Sample Output
| Input Snippet | Prediction | Confidence |
|:---|:---:|:---:|
| "NASA rover discovers signs of ancient water on Mars surface." | **REAL** | 98.4% |
| "Celebrity spotted on the moon in a secret billionaire base." | **FAKE** | 99.1% |
| "Breakthrough in fusion energy achieves net power gain." | **REAL** | 94.2% |

---

## 🛡️ Mission Statement
Fake Buster aims to restore digital trust by providing transparent, AI-driven verification tools. By focusing on snippet analysis, we address the most common vector for misinformation—viral, short-form content—and empower users to verify facts before they share.

---
© 2026 Fake Buster AI Project | JRM Infotech Internship Submission
