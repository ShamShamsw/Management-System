import json
import datetime

class CustomerFeedbackSystem:
    def __init__(self, surveys_file="surveys.json", feedback_file="feedback.json"):
        self.surveys_file = surveys_file
        self.feedback_file = feedback_file
        self.surveys = self.load_data(self.surveys_file)
        self.feedback = self.load_data(self.feedback_file)

    def load_data(self, filename):
        """Load data from a JSON file."""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, filename, data):
        """Save data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def create_survey(self, survey_name, questions):
        """Create a new customer survey with custom questions."""
        survey = {"survey_name": survey_name, "questions": questions}
        self.surveys.append(survey)
        self.save_data(self.surveys_file, self.surveys)
        print(f"Survey '{survey_name}' created successfully!")

    def collect_feedback(self, survey_name, responses):
        """Collect customer feedback for a given survey."""
        feedback_entry = {"survey_name": survey_name, "responses": responses, "date": str(datetime.datetime.now())}
        self.feedback.append(feedback_entry)
        self.save_data(self.feedback_file, self.feedback)
        print(f"Feedback recorded for survey '{survey_name}'.")

    def analyze_feedback(self):
        """Analyze feedback to identify trends and satisfaction scores."""
        survey_analysis = {}
        for entry in self.feedback:
            survey_name = entry["survey_name"]
            if survey_name not in survey_analysis:
                survey_analysis[survey_name] = []
            survey_analysis[survey_name].append(entry["responses"])
        
        print("Feedback Analysis:")
        for survey, responses in survey_analysis.items():
            print(f"Survey: {survey}, Total Responses: {len(responses)}")

    def run(self):
        """Main function to handle customer feedback interactions."""
        while True:
            action = input("Choose an action: create_survey, collect_feedback, analyze_feedback, or quit: ")
            if action == "quit":
                break
            elif action == "create_survey":
                survey_name = input("Enter survey name: ")
                questions = []
                while True:
                    question = input("Enter a question (or 'done' to finish): ")
                    if question.lower() == "done":
                        break
                    questions.append(question)
                self.create_survey(survey_name, questions)
            elif action == "collect_feedback":
                survey_name = input("Enter survey name: ")
                responses = []
                for survey in self.surveys:
                    if survey["survey_name"] == survey_name:
                        for question in survey["questions"]:
                            response = input(f"{question}: ")
                            responses.append(response)
                        self.collect_feedback(survey_name, responses)
                        break
                else:
                    print("Survey not found.")
            elif action == "analyze_feedback":
                self.analyze_feedback()
            else:
                print("Invalid action.")

if __name__ == "__main__":
    cfs = CustomerFeedbackSystem()
    cfs.run()
