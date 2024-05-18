from flask import Flask, render_template, request, jsonify

import sys
sys.path.append('/ChemPal')
from Final import final_solution

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            try:
                processed_text = final_solution(text)
                return render_template('home.html', input_text=text, data=processed_text)
            except Exception as e:
                app.logger.error(f"Error processing text: {e}")
                return render_template('home.html', input_text = '',data = {'correct_input': False})
        else:
            return "No text provided", 400
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=False)
    # host='0.0.0.0'
