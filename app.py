from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pickle

app = Flask(__name__)

# Load and clean data from CSV file
data = pd.read_csv('data/laptop_pricing_dataset.csv')

X = data[['RAM_GB', 'Storage_GB_SSD', 'Screen_Size_cm', 'CPU_frequency', 'Weight_kg', 'GPU', 'Screen_Type', 'OS']]
y = data['Price']

X = pd.get_dummies(X, columns=['GPU', 'Screen_Type', 'OS'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeRegressor()
model.fit(X_train, y_train)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Get JSON data from the request
        data = request.get_json()

        # Extract form values
        ram = float(data['ram'])
        storage = float(data['storage'])
        screen_size = float(data['screenSize'])
        cpu_frequency = float(data['cpuFrequency'])
        weight = float(data['weight'])
        gpu = data['gpu']
        screen_type = data['screen']
        os = data['os']

        # Create DataFrame for input data and perform one-hot encoding
        input_data = pd.DataFrame([[ram, storage, screen_size, cpu_frequency, weight, gpu, screen_type, os]],
                                  columns=['RAM_GB', 'Storage_GB_SSD', 'Screen_Size_cm', 'CPU_frequency', 'Weight_kg', 'GPU', 'Screen_Type', 'OS'])
        input_data = pd.get_dummies(input_data, columns=['GPU', 'Screen_Type', 'OS'])

        input_data = input_data.reindex(columns=X_train.columns, fill_value=0)

        predicted_price = model.predict(input_data)[0]

        return jsonify({'prediction': predicted_price})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
