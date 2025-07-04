# feedback.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def analyze_feedback(data):
    try:
        feedback_id = data.get('id')
        employee_id = data.get('employee_id')
        branch_id = data.get('branch_id')
        behaviour = data.get('behaviour')
        communication = data.get('communication')
        satisfaction = data.get('satisfaction')
        overall_rating = data.get('overall_rating')
        comment = data.get('comment', "")

        prompt_text = f"""
        Analyze the following customer feedback:
        Behaviour: {behaviour}/10
        Communication: {communication}/10
        Satisfaction: {satisfaction}/10
        Overall Rating: {overall_rating}/10
        Comments: {comment.replace('$$', ', ')}
        Provide a concise 3-4 line summary of key insights and improvement areas.
        """

        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=150
        )

        analysis_result = response.choices[0].message.content.strip()

        return {
            "feedback_id": feedback_id,
            "employee_id": employee_id,
            "branch_id": branch_id,
            "analysis": analysis_result
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
