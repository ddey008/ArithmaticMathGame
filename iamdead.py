import sympy as sp


class YourClass:
    def answer(self):
        # Example input string
        answer_text = "8*x**3 + 14*cot(x)*(-csc(x))*cot(x)"

        # Correct answer from your method (assuming it returns a string)
        correct_ans_str = "8*x**3 - 14*cos(x)/sin(x)**3"
        correct_ans = sp.simplify(sp.sympify(correct_ans_str))

        # Perform string corrections directly in the answer text
        answer_text = self.answer_string_correction(answer_text)

        try:
            # Parse and simplify the corrected answer text
            answer_expr = sp.simplify(answer_text)

            print("Correct answer:", correct_ans)
            print("Answer text:", answer_expr)

            # Check if the simplified expressions match
            if answer_expr.equals(correct_ans) or sp.simplify(answer_expr - correct_ans) == 0:
                print("Correct!")
            else:
                print("Incorrect.")

        except sp.SympifyError as e:
            print("Error parsing expression:", e)

    def answer_string_correction(self, text):
        # Replace '^' with '**'
        text = text.replace("^", "**")

        # Replace cot(x) and csc(x) with SymPy functions
        text = text.replace("cot(x)", "cot(x)")
        text = text.replace("-csc(x)", "-1/cos(x)")

        return text


# Example usage
your_instance = YourClass()
your_instance.answer()
