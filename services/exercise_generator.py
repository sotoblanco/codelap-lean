import uuid
from typing import List, Dict
from database.schemas import CodingExercise

class ExerciseGenerator:
    """Generates coding exercises for different programming topics"""
    
    def __init__(self):
        self.exercise_templates = self._load_exercise_templates()
    
    def _load_exercise_templates(self) -> Dict[str, List[Dict]]:
        """Load exercise templates for different topics"""
        return {
            "python_basics": [
                {
                    "title": "Hello World",
                    "description": "Create a simple print statement to output 'Hello, World!'",
                    "difficulty": "beginner",
                    "code_template": "print({{message}})",
                    "solution": 'print("Hello, World!")',
                    "hints": ["Use the print() function", "Remember to use quotes for strings"],
                    "validation_rules": ["contains:print", "contains:Hello, World!"],
                    "expected_output": "Hello, World!",
                    "blanks": [
                        {"placeholder": "{{message}}", "correct_answer": '"Hello, World!"', "hint": "Use quotes around the text"}
                    ]
                },
                {
                    "title": "Variable Assignment",
                    "description": "Create a variable named 'name' and assign it your name, then print it",
                    "difficulty": "beginner",
                    "code_template": "{{variable_name}} = {{value}}\nprint({{variable_name}})",
                    "solution": 'name = "John"\nprint(name)',
                    "hints": ["Use the = operator to assign values", "Variable names should be descriptive"],
                    "validation_rules": ["contains:=", "contains:print", "function:name"],
                    "expected_output": "John",
                    "blanks": [
                        {"placeholder": "{{variable_name}}", "correct_answer": "name", "hint": "Use a descriptive variable name"},
                        {"placeholder": "{{value}}", "correct_answer": '"John"', "hint": "Use quotes for string values"},
                        {"placeholder": "{{variable_name}}", "correct_answer": "name", "hint": "Use the same variable name you defined"}
                    ]
                },
                {
                    "title": "Basic Math",
                    "description": "Calculate the sum of two numbers and store it in a variable called 'result'",
                    "difficulty": "beginner",
                    "code_template": "a = {{number1}}\nb = {{number2}}\nresult = {{calculation}}\nprint(result)",
                    "solution": "a = 5\nb = 3\nresult = a + b\nprint(result)",
                    "hints": ["Use the + operator for addition", "Make sure to assign the result to a variable"],
                    "validation_rules": ["contains:+", "contains:result", "contains:print"],
                    "expected_output": "8",
                    "blanks": [
                        {"placeholder": "{{number1}}", "correct_answer": "5", "hint": "Choose any number"},
                        {"placeholder": "{{number2}}", "correct_answer": "3", "hint": "Choose another number"},
                        {"placeholder": "{{calculation}}", "correct_answer": "a + b", "hint": "Add the two variables together"}
                    ]
                }
            ],
            "functions": [
                {
                    "title": "Simple Function",
                    "description": "Create a function called 'greet' that takes a name parameter and returns a greeting",
                    "difficulty": "intermediate",
                    "code_template": "def {{function_name}}({{parameter}}):\n    return {{return_value}}\n\nprint(greet('Alice'))",
                    "solution": 'def greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Alice"))',
                    "hints": ["Use 'def' to define a function", "Use f-strings for string formatting"],
                    "validation_rules": ["function:greet", "contains:def", "contains:return"],
                    "expected_output": "Hello, Alice!",
                    "blanks": [
                        {"placeholder": "{{function_name}}", "correct_answer": "greet", "hint": "Use the function name 'greet'"},
                        {"placeholder": "{{parameter}}", "correct_answer": "name", "hint": "Use 'name' as the parameter"},
                        {"placeholder": "{{return_value}}", "correct_answer": 'f"Hello, {name}!"', "hint": "Use an f-string to format the greeting"}
                    ]
                },
                {
                    "title": "Function with Parameters",
                    "description": "Create a function called 'add_numbers' that takes two parameters and returns their sum",
                    "difficulty": "intermediate",
                    "code_template": "def {{function_name}}({{param1}}, {{param2}}):\n    return {{calculation}}\n\nresult = add_numbers(10, 5)\nprint(result)",
                    "solution": "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(10, 5)\nprint(result)",
                    "hints": ["Function parameters go in parentheses", "Use the return statement to send back a value"],
                    "validation_rules": ["function:add_numbers", "contains:return", "contains:+"],
                    "expected_output": "15",
                    "blanks": [
                        {"placeholder": "{{function_name}}", "correct_answer": "add_numbers", "hint": "Use the function name 'add_numbers'"},
                        {"placeholder": "{{param1}}", "correct_answer": "a", "hint": "Use 'a' as the first parameter"},
                        {"placeholder": "{{param2}}", "correct_answer": "b", "hint": "Use 'b' as the second parameter"},
                        {"placeholder": "{{calculation}}", "correct_answer": "a + b", "hint": "Add the two parameters together"}
                    ]
                }
            ],
            "data_structures": [
                {
                    "title": "List Operations",
                    "description": "Create a list of numbers and find the sum of all elements",
                    "difficulty": "intermediate",
                    "code_template": "numbers = [{{list_values}}]\ntotal = {{calculation}}\nprint(total)",
                    "solution": "numbers = [1, 2, 3, 4, 5]\ntotal = sum(numbers)\nprint(total)",
                    "hints": ["Use square brackets for lists", "The sum() function adds all numbers in a list"],
                    "validation_rules": ["contains:[", "contains:sum", "contains:print"],
                    "expected_output": "15",
                    "blanks": [
                        {"placeholder": "{{list_values}}", "correct_answer": "1, 2, 3, 4, 5", "hint": "Create a list with some numbers"},
                        {"placeholder": "{{calculation}}", "correct_answer": "sum(numbers)", "hint": "Use the sum() function on the list"}
                    ]
                },
                {
                    "title": "Dictionary Creation",
                    "description": "Create a dictionary with keys 'name' and 'age', then print the age",
                    "difficulty": "intermediate",
                    "code_template": "person = {{{{'name': 'John', 'age': 30}}}}\nprint(person['{{key}}'])",
                    "solution": "person = {'name': 'John', 'age': 30}\nprint(person['age'])",
                    "hints": ["Use curly braces for dictionaries", "Access values using square brackets"],
                    "validation_rules": ["contains:{", "contains:print", "contains:person"],
                    "expected_output": "30",
                    "blanks": [
                        {"placeholder": "{{'name': 'John', 'age': 30}}", "correct_answer": "'name': 'John', 'age': 30", "hint": "Create key-value pairs for name and age"},
                        {"placeholder": "{{key}}", "correct_answer": "age", "hint": "Use the key 'age' to access the age value"}
                    ]
                }
            ],
            "control_flow": [
                {
                    "title": "If Statement",
                    "description": "Create a function that checks if a number is positive, negative, or zero",
                    "difficulty": "intermediate",
                    "code_template": "def check_number({{parameter}}):\n    if {{condition1}}:\n        return {{result1}}\n    elif {{condition2}}:\n        return {{result2}}\n    else:\n        return {{result3}}\n\nprint(check_number(5))",
                    "solution": 'def check_number(num):\n    if num > 0:\n        return "Positive"\n    elif num < 0:\n        return "Negative"\n    else:\n        return "Zero"\n\nprint(check_number(5))',
                    "hints": ["Use if, elif, and else statements", "Compare numbers using >, <, =="],
                    "validation_rules": ["function:check_number", "contains:if", "contains:elif", "contains:else"],
                    "expected_output": "Positive",
                    "blanks": [
                        {"placeholder": "{{parameter}}", "correct_answer": "num", "hint": "Use 'num' as the parameter name"},
                        {"placeholder": "{{condition1}}", "correct_answer": "num > 0", "hint": "Check if the number is greater than 0"},
                        {"placeholder": "{{result1}}", "correct_answer": '"Positive"', "hint": "Return 'Positive' for positive numbers"},
                        {"placeholder": "{{condition2}}", "correct_answer": "num < 0", "hint": "Check if the number is less than 0"},
                        {"placeholder": "{{result2}}", "correct_answer": '"Negative"', "hint": "Return 'Negative' for negative numbers"},
                        {"placeholder": "{{result3}}", "correct_answer": '"Zero"', "hint": "Return 'Zero' for zero"}
                    ]
                },
                {
                    "title": "For Loop",
                    "description": "Create a function that prints all even numbers from 1 to 10",
                    "difficulty": "intermediate",
                    "code_template": "def print_even_numbers():\n    for {{variable}} in range({{start}}, {{end}}):\n        if {{condition}}:\n            print({{variable}})\n\nprint_even_numbers()",
                    "solution": "def print_even_numbers():\n    for i in range(1, 11):\n        if i % 2 == 0:\n            print(i)\n\nprint_even_numbers()",
                    "hints": ["Use range() to create a sequence", "Use % operator to check for even numbers"],
                    "validation_rules": ["function:print_even_numbers", "contains:for", "contains:if", "contains:%"],
                    "expected_output": "2\n4\n6\n8\n10",
                    "blanks": [
                        {"placeholder": "{{variable}}", "correct_answer": "i", "hint": "Use 'i' as the loop variable"},
                        {"placeholder": "{{start}}", "correct_answer": "1", "hint": "Start from 1"},
                        {"placeholder": "{{end}}", "correct_answer": "11", "hint": "End at 11 (exclusive)"},
                        {"placeholder": "{{condition}}", "correct_answer": "i % 2 == 0", "hint": "Check if the number is even using modulo"},
                        {"placeholder": "{{variable}}", "correct_answer": "i", "hint": "Print the loop variable"}
                    ]
                }
            ],
            "fastapi_basics": [
                {
                    "title": "Basic FastAPI Route",
                    "description": "Create a simple FastAPI route that returns a JSON response",
                    "difficulty": "intermediate",
                    "code_template": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/{{route}}')\ndef {{function_name}}():\n    return {{{{'message': 'Hello from FastAPI!'}}}}\n",
                    "solution": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/hello')\ndef hello():\n    return {'message': 'Hello from FastAPI!'}",
                    "hints": ["Import FastAPI", "Use the @app.get decorator", "Return a dictionary for JSON response"],
                    "validation_rules": ["import:fastapi", "contains:@app.get", "contains:return"],
                    "expected_output": "{'message': 'Hello from FastAPI!'}",
                    "blanks": [
                        {"placeholder": "{{route}}", "correct_answer": "hello", "hint": "Use 'hello' as the route path"},
                        {"placeholder": "{{function_name}}", "correct_answer": "hello", "hint": "Use 'hello' as the function name"},
                        {"placeholder": "{{'message': 'Hello from FastAPI!'}}", "correct_answer": "'message': 'Hello from FastAPI!'", "hint": "Create a dictionary with a message key"}
                    ]
                },
                {
                    "title": "Route with Parameters",
                    "description": "Create a FastAPI route that accepts a name parameter and returns a personalized greeting",
                    "difficulty": "intermediate",
                    "code_template": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/greet/{{parameter}}')\ndef greet({{parameter}}: str):\n    return {{{{'message': f'Hello, {{parameter}}!'}}}}\n",
                    "solution": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/greet/{name}')\ndef greet(name: str):\n    return {'message': f'Hello, {name}!'}",
                    "hints": ["Use path parameters with curly braces", "Add type hints to parameters", "Use f-strings for formatting"],
                    "validation_rules": ["import:fastapi", "contains:@app.get", "contains:str"],
                    "expected_output": "{'message': 'Hello, John!'}",
                    "blanks": [
                        {"placeholder": "{{parameter}}", "correct_answer": "{name}", "hint": "Use {name} as the path parameter"},
                        {"placeholder": "{{parameter}}", "correct_answer": "name", "hint": "Use 'name' as the function parameter"},
                        {"placeholder": "{{parameter}}", "correct_answer": "name", "hint": "Use 'name' in the f-string"}
                    ]
                }
            ]
        }
    
    def generate_exercises_for_step(self, step_title: str, step_description: str, difficulty: str = "intermediate") -> List[CodingExercise]:
        """Generate coding exercises for a specific learning step"""
        exercises = []
        
        # Determine topic based on step content
        topic = self._determine_topic(step_title, step_description)
        
        # Get exercises for the topic
        topic_exercises = self.exercise_templates.get(topic, self.exercise_templates["python_basics"])
        
        # Filter by difficulty if specified
        if difficulty:
            topic_exercises = [ex for ex in topic_exercises if ex["difficulty"] == difficulty]
        
        # Generate 2-3 exercises per step with progressive difficulty
        num_exercises = min(3, len(topic_exercises))
        
        for i in range(num_exercises):
            exercise_data = topic_exercises[i]
            
            # Create progressive difficulty by adjusting blanks
            if i == 0:  # First exercise - fewer blanks
                exercise_data = self._create_beginner_version(exercise_data)
            elif i == 1:  # Second exercise - more blanks
                exercise_data = self._create_intermediate_version(exercise_data)
            else:  # Third exercise - most blanks
                exercise_data = self._create_advanced_version(exercise_data)
            
            exercise = CodingExercise(
                id=str(uuid.uuid4()),
                title=exercise_data["title"],
                description=exercise_data["description"],
                difficulty=exercise_data["difficulty"],
                code_template=exercise_data["code_template"],
                solution=exercise_data["solution"],
                hints=exercise_data["hints"],
                validation_rules=exercise_data["validation_rules"],
                expected_output=exercise_data.get("expected_output"),
                test_cases=exercise_data.get("test_cases", []),
                blanks=exercise_data.get("blanks", [])
            )
            exercises.append(exercise)
        
        return exercises
    
    def _create_beginner_version(self, exercise_data: Dict) -> Dict:
        """Create a beginner version with fewer blanks and more hints"""
        beginner_data = exercise_data.copy()
        if "blanks" in beginner_data:
            # Keep only the first 2-3 blanks for beginners
            beginner_data["blanks"] = beginner_data["blanks"][:2]
            # Add more hints
            beginner_data["hints"].extend([
                "Take your time to understand each part",
                "Check the syntax carefully"
            ])
        return beginner_data
    
    def _create_intermediate_version(self, exercise_data: Dict) -> Dict:
        """Create an intermediate version with more blanks"""
        intermediate_data = exercise_data.copy()
        if "blanks" in intermediate_data:
            # Keep most blanks but not all
            intermediate_data["blanks"] = intermediate_data["blanks"][:4]
        return intermediate_data
    
    def _create_advanced_version(self, exercise_data: Dict) -> Dict:
        """Create an advanced version with all blanks and fewer hints"""
        advanced_data = exercise_data.copy()
        if "blanks" in advanced_data:
            # Keep all blanks
            advanced_data["blanks"] = advanced_data["blanks"]
            # Remove some hints to make it more challenging
            if len(advanced_data["hints"]) > 2:
                advanced_data["hints"] = advanced_data["hints"][:2]
        return advanced_data
    
    def _determine_topic(self, step_title: str, step_description: str) -> str:
        """Determine the programming topic based on step content"""
        content = (step_title + " " + step_description).lower()
        
        if any(word in content for word in ["fastapi", "api", "route", "endpoint"]):
            return "fastapi_basics"
        elif any(word in content for word in ["function", "def", "parameter"]):
            return "functions"
        elif any(word in content for word in ["list", "dictionary", "tuple", "set"]):
            return "data_structures"
        elif any(word in content for word in ["if", "else", "for", "while", "loop"]):
            return "control_flow"
        else:
            return "python_basics"

# Global exercise generator instance
exercise_generator = ExerciseGenerator()
