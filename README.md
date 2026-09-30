# 🌸 Iris Flower Classifier Web App

An interactive machine learning web application built with **Streamlit** and **scikit-learn** to predict Iris flower species.

---

## 📁 Project Structure

```text
Streamlit/
├── app.py                 # Main Streamlit web application
├── Model Training.ipynb   # Jupyter Notebook used to train and export the model
├── iris_model.pkl         # Trained RandomForestClassifier model file
├── requirements.txt       # Python package dependencies
├── test.py                # Hands-on practice calculator app
└── README.md              # Project documentation
```

---

## ✨ Features

- **Trained ML Model**: Uses a `RandomForestClassifier` trained on the Iris dataset in `Model Training.ipynb`.
- **4 Measurement Sliders**: Easily adjust Sepal Length, Sepal Width, Petal Length, and Petal Width.
- **Species Prediction**: Identifies whether the flower is **Setosa**, **Versicolor**, or **Virginica**.
- **Confidence Score**: Shows the model's confidence percentage for the prediction.
- **Sidebar Summary**: Quick access to model and dataset information.

---

## 🚀 How to Run the App

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501` (or the port shown in your terminal).
