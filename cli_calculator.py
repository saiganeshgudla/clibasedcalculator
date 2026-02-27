# ==========================================================
# GenAlpha CLI Calculator
# Advanced Stack-Based Expression Evaluator
# Supports: +  -  *  /  ^  ( )  Decimals
# Data Structures Used: Arrays (list) + Stacks (list)
# ==========================================================


class CalculatorCLI:
    def __init__(self):
        self.history = []          # Array for storing calculation history
        self.result_stack = []     # Stack for undo functionality

    # ------------------------------------------------------
    # Operator Precedence
    # ------------------------------------------------------
    def precedence(self, op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        if op == '^':
            return 3
        return 0

    # ------------------------------------------------------
    # Check if token is a valid number (supports decimals)
    # ------------------------------------------------------
    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    # ------------------------------------------------------
    # Infix → Postfix Conversion (Stack Based)
    # ------------------------------------------------------
    def infix_to_postfix(self, expression):
        stack = []      # operator stack
        postfix = []    # output list (array)

        tokens = expression.split()

        for token in tokens:

            if self.is_number(token):
                postfix.append(token)

            elif token == '(':
                stack.append(token)

            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses")
                stack.pop()

            else:  # operator
                while (
                    stack and
                    stack[-1] != '(' and
                    (
                        self.precedence(stack[-1]) > self.precedence(token)
                        or (
                            self.precedence(stack[-1]) == self.precedence(token)
                            and token != '^'  # Right-associative power
                        )
                    )
                ):
                    postfix.append(stack.pop())

                stack.append(token)

        while stack:
            if stack[-1] == '(':
                raise ValueError("Mismatched parentheses")
            postfix.append(stack.pop())

        return postfix

    # ------------------------------------------------------
    # Postfix Evaluation (Stack Based)
    # ------------------------------------------------------
    def evaluate_postfix(self, postfix):
        stack = []

        for token in postfix:

            if self.is_number(token):
                stack.append(float(token))

            else:
                if len(stack) < 2:
                    raise ValueError("Invalid Expression")

                b = stack.pop()
                a = stack.pop()

                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
                else:
                    raise ValueError("Unknown operator")

        if len(stack) != 1:
            raise ValueError("Invalid Expression")

        return stack[0]

    # ------------------------------------------------------
    # Calculate Expression
    # ------------------------------------------------------
    def calculate(self, expression):
        try:
            postfix = self.infix_to_postfix(expression)
            result = self.evaluate_postfix(postfix)

            self.history.append(f"{expression} = {result}")
            self.result_stack.append(result)

            print("Result:", result)

        except Exception as e:
            print("Error:", e)

    # ------------------------------------------------------
    # Undo Last Calculation
    # ------------------------------------------------------
    def undo(self):
        if self.result_stack:
            self.result_stack.pop()
            removed = self.history.pop()
            print("Undone:", removed)
        else:
            print("Nothing to undo")

    # ------------------------------------------------------
    # Show History
    # ------------------------------------------------------
    def show_history(self):
        print("\n--- Calculation History ---")
        if not self.history:
            print("No history available")
        else:
            for h in self.history:
                print(h)


# ==========================================================
# CLI INTERFACE
# ==========================================================

def main():
    calc = CalculatorCLI()

    while True:
        print("\n========== GenAlpha CLI Calculator ==========")
        print("1. Calculate Expression")
        print("2. Undo Last")
        print("3. Show History")
        print("4. Exit")
        print("=============================================")

        choice = input("Choose option: ").strip()

        if choice == "1":
            print("\nEnter expression with spaces.")
            print("Example: ( 2.5 + 3 ) ^ 2")
            expression = input("Expression: ").strip()
            calc.calculate(expression)

        elif choice == "2":
            calc.undo()

        elif choice == "3":
            calc.show_history()

        elif choice == "4":
            print("Exiting GenAlpha Calculator...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()