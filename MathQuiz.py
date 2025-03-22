import random
import csv
import os
import time
import threading
import sys
import select

# Quiz questions
Quiz_list = [
    # Linear Algebra (5)
    ['Linear Algebra', 'If the zeroes of the given quadratic polynomial x^2-kx+16 are equal, then find the value of k?', '+-8', '+8', '-8', 'More than one of the above', 'a'],
    ['Linear Algebra', 'Solve for x: 2x^2 - 5x + 2 = 0', '2, 1/2', '1, 2', '-2, -1/2', 'No real solutions', 'a'],
    ['Linear Algebra', 'If α and β are the roots of x^2 - 7x + 10 = 0, what is the value of α + β?', '-10', '10', '-7', '7', 'd'],
    ['Linear Algebra', 'For what value of k will (x - 3) be a factor of x^2 - kx + 9?', '3', '6', '9', '12', 'b'],
    ['Linear Algebra', 'What is the sum of the roots of the quadratic equation 3x^2 - 7x + 2 = 0?', '7/3', '3/7', '-7/3', '-3/7', 'a'],
    
    # Calculus (5)
    ['Calculus', 'If f(x) = x^3 - 3x^2 + 2x, then what is f\'(x)?', '3x^2 - 6x + 2', '3x - 6', 'x^2 - 3x + 2', 'None of the above', 'a'],
    ['Calculus', 'What is the derivative of sin(x) with respect to x?', 'cos(x)', '-sin(x)', 'tan(x)', '-cos(x)', 'a'],
    ['Calculus', 'Evaluate the limit: lim (x→0) (sin x / x)', '0', '1', '∞', 'Does not exist', 'b'],
    ['Calculus', 'Find the integral of e^x dx.', 'e^x + C', 'e^(x+1) + C', 'x e^x + C', '1/e^x + C', 'a'],
    ['Calculus', 'If f(x) = ln(x), what is f\'(x)?', '1/x', 'ln(x)', 'x', 'x ln(x)', 'a'],
    
    # Statistics (5)
    ['Statistics', 'What is the mean of the numbers 2, 4, 6, 8, 10?', '4', '5', '6', '7', 'c'],
    ['Statistics', 'Which of the following is a measure of central tendency?', 'Mean', 'Variance', 'Standard Deviation', 'Skewness', 'a'],
    ['Statistics', 'The median of {1, 3, 3, 6, 7, 8, 9} is?', '6', '5', '7', '8', 'a'],
    ['Statistics', 'What does standard deviation measure?', 'Central tendency', 'Spread of data', 'Probability', 'Regression', 'b'],
    ['Statistics', 'If a dataset has a large interquartile range (IQR), what does it indicate?', 'High variability', 'Low variability', 'Normal distribution', 'No relation', 'a'],
    
    # Trigonometry (5)
    ['Trigonometry', 'What is sin(30°)?', '1/2', '√3/2', '1', '0', 'a'],
    ['Trigonometry', 'What is the Pythagorean identity?', 'sin²x + cos²x = 1', 'tan²x + 1 = sec²x', '1 + cot²x = csc²x', 'All of the above', 'd'],
    ['Trigonometry', 'What is the value of tan(45°)?', '0', '1', '√2', '-1', 'b'],
    ['Trigonometry', 'If sin x = 3/5, what is cos x?', '4/5', '3/4', '5/3', '2/5', 'a'],
    ['Trigonometry', 'What is the range of the sine function?', '[-1,1]', '[0,1]', '[0,∞]', '[-∞,∞]', 'a'],
    
    # Geometry (5)
    ['Geometry', 'What is the sum of interior angles of a pentagon?', '360°', '540°', '720°', '180°', 'b'],
    ['Geometry', 'What is the formula for the area of a circle?', 'πr²', '2πr', 'πd', 'πr', 'a'],
    ['Geometry', 'A triangle with all sides equal is called?', 'Scalene', 'Isosceles', 'Equilateral', 'Right-angled', 'c'],
    ['Geometry', 'What is the perimeter of a square with side length 5?', '10', '15', '20', '25', 'c'],
    ['Geometry', 'How many faces does a cube have?', '4', '6', '8', '12', 'b'],
    
    # Number Theory (5)
    ['Number Theory', 'What is the smallest prime number?', '0', '1', '2', '3', 'c'],
    ['Number Theory', 'What is 7 mod 3?', '0', '1', '2', '3', 'b'],
    ['Number Theory', 'What is the greatest common divisor (GCD) of 24 and 36?', '6', '8', '12', '24', 'c'],
    ['Number Theory', 'What is the LCM of 4 and 6?', '12', '24', '18', '6', 'a'],
    ['Number Theory', 'How many prime numbers are there between 1 and 10?', '2', '4', '5', '6', 'c'],
    
    # Set Theory (5)
    ['Set Theory', 'If A = {1,2,3} and B = {2,3,4}, what is A ∩ B?', '{1,2,3,4}', '{2,3}', '{1,4}', '{}', 'b'],
    ['Set Theory', 'The empty set is denoted as?', '{}', 'Ø', 'Both', 'None', 'c'],
    ['Set Theory', 'Which of the following is always true for any set A?', 'A ∪ A = A', 'A ∩ A = Ø', 'A ⊆ Ø', 'A ⊆ A', 'd'],
    ['Set Theory', 'What is the cardinality of {a, b, c, d} ?', '2', '3', '4', '5', 'c'],
    ['Set Theory', 'The power set of {1,2} has how many subsets?', '2', '4', '6', '8', 'b'],
    
    # Discrete Mathematics (5)
    ['Discrete Mathematics', 'What is the binary representation of 10?', '1010', '1001', '1100', '1000', 'a'],
    ['Discrete Mathematics', 'A graph with no cycles is called?', 'Tree', 'Cycle', 'Path', 'Loop', 'a'],
    ['Discrete Mathematics', 'In Boolean Algebra, what is 1 AND 0?', '1', '0', 'None', 'Both', 'b'],
    ['Discrete Mathematics', 'What is P → Q in logic?', 'Implication', 'Conjunction', 'Disjunction', 'Negation', 'a'],
    ['Discrete Mathematics', 'Which sorting algorithm has the best time complexity?', 'Bubble Sort', 'Selection Sort', 'Quick Sort', 'Merge Sort', 'd']
]

