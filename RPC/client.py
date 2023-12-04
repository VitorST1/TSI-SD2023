# client.py

from rpc.client import Client
from tkinter import *
# import time

HOST = 'localhost'
PORT = 5000

client = Client(HOST, PORT)


def handle_result_two_inputs(result, input1, input2, input_window):
    print("Result:", result)
    if 'result_label' in input_window.__dict__:
        result_label = input_window.result_label
        result_label.config(text=f"Result: {result}")
    else:
        result_label = Label(input_window, text=f"Result: {result}")
        result_label.pack()
    input_window.result_label = result_label
    input1.delete(0, END)  # Clear the first input field
    input2.delete(0, END)  # Clear the second input field


def handle_result_one_input(result, input, input_window):
    print("Result:", result)
    if 'result_label' in input_window.__dict__:
        result_label = input_window.result_label
        result_label.config(text=f"Result: {result}")
    else:
        result_label = Label(input_window, text=f"Result: {result}")
        result_label.pack()
    input_window.result_label = result_label
    input.delete(0, END)  # Clear the first input field


def handle_result_last_news_input(result, input, input_window):
    print("Result:", result)
    for title in result:
        print(title)
        result_label = Label(input_window, text=title)
        result_label.pack()
    input.delete(0, END)  # Clear the first input field


def sum_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter first number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Label(input_window, text="Enter second number:").pack()
    input2 = Entry(input_window)
    input2.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_sun_function(input1, input2, input_window)).pack()


def submit_sun_function(input1, input2, input_window):
    result = client.sum(input1.get(), input2.get())
    handle_result_two_inputs(result, input1, input2, input_window)


def subtraction_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter first number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Label(input_window, text="Enter second number:").pack()
    input2 = Entry(input_window)
    input2.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_sub_function(input1, input2, input_window)).pack()


def submit_sub_function(input1, input2, input_window):
    result = client.sub(input1.get(), input2.get())
    handle_result_two_inputs(result, input1, input2, input_window)


def division_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter first number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Label(input_window, text="Enter second number:").pack()
    input2 = Entry(input_window)
    input2.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_div_function(input1, input2, input_window)).pack()


def submit_div_function(input1, input2, input_window):
    result = client.div(input1.get(), input2.get())
    handle_result_two_inputs(result, input1, input2, input_window)


def multiplication_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter first number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Label(input_window, text="Enter second number:").pack()
    input2 = Entry(input_window)
    input2.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_mul_function(input1, input2, input_window)).pack()


def submit_mul_function(input1, input2, input_window):
    result = client.mul(input1.get(), input2.get())
    handle_result_two_inputs(result, input1, input2, input_window)


def is_prime_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_is_prime_function(input1, input_window)).pack()


def submit_is_prime_function(input1, input_window):
    result = client.is_prime(input1.get())
    handle_result_one_input(result, input1, input_window)


def last_news_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("1000x720")
    Label(input_window, text="Enter number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_last_news_function(input1, input_window)).pack()


def submit_last_news_function(input1, input_window):
    result = client.last_news_if_barbacena(input1.get())
    handle_result_last_news_input(result, input1, input_window)


def prime_in_range_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("500x150")
    Label(input_window, text="Enter first number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Label(input_window, text="Enter second number:").pack()
    input2 = Entry(input_window)
    input2.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_prime_in_range_function(input1, input2, input_window)).pack()


def submit_prime_in_range_function(input1, input2, input_window):
    result = client.show_prime_in_range_multiprocessing(
        input1.get(), input2.get())
    handle_result_two_inputs(result, input1, input2, input_window)


def cpf_validate_function():
    input_window = Toplevel(window)
    input_window.title('Input')
    input_window.geometry("250x150")
    Label(input_window, text="Enter number:").pack()
    input1 = Entry(input_window)
    input1.pack()
    Button(input_window, text="Submit",
           command=lambda: submit_cpf_function(input1, input_window)).pack()


def submit_cpf_function(input1, input_window):
    result = client.valida_CPF(input1.get())
    if result == True:
        result = "Valid"
    elif result == False:
        result = "Invalid"
    handle_result_one_input(result, input1, input_window)


window = Tk()
window.title('RPC Client')
window.geometry("215x164+10+20")

sum_button = Button(window, text="Sum",
                    command=sum_function, width=14, height=2)
subtraction_button = Button(
    window, text="Subtraction", command=subtraction_function, width=14, height=2)
division_button = Button(window, text="Division",
                         command=division_function, width=14, height=2)
multiplication_button = Button(
    window, text="Multiplication", command=multiplication_function, width=14, height=2)
is_prime_button = Button(window, text="Is Prime",
                         command=is_prime_function, width=14, height=2)
last_news_button = Button(window, text="Last News",
                          command=last_news_function, width=14, height=2)
prime_in_range_button = Button(
    window, text="Prime In Range", command=prime_in_range_function, width=14, height=2)
cpf_validate_button = Button(
    window, text="CPF Validate", command=cpf_validate_function, width=14, height=2)

sum_button.grid(row=0, column=0)
subtraction_button.grid(row=0, column=1)
division_button.grid(row=1, column=0)
multiplication_button.grid(row=1, column=1)
is_prime_button.grid(row=2, column=0)
last_news_button.grid(row=2, column=1)
prime_in_range_button.grid(row=3, column=0)
cpf_validate_button.grid(row=3, column=1)

window.mainloop()

client.close()
