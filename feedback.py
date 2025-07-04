from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq  # Make sure: pip install groq

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get Groq API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client with API key from .env
client = Groq(api_key=groq_api_key)
@app.route('/feedback', methods=['POST'])
def analyze_feedback():
    try:
        data = request.json
    
        # Extract feedback details
        feedback_id = data.get('id')
        employee_id = data.get('employee_id')
        branch_id = data.get('branch_id')
        behaviour = data.get('behaviour')
        communication = data.get('communication')
        satisfaction = data.get('satisfaction')
        overall_rating = data.get('overall_rating')
        comment = data.get('comment', "")

        # Format data for Groq API
        prompt_text = f"""
        Analyze the following customer feedback:
        Behaviour: {behaviour}/10
        Communication: {communication}/10
        Satisfaction: {satisfaction}/10
        Overall Rating: {overall_rating}/10
        Comments: {comment.replace('$$', ', ')}
        Provide a concise 3-4 line summary of key insights and improvement areas.
        """
        
        # Send request to Groq Cloud API
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=150
        )
        
        # Extract response
        analysis_result = response.choices[0].message.content.strip()
        
        return jsonify({
            "feedback_id": feedback_id,
            "employee_id": employee_id,
            "branch_id": branch_id,
            "analysis": analysis_result
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