# Shuffle questions
random.shuffle(Quiz_list)

# File to store results
csv_filename = "student_math_performance.csv"

# Function to check if student ID already exists
def is_duplicate_id(student_id):
    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row and str(row[0]) == str(student_id):
                    return True
    return False

# Function for countdown timer
def countdown_timer(duration, event):
    """Displays countdown timer while waiting for user input"""
    for remaining in range(duration, 0, -1):
        if event.is_set():
            break  # Stop countdown if user answers early
        print(f"\r⏳ Time Left: {remaining} sec", end="", flush=True)
        time.sleep(1)
    if not event.is_set():
        print("\n⏳ Time's up! Moving to next question.")

# Function for non-blocking input with timeout
def input_with_timeout(prompt, timeout):
    """Waits for user input with a timeout"""
    print(prompt, end="", flush=True)
    event = threading.Event()
    
    timer_thread = threading.Thread(target=countdown_timer, args=(timeout, event))
    timer_thread.start()

    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    event.set()  # Stop countdown if input is received

    if ready:
        return sys.stdin.readline().strip().lower()
    return ""  # Return empty input if time runs out

# Get player details
while True:
    name = input("Enter your name: ")
    student_id = input("Enter your student ID: ").strip()
    
    if not student_id.isdigit():
        print("❌ Invalid ID! Please enter a numeric ID.")
        continue

    student_id = int(student_id)

    if is_duplicate_id(student_id):
        print("⚠️ This Student ID already exists! Please enter a different ID.")
    else:
        break

panel = input("Enter your panel: ")

print("\n---------------- YOUR TEST BEGINS --------------\n")

# Initialize variables
score = 0
total_questions = len(Quiz_list)
topic_scores = {}
topic_total = {}
time_taken_per_question = []
time_limit = 30  # Time limit per question (in seconds)
review_data = []  # Store question review details

