from flask import Flask, render_template, request
import sys
sys.path.append('/ChemPal-v0.1')
# from functions_testing import make_a_list 
from Final import final_solution


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            processed_text = final_solution(text)
            # Pass both the input text and the processed text to the template
            return render_template('home.html', input_text=text, data=processed_text)
        else:
            return "No text provided", 400
    return render_template('home.html')


if __name__ =='__main__':
    app.run(debug=False, host='0.0.0.0')