import pytrends
from pytrends.request import TrendReq
import pandas as pd

import ast

# Open the file in read mode
file_path = 'example.txt'

with open(file_path, 'r') as file:

    file_content = file.read()

    try:
        my_list = ast.literal_eval(file_content)
        print("List from the file:", my_list)
    except (SyntaxError, ValueError) as e:
        print(f"Error reading the file: {e}")
In this example, ast.literal_eval() is used instead of eval() to safely evaluate the file's content. eval() can execute arbitrary code and is generally not recommended for evaluating untrusted input, as it could pose a security risk.

Make sure to handle any exceptions that may occur during the file reading and evaluation process, as shown in the example. This way, your program can gracefully handle cases where the file content is not a valid Python list.