# Ask questions with a proper countdown timer
for i in range(total_questions):
    question = Quiz_list[i]
    topic = question[0]

    # Initialize topic-wise scores if not present
    if topic not in topic_scores:
        topic_scores[topic] = 0
        topic_total[topic] = 0

    topic_total[topic] += 2  # Each question contributes 2 points to total

    print(f"\nTopic: {topic}")
    print(f"Question {i+1}: {question[1]}")
    print(f"a. {question[2]}")
    print(f"b. {question[3]}")
    print(f"c. {question[4]}")
    print(f"d. {question[5]}")

    # Get user input with timeout handling
    start_time = time.time()
    answer = input_with_timeout("\nEnter your answer (a/b/c/d) before time runs out: \n", time_limit)
    print("\n")
    end_time = time.time()

    # Calculate time taken
    time_taken = end_time - start_time
    time_taken_per_question.append(time_taken)

    # Store for review mode
    correct_answer = question[6]
    if answer == "":
        result = "Skipped"
    elif answer == correct_answer:
        result = "Correct"
        score += 2
        topic_scores[topic] += 2
    else:
        result = f"Incorrect (Correct: {correct_answer})"

    review_data.append([question[1], question[6], answer if answer else "No Answer", result])

    print(f"📝 Your Answer: {answer if answer else 'No Answer'} - {result}\n")

# End of Quiz
print(f"\n🎉 Quiz Complete! {name}, your final score is: {score} / {total_questions * 2} 🎉\n")

# Display individual topic-wise scores
print("\n📊 Topic-wise Performance 📊")
for topic, marks in topic_scores.items():
    total_marks = topic_total[topic]
    print(f"{topic}: {marks} / {total_marks} ({(marks/total_marks)*100:.2f}%)")

# Speed Analysis
avg_time = sum(time_taken_per_question) / total_questions
print(f"\n⏱ **Average Time Per Question:** {avg_time:.2f} seconds")
if avg_time < 10:
    print("🚀 Fast response time! Keep it up!")
elif avg_time < 20:
    print("📈 Good speed, but can be improved.")
else:
    print("🐢 Slow response time. Try to answer faster.")

def recommend_study_plan(score, max_score, topic_scores):
    # Calculate percentage
    percentage = (score / max_score) * 100

    # Determine total study hours based on overall performance
    if percentage <= 30:
        total_hours = 18
    elif percentage <= 60:
        total_hours = 15
    else:
        total_hours = 12  

    # Allocate time per topic
    topic_study_hours = {}
    for topic, marks in topic_scores.items():
        if marks >= 9:
            topic_study_hours[topic] = 1
        elif 7 <= marks <= 8:
            topic_study_hours[topic] = 2.5
        elif 5 <= marks <= 6:
            topic_study_hours[topic] = 4.5
        else:
            topic_study_hours[topic] = 6 

    # Adjust total hours to match allocated study time
    allocated_hours = sum(topic_study_hours.values())
    scaling_factor = total_hours / allocated_hours

    for topic in topic_study_hours:
        topic_study_hours[topic] = round(topic_study_hours[topic] * scaling_factor, 1)

    # Display Recommendations
    print("\n📚 **Recommended Study Plan for the Week** 📚\n")
    print(f"➡️ **Total study hours recommended:** {total_hours} hours per week\n")

    for topic, hours in topic_study_hours.items():
        print(f"📌 **{topic}** → Study **{hours} hours** this week.")

# Generate recommendation
recommend_study_plan(score, total_questions * 2, topic_scores)

# Save the result in a CSV file
file_exists = os.path.exists(csv_filename)

with open(csv_filename, mode="a", newline="") as file:
    writer = csv.writer(file)

    # Write the header only if the file is new
    if not file_exists:
        writer.writerow(["Name", "Student ID", "Panel", "Total Score", "Max Score"] + list(topic_scores.keys()))

    # Create a row with student details and topic-wise scores
    row = [student_id, name, panel, score, total_questions * 2] + [topic_scores.get(topic, 0) for topic in topic_scores.keys()]
    writer.writerow(row)

print(f"\n📂 Your performance has been recorded in {csv_filename}.\n")

Review = input("Do you want to review model?(y/n): ")

if(Review == 'y' or Review == 'Y'):
    for idx, (question_text, correct, user_answer, result) in enumerate(review_data, 1):
        print(f"\n🔹 Question {idx}: {question_text}")
        print(f"✔ Correct Answer: {correct}")
        print(f"❓ Your Answer: {user_answer}")
        print(f"📌 Result: {result}")