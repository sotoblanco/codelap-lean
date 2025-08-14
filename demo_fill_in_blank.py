#!/usr/bin/env python3
"""
Demonstration script for the enhanced fill-in-the-blank coding editor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.exercise_generator import exercise_generator
from services.code_validator import code_validator

def demo_fill_in_blank_system():
    """Demonstrate the fill-in-the-blank exercise system"""
    
    print("🎯 CodeLap Lean - Enhanced Fill-in-the-Blank Coding Editor")
    print("=" * 60)
    print("This demonstration shows how the DataCamp-style coding exercises work.")
    print()
    
    # Generate exercises for different topics
    topics = [
        ("Python Basics", "Learn basic Python syntax and variables", "beginner"),
        ("Functions", "Learn to create and use functions", "intermediate"),
        ("Control Flow", "Learn if statements and loops", "intermediate")
    ]
    
    for topic_title, topic_desc, difficulty in topics:
        print(f"📚 Topic: {topic_title}")
        print(f"   Description: {topic_desc}")
        print(f"   Difficulty: {difficulty}")
        print("-" * 40)
        
        exercises = exercise_generator.generate_exercises_for_step(
            step_title=topic_title,
            step_description=topic_desc,
            difficulty=difficulty
        )
        
        for i, exercise in enumerate(exercises):
            print(f"\nExercise {i+1}: {exercise.title}")
            print(f"Difficulty Level: {i+1} ({len(exercise.blanks)} blanks)")
            print(f"Description: {exercise.description}")
            print()
            
            # Show the code template with blanks
            print("Code Template:")
            lines = exercise.code_template.split('\n')
            for j, line in enumerate(lines):
                print(f"  {j+1:2d} | {line}")
            
            print("\nBlanks to fill:")
            for j, blank in enumerate(exercise.blanks):
                print(f"  {j+1}. {blank['placeholder']}")
                print(f"     Correct Answer: {blank['correct_answer']}")
                print(f"     Hint: {blank['hint']}")
            
            print("\nExpected Solution:")
            lines = exercise.solution.split('\n')
            for j, line in enumerate(lines):
                print(f"  {j+1:2d} | {line}")
            
            print("\n" + "="*60)
    
    # Demonstrate validation
    print("\n🔍 Validation Demonstration")
    print("=" * 40)
    
    # Test with a simple exercise
    exercise_data = {
        "title": "Hello World",
        "description": "Create a simple print statement",
        "code_template": "print({{message}})",
        "solution": 'print("Hello, World!")',
        "blanks": [
            {"placeholder": "{{message}}", "correct_answer": '"Hello, World!"', "hint": "Use quotes around the text"}
        ]
    }
    
    print(f"Exercise: {exercise_data['title']}")
    print(f"Template: {exercise_data['code_template']}")
    print(f"Solution: {exercise_data['solution']}")
    
    # Test different user submissions
    test_cases = [
        ('print("Hello, World!")', "Correct answer"),
        ('print(Hello World)', "Missing quotes"),
        ('print({{message}})', "Not filled"),
        ('print("Wrong message")', "Wrong content")
    ]
    
    for user_code, description in test_cases:
        print(f"\nTesting: {description}")
        print(f"User Code: {user_code}")
        
        result = code_validator.validate_exercise(
            user_code=user_code,
            exercise=exercise_data
        )
        
        print(f"Result: {'✅ Correct' if result.is_valid else '❌ Incorrect'}")
        print(f"Score: {result.score}/100")
        print(f"Feedback: {result.feedback}")
        if result.hints:
            print(f"Hints: {', '.join(result.hints)}")

def demo_progressive_difficulty():
    """Demonstrate progressive difficulty levels"""
    
    print("\n📈 Progressive Difficulty Demonstration")
    print("=" * 50)
    
    exercises = exercise_generator.generate_exercises_for_step(
        step_title="Functions",
        step_description="Learn to create and use functions",
        difficulty="intermediate"
    )
    
    for i, exercise in enumerate(exercises):
        level = i + 1
        print(f"\n🎯 Level {level} Exercise: {exercise.title}")
        print(f"   Blanks: {len(exercise.blanks)}")
        print(f"   Hints: {len(exercise.hints)}")
        print(f"   Difficulty: {exercise.difficulty}")
        
        print("\n   Code Template:")
        lines = exercise.code_template.split('\n')
        for j, line in enumerate(lines):
            print(f"     {j+1:2d} | {line}")
        
        print("\n   Blanks:")
        for j, blank in enumerate(exercise.blanks):
            print(f"     {j+1}. {blank['placeholder']} -> {blank['correct_answer']}")
        
        print("\n   Hints:")
        for j, hint in enumerate(exercise.hints):
            print(f"     {j+1}. {hint}")

def demo_learning_benefits():
    """Demonstrate the learning benefits"""
    
    print("\n🎓 Learning Benefits")
    print("=" * 30)
    
    benefits = [
        "✅ Guided Learning: Step-by-step code completion",
        "✅ Immediate Feedback: Real-time validation and hints",
        "✅ Progressive Difficulty: Builds confidence gradually",
        "✅ Visual Progress: Clear indication of completion status",
        "✅ Interactive Experience: Engaging DataCamp-style interface",
        "✅ Contextual Hints: Smart hints for each blank",
        "✅ Syntax Highlighting: Professional code editor appearance",
        "✅ Mobile Responsive: Works on all devices"
    ]
    
    for benefit in benefits:
        print(benefit)

if __name__ == "__main__":
    demo_fill_in_blank_system()
    demo_progressive_difficulty()
    demo_learning_benefits()
    
    print("\n" + "="*60)
    print("🎉 Enhanced Fill-in-the-Blank Coding Editor Demo Complete!")
    print("\nTo use this system:")
    print("1. Start the backend: python app.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Navigate to a learning step with coding exercises")
    print("4. Experience the interactive fill-in-the-blank exercises!")
    print("\nFor more information, see ENHANCED_CODING_EDITOR_README.md")
