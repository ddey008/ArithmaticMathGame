import sympy as sp
import matplotlib.pyplot as plt
import PIL as pil
from PIL import ImageTk, Image
from sympy import symbols

# Define symbols
x = symbols('x')

def create_question_image():
    # LaTeX equation for the image
    expression = x**3
    expr_latex = "$" + sp.latex(expression) + "$"

    # Create Matplotlib figure
    fig, ax = plt.subplots(figsize=(2, 2))  # Adjust figsize as needed
    ax.text(0.5, 0.5, expr_latex, fontsize=20, ha='center', va='center')
    ax.axis('off')

    # Save figure
    fig.savefig("temp.png", bbox_inches='tight', pad_inches=0, transparent=True)

    # Open and process the image
    image1 = pil.Image.open("temp.png")
    question_image = pil.ImageTk.PhotoImage(image1)  # Assuming you have ImageTk imported

    return question_image

# Ex

