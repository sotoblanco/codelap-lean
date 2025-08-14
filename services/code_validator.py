import ast
import subprocess
import tempfile
import os
import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    feedback: str
    score: int
    execution_result: Optional[str] = None
    error_message: Optional[str] = None
    hints: List[str] = None

class CodeValidator:
    """Validates Python code submissions for coding exercises"""
    
    def __init__(self):
        self.safe_modules = {
            'math', 'random', 'datetime', 'collections', 'itertools',
            'functools', 'operator', 're', 'json', 'os', 'sys'
        }
    
    def validate_exercise(
        self, 
        user_code: str, 
        exercise: Dict,
        test_cases: List[Dict] = None
    ) -> ValidationResult:
        """Validate user code against exercise requirements"""
        
        # Basic syntax validation
        syntax_result = self._validate_syntax(user_code)
        if not syntax_result.is_valid:
            return syntax_result
        
        # Security validation
        security_result = self._validate_security(user_code)
        if not security_result.is_valid:
            return security_result
        
        # Fill-in-the-blank validation if blanks are provided
        if exercise.get("blanks"):
            blank_result = self._validate_fill_in_blanks(user_code, exercise)
            if not blank_result.is_valid:
                return blank_result
        
        # Run test cases if provided
        if test_cases:
            test_result = self._run_test_cases(user_code, test_cases)
            if not test_result.is_valid:
                return test_result
        
        # Check against solution patterns
        pattern_result = self._validate_patterns(user_code, exercise)
        
        return pattern_result
    
    def _validate_syntax(self, code: str) -> ValidationResult:
        """Check if the code has valid Python syntax"""
        try:
            ast.parse(code)
            return ValidationResult(
                is_valid=True,
                feedback="Syntax is valid",
                score=100,
                hints=[]
            )
        except SyntaxError as e:
            return ValidationResult(
                is_valid=False,
                feedback=f"Syntax error: {str(e)}",
                score=0,
                error_message=str(e),
                hints=["Check your Python syntax", "Make sure all parentheses and brackets are properly closed"]
            )
    
    def _validate_security(self, code: str) -> ValidationResult:
        """Check for potentially dangerous code"""
        dangerous_patterns = [
            r'__import__\s*\(',
            r'eval\s*\(',
            r'exec\s*\(',
            r'open\s*\(',
            r'input\s*\(',
            r'file\s*\(',
            r'compile\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'vars\s*\(',
            r'dir\s*\(',
            r'help\s*\(',
            r'breakpoint\s*\(',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                return ValidationResult(
                    is_valid=False,
                    feedback="This code contains potentially unsafe operations",
                    score=0,
                    error_message="Security violation detected",
                    hints=["Avoid using eval(), exec(), or other potentially dangerous functions"]
                )
        
        return ValidationResult(
            is_valid=True,
            feedback="Code passes security checks",
            score=100,
            hints=[]
        )
    
    def _validate_fill_in_blanks(self, code: str, exercise: Dict) -> ValidationResult:
        """Validate fill-in-the-blank exercises"""
        blanks = exercise.get("blanks", [])
        template = exercise.get("code_template", "")
        
        if not blanks or not template:
            return ValidationResult(
                is_valid=True,
                feedback="No blanks to validate",
                score=100,
                hints=[]
            )
        
        # For fill-in-the-blank exercises, we'll use pattern matching
        # since the user code should match the expected solution pattern
        solution = exercise.get("solution", "")
        
        # Validate each blank by checking if the code matches the expected pattern
        correct_count = 0
        total_blanks = len(blanks)
        feedback_parts = []
        hints = []
        
        # Check if the code matches the solution pattern
        normalized_code = self._normalize_answer(code.strip())
        normalized_solution = self._normalize_answer(solution.strip())
        
        if normalized_code == normalized_solution:
            correct_count = total_blanks
            feedback = "Perfect! All blanks are filled correctly."
        else:
            # Check individual blanks by comparing with template
            for i, blank in enumerate(blanks):
                placeholder = blank.get("placeholder", "")
                correct_answer = blank.get("correct_answer", "")
                hint = blank.get("hint", "")
                
                # Check if the placeholder is still in the code (not filled)
                if placeholder in code:
                    feedback_parts.append(f"Blank {i+1}: Not filled")
                    hints.append(f"Hint for blank {i+1}: {hint}")
                else:
                    # Check if the code contains the correct answer pattern
                    normalized_correct = self._normalize_answer(correct_answer)
                    if normalized_correct in normalized_code:
                        correct_count += 1
                    else:
                        feedback_parts.append(f"Blank {i+1}: Incorrect answer")
                        hints.append(f"Hint for blank {i+1}: {hint}")
        
        # Calculate score
        score = int((correct_count / total_blanks) * 100) if total_blanks > 0 else 0
        
        # Generate feedback if not already set
        if correct_count != total_blanks:
            if correct_count > 0:
                feedback = f"Good progress! {correct_count}/{total_blanks} blanks correct. {', '.join(feedback_parts)}"
            else:
                feedback = f"Try again. {', '.join(feedback_parts)}"
        
        return ValidationResult(
            is_valid=correct_count == total_blanks,
            feedback=feedback,
            score=score,
            hints=hints
        )
    
    def _extract_user_answers(self, code: str, template: str, blanks: List[Dict]) -> Dict[str, str]:
        """Extract user answers from the code based on the template"""
        user_answers = {}
        
        # For now, we'll use a simple approach: compare the code with the template
        # and identify what the user has filled in
        for blank in blanks:
            placeholder = blank.get("placeholder", "")
            correct_answer = blank.get("correct_answer", "")
            
            # Check if the placeholder is still in the code (not filled)
            if placeholder in code:
                user_answers[placeholder] = placeholder  # Not filled
            else:
                # The placeholder has been replaced, try to extract the answer
                # This is a simplified approach - in a real implementation, you'd need
                # more sophisticated parsing
                user_answers[placeholder] = correct_answer  # Assume correct for now
        
        return user_answers
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison"""
        # Remove extra whitespace
        normalized = answer.strip()
        
        # Remove extra quotes if they're not part of the answer
        if normalized.startswith('"') and normalized.endswith('"'):
            normalized = normalized[1:-1]
        elif normalized.startswith("'") and normalized.endswith("'"):
            normalized = normalized[1:-1]
        
        return normalized
    
    def _run_test_cases(self, code: str, test_cases: List[Dict]) -> ValidationResult:
        """Run test cases against the user code"""
        try:
            # Create a temporary file with the user code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Add test execution code
            test_code = f"""
{code}

# Test execution
if __name__ == "__main__":
    results = []
    errors = []
    
    try:
        # Test case 1: Basic functionality
        result = main()  # Assuming main() is the function to test
        results.append(result)
    except Exception as e:
        errors.append(str(e))
    
    print(json.dumps({{"results": results, "errors": errors}}))
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                test_file = f.name
            
            # Execute the test
            result = subprocess.run(
                ['python3', test_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Clean up temporary files
            os.unlink(temp_file)
            os.unlink(test_file)
            
            if result.returncode != 0:
                return ValidationResult(
                    is_valid=False,
                    feedback="Code execution failed",
                    score=0,
                    error_message=result.stderr,
                    hints=["Check your code logic", "Make sure all variables are defined"]
                )
            
            # Parse results
            try:
                output = json.loads(result.stdout.strip())
                if output.get("errors"):
                    return ValidationResult(
                        is_valid=False,
                        feedback="Code produced errors during execution",
                        score=0,
                        error_message=", ".join(output["errors"]),
                        hints=["Check your function implementation", "Verify all variables are properly initialized"]
                    )
                
                return ValidationResult(
                    is_valid=True,
                    feedback="Code executed successfully",
                    score=100,
                    execution_result=str(output.get("results", [])),
                    hints=[]
                )
                
            except json.JSONDecodeError:
                return ValidationResult(
                    is_valid=True,
                    feedback="Code executed successfully",
                    score=100,
                    execution_result=result.stdout,
                    hints=[]
                )
                
        except subprocess.TimeoutExpired:
            return ValidationResult(
                is_valid=False,
                feedback="Code execution timed out",
                score=0,
                error_message="Execution timeout",
                hints=["Check for infinite loops", "Optimize your code"]
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                feedback="Error during code execution",
                score=0,
                error_message=str(e),
                hints=["Check your code structure", "Make sure all imports are correct"]
            )
    
    def _validate_patterns(self, code: str, exercise: Dict) -> ValidationResult:
        """Validate code against expected patterns and solution"""
        solution = exercise.get("solution", "")
        validation_rules = exercise.get("validation_rules", [])
        
        score = 100
        feedback_parts = []
        hints = []
        
        # Check for required patterns
        for rule in validation_rules:
            if rule.startswith("contains:"):
                pattern = rule.split(":", 1)[1]
                if pattern not in code:
                    score -= 20
                    feedback_parts.append(f"Missing required pattern: {pattern}")
                    hints.append(f"Make sure your code includes: {pattern}")
            
            elif rule.startswith("function:"):
                func_name = rule.split(":", 1)[1]
                if f"def {func_name}" not in code:
                    score -= 30
                    feedback_parts.append(f"Missing required function: {func_name}")
                    hints.append(f"Define a function named: {func_name}")
            
            elif rule.startswith("import:"):
                module = rule.split(":", 1)[1]
                if f"import {module}" not in code and f"from {module}" not in code:
                    score -= 15
                    feedback_parts.append(f"Missing required import: {module}")
                    hints.append(f"Import the {module} module")
        
        # Check code length (basic complexity check)
        if len(code.strip()) < 10:
            score -= 20
            feedback_parts.append("Code seems too short")
            hints.append("Make sure you've implemented the required functionality")
        
        # Generate feedback
        if score == 100:
            feedback = "Excellent! Your code meets all requirements."
        elif score >= 80:
            feedback = f"Good work! {', '.join(feedback_parts)}"
        elif score >= 60:
            feedback = f"Almost there! {', '.join(feedback_parts)}"
        else:
            feedback = f"Try again. {', '.join(feedback_parts)}"
        
        return ValidationResult(
            is_valid=score >= 70,
            feedback=feedback,
            score=max(0, score),
            hints=hints
        )

# Global validator instance
code_validator = CodeValidator()
