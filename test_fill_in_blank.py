#!/usr/bin/env python3
"""
Test script for fill-in-the-blank coding exercises
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.exercise_generator import exercise_generator
from services.code_validator import code_validator

def test_fill_in_blank_exercises():
    """Test the fill-in-the-blank exercise generation and validation"""
    
    print("🧪 Testing Fill-in-the-Blank Exercise System")
    print("=" * 50)
    
    # Test exercise generation
    print("\n1. Testing Exercise Generation...")
    exercises = exercise_generator.generate_exercises_for_step(
        step_title="Python Basics",
        step_description="Learn basic Python syntax and variables",
        difficulty="beginner"
    )
    
    print(f"Generated {len(exercises)} exercises")
    
    for i, exercise in enumerate(exercises):
        print(f"\nExercise {i+1}: {exercise.title}")
        print(f"Difficulty: {exercise.difficulty}")
        print(f"Blanks: {len(exercise.blanks)}")
        print(f"Template: {exercise.code_template}")
        
        if exercise.blanks:
            print("Blanks:")
            for j, blank in enumerate(exercise.blanks):
                print(f"  {j+1}. {blank['placeholder']} -> {blank['correct_answer']}")
                print(f"     Hint: {blank['hint']}")
    
    # Test validation with correct answers
    print("\n2. Testing Validation with Correct Answers...")
    if exercises:
        exercise = exercises[0]
        if exercise.blanks:
            # Create correct code by replacing placeholders
            correct_code = exercise.code_template
            for blank in exercise.blanks:
                correct_code = correct_code.replace(blank['placeholder'], blank['correct_answer'])
            
            print(f"Original template: {exercise.code_template}")
            print(f"Correct code: {correct_code}")
            
            # Validate correct code
            validation_result = code_validator.validate_exercise(
                user_code=correct_code,
                exercise={
                    "solution": exercise.solution,
                    "validation_rules": exercise.validation_rules,
                    "blanks": exercise.blanks
                }
            )
            
            print(f"Validation result: {validation_result.is_valid}")
            print(f"Score: {validation_result.score}")
            print(f"Feedback: {validation_result.feedback}")
    
    # Test validation with incorrect answers
    print("\n3. Testing Validation with Incorrect Answers...")
    if exercises and exercises[0].blanks:
        exercise = exercises[0]
        # Create incorrect code
        incorrect_code = exercise.code_template
        for blank in exercise.blanks:
            incorrect_code = incorrect_code.replace(blank['placeholder'], "WRONG_ANSWER")
        
        print(f"Incorrect code: {incorrect_code}")
        
        validation_result = code_validator.validate_exercise(
            user_code=incorrect_code,
            exercise={
                "solution": exercise.solution,
                "validation_rules": exercise.validation_rules,
                "blanks": exercise.blanks
            }
        )
        
        print(f"Validation result: {validation_result.is_valid}")
        print(f"Score: {validation_result.score}")
        print(f"Feedback: {validation_result.feedback}")
        print(f"Hints: {validation_result.hints}")
    
    # Test progressive difficulty
    print("\n4. Testing Progressive Difficulty...")
    exercises = exercise_generator.generate_exercises_for_step(
        step_title="Functions",
        step_description="Learn to create and use functions",
        difficulty="intermediate"
    )
    
    for i, exercise in enumerate(exercises):
        print(f"\nExercise {i+1} (Difficulty Level {i+1}):")
        print(f"  Blanks: {len(exercise.blanks)}")
        print(f"  Hints: {len(exercise.hints)}")
        print(f"  Title: {exercise.title}")
    
    print("\n✅ Fill-in-the-Blank Exercise Tests Completed!")

def test_specific_exercise():
    """Test a specific exercise template"""
    
    print("\n🔍 Testing Specific Exercise Template")
    print("=" * 40)
    
    # Test the "Hello World" exercise
    exercise_data = {
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
    }
    
    print(f"Exercise: {exercise_data['title']}")
    print(f"Template: {exercise_data['code_template']}")
    print(f"Expected: {exercise_data['solution']}")
    
    # Test with correct answer
    correct_code = 'print("Hello, World!")'
    print(f"\nTesting correct code: {correct_code}")
    
    validation_result = code_validator.validate_exercise(
        user_code=correct_code,
        exercise=exercise_data
    )
    
    print(f"Result: {validation_result.is_valid}")
    print(f"Score: {validation_result.score}")
    print(f"Feedback: {validation_result.feedback}")
    
    # Test with incorrect answer
    incorrect_code = 'print(WRONG)'
    print(f"\nTesting incorrect code: {incorrect_code}")
    
    validation_result = code_validator.validate_exercise(
        user_code=incorrect_code,
        exercise=exercise_data
    )
    
    print(f"Result: {validation_result.is_valid}")
    print(f"Score: {validation_result.score}")
    print(f"Feedback: {validation_result.feedback}")

if __name__ == "__main__":
    test_fill_in_blank_exercises()
    test_specific_exercise()
