from flask import Flask, render_template, request
import logging
from workout_plan import workout_plan
from diet_plan import diet_plan

app = Flask(__name__,template_folder='.',static_folder='.')

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workout_plan')
def workout():
    return render_template('workout_plan.html', workout_plan=workout_plan)

@app.route('/diet_plan')
def diet():
    return render_template('diet_plan.html', diet_plan=diet_plan)

@app.route('/bmi_calculator', methods=['GET', 'POST'])
def bmi_calculator():
    bmi = None
    bmi_message = None
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            if height <= 0 or weight <= 0:
                raise ValueError("Weight and height must be positive numbers.")

            bmi = weight / (height ** 2)

            if bmi < 18.5:
                bmi_message = "You are underweight. Consider a diet rich in calories and nutrients."
            elif 18.5 <= bmi < 24.9:
                bmi_message = "You have a normal weight. Maintain a balanced diet to stay healthy."
            elif 25 <= bmi < 29.9:
                bmi_message = "You are overweight. Consider a balanced diet with fewer calories."
            else:
                bmi_message = "You are obese. A structured weight loss diet may be beneficial."

        except ValueError as e:
            bmi_message = str(e)
            app.logger.error(f"Error calculating BMI: {e}")

    return render_template('bmi_calculator.html', bmi=bmi, bmi_message=bmi_message)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/health_tips')
def health_tips():
    return render_template('healthtip.html')

@app.route('/workout_week/<week_name>')
def workout_week(week_name):
    week_data = workout_plan.get(week_name)
    if week_data:
        return render_template('workout_week.html', week_name=week_name, week_data=week_data)
    else:
        app.logger.warning(f"Week not found: {week_name}")
        return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
