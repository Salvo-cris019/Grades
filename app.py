from flask import Flask, render_template, request
from decimal import Decimal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

def calculate_required_grades(prelim_grade):
   
    prelim_grade = Decimal(prelim_grade)

    passing_grade = Decimal('75')
    prelim_weight = Decimal('0.20')
    midterm_weight = Decimal('0.30')
    final_weight = Decimal('0.50')
    grade_range = (Decimal('0'), Decimal('100'))

   
    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

  
    current_total = prelim_grade * prelim_weight
    required_total = passing_grade - current_total
    min_required_average = required_total / (midterm_weight + final_weight)

   
    if prelim_grade >= passing_grade:
        return f"Keep pushing forward and remain committed. Required Grade for Midterms and Finals: {min_required_average:.2f}%"

   
    if min_required_average > grade_range[1]:
        return "Error: It is not possible to achieve the passing grade with this preliminary score."

   
    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]
    
    return f"Required Grade for Midterms and Finals: {min_required_average:.2f}%"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            prelim_grade = Decimal(request.form['prelim_grade'])
            result = calculate_required_grades(prelim_grade)
        except (ValueError, Decimal.InvalidOperation):
            result = "Error: Invalid input. Please enter a valid number."

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
