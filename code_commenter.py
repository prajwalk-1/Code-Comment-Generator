import openai
from flask import Flask, request, render_template

# Initialize Flask app
app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = 'Your_Openai_API_Key'  # Make sure to keep your API key secure

def generate_code_comments(code):
    """
    This function interacts with the OpenAI API to generate comments for the given code.
    
    :param code: The raw code input by the user
    :return: Code with comments generated by the LLM
    """
    prompt = f"Explain the following Python code with comments:\n\n{code}"

    try:
        # Call the OpenAI API using ChatCompletion (for newer versions)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains code by adding comments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        
        # Return the generated response
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create a basic route for the web interface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comment', methods=['POST'])
def comment():
    """
    This route receives the input code from the user and returns the commented code.
    """
    user_code = request.form['code']
    
    # Call the function to generate comments
    commented_code = generate_code_comments(user_code)
    
    return render_template('index.html', input_code=user_code, commented_code=commented_code)

if __name__ == '__main__':
    app.run(debug=True)
