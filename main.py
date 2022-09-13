"""
Straightforward-Calculator
description: This calculator simulates the calculator found in MacOS using tkinter
author: Pedro Torres
version: 0.1
"""
import tkinter as tk
from collections import deque
from tkmacosx import Button


# Calculator class will handle all the functions of the calculator
class Calculator:
    def __init__(self):
        self.display_number = tk.StringVar(root, '0')
        self.clear_button = tk.StringVar(root, 'AC')
        self.numbers = deque(maxlen=3)
        self.total = 0
        self.current_number = ''
        self.operation = ''
        self.second_operation = ''
        self.last_operation = ''
        self.last_number = ''
        self.equal_pressed = False
        self.operation_pressed = False
        self.decimal = False
        self.continued_total = False
        self.clear_state = True

    # Clears the calculator (current entity or all memory) with either 'C' or 'AC'
    def clear(self):
        self.current_number = '0'
        self.update_output()
        self.clear_button.set('AC')
        self.operation_pressed = False
        if self.clear_state:
            self.numbers.clear()
            self.equal_pressed = False
            self.decimal = False
            self.continued_total = False
            self.operation = ''
            self.second_operation = ''
            self.last_operation = ''
            self.last_number = ''
        else:
            self.clear_state = True

    # Changes between 'C' and 'AC'
    def set_clear(self):
        self.clear_state = False
        self.clear_button.set('C')

    # Changes the sign of the current number to the opposite sign
    def change_sign(self):
        self.current_number = str(-float(self.current_number))
        self.update_output()

    # Converts the current percent(current number) into a decimal
    def percent_conversion(self):
        self.current_number = str(float(self.current_number) / 100)
        self.update_output()

    # Updates the calculator output/screen
    def update_output(self):
        temp_number = float(self.current_number)
        # Removes any unnecessary decimals or zeros
        if self.decimal:
            self.display_number.set(('%f' % temp_number).rstrip('0'))
        else:
            self.display_number.set(('%f' % temp_number).rstrip('0').rstrip('.'))

    # Handles all presses of the number buttons
    def number_button(self, number):
        # adds previous number to the stack
        if self.operation_pressed:
            self.new_number()
        if self.current_number == '0' or self.equal_pressed:
            self.current_number = ''
        # Checks for duplicate decimals
        if number == '.':
            self.decimal = True
            if self.current_number.count('.') > 0:
                number = ''
        # Resets needed parameters to continue function
        self.current_number += number
        self.update_output()
        self.set_clear()
        self.operation_pressed = False
        self.equal_pressed = False
        self.decimal = False

    # Adds current_number to the stack
    def new_number(self):
        # Allows for calculations that are continuing operations
        if self.continued_total:
            self.numbers.pop()
            self.continued_total = False
        # Appends to stack
        if len(self.current_number) > 0:
            self.numbers.append(float(self.current_number))
            self.current_number = ''

    # Gets total of previous operation and adds to stack
    def get_total(self):
        if self.equal_pressed:
            self.numbers.append(self.total)
            self.continued_total = True
        self.equal_pressed = False

    # The four following methods are for the four operations
    def add(self):
        self.operation_pressed = True
        self.operation = 'add'
        self.get_total()

    def subtract(self):
        self.operation_pressed = True
        self.operation = 'subtract'
        self.get_total()

    # Both divide and multiply have statements to check for order of operations for 3 number equations
    def multiply(self):
        if self.operation == 'add' or self.operation == 'subtract':
            self.second_operation = 'multiply'
        else:
            self.operation = 'multiply'
        self.operation_pressed = True
        self.get_total()

    def divide(self):
        if self.operation == 'add' or self.operation == 'subtract':
            self.second_operation = 'divide'
        else:
            self.operation = 'divide'
        self.operation_pressed = True
        self.get_total()

    # Calculates two or three number equations
    def equal(self):
        # Variables for continuing operations
        operation = self.operation
        second_operation = self.second_operation
        last_operation_true = False

        # Handles multiplication or division in a 3 number equation
        try:
            if second_operation == 'multiply' or second_operation == 'divide':
                third_num = self.numbers.pop()
                second_num = self.numbers.pop()
                if second_operation == 'multiply':
                    self.numbers.append(second_num * third_num)
                else:
                    self.numbers.append(second_num / third_num)
                self.last_operation = second_operation
                self.last_number = third_num
            else:
                self.last_operation = operation
                last_operation_true = True

            first_number = self.numbers.pop()
            second_number = self.numbers.pop()

            if last_operation_true:
                self.last_number = first_number

            # Handles normal operand calculations
            if operation == 'add':
                return first_number + second_number
            elif operation == 'subtract':
                return second_number - first_number
            elif operation == 'multiply':
                return first_number * second_number
            elif operation == 'divide':
                return second_number / first_number

        # Handles division by 0
        except ZeroDivisionError:
            self.display_number.set('ERROR')

    # Method when equal button is pressed
    def equal_button(self):
        try:
            self.equal_pressed = True
            self.new_number()
            length = len(self.numbers)

            # For cases when used only inputs 1 number and 1 operand
            if self.operation_pressed:
                self.last_number = self.numbers.pop()
                self.numbers.append(self.last_number)
                self.last_operation = self.operation

            # Handles normal calculations
            if length >= 2:
                self.current_number = str(self.equal())
                self.total = float(self.current_number)
            else:
                self.numbers.append(self.last_number)
                self.operation = self.last_operation
                self.current_number = str(self.equal())
                self.total = float(self.current_number)
            self.operation_pressed = False
            self.update_output()
            self.second_operation = ''
            self.operation = ''

        # Handles if there are no numbers in the stack
        except IndexError:
            pass


# Creates the root and gives program a title
root = tk.Tk()
root.resizable(width=False, height=False)
root.title('Calculator')

active_calculator = Calculator()

mainFrame = tk.Frame(root)
mainFrame.grid(row=0, column=0, sticky='NSEW')

# Sets the design elements for the calculator
display_font = ('Helvetica', 30)
calc_font = ('Helvetica', 20)

white = '#FFFFFF'
orange = '#FF9E0B'
light_grey = '#5D5C5C'
dark_grey = '#3D3B3C'
darker_grey = '#282627'

active_numpad = '#9F9F9F'
active_top = '#5D5C5C'
active_operands = '#CB7D04'

# Creates the output label and attaches to grid
calculator_output = tk.Label(mainFrame, text='0', textvariable=active_calculator.display_number, anchor=tk.E,
                             bg=darker_grey, fg=white, padx=24, font=display_font)
calculator_output.grid(row=0, columnspan=4, sticky='NSEW')

# Creates the buttons for the calculator
clear_button = Button(mainFrame, textvariable=active_calculator.clear_button, bg=dark_grey, fg=white,
                      activebackground=active_top,
                      font=calc_font, bordercolor=darker_grey, bd=0, width=60, height=50,
                      command=lambda: active_calculator.clear())
sign_change = Button(mainFrame, text='+/-', bg=dark_grey, fg=white, activebackground=active_top, font=calc_font,
                     bordercolor=darker_grey,
                     bd=0, width=60, height=50, command=lambda: active_calculator.change_sign())
percent_button = Button(mainFrame, text='%', bg=dark_grey, fg=white, activebackground=active_top, font=calc_font,
                        bordercolor=darker_grey, bd=0, width=60, height=50,
                        command=lambda: active_calculator.percent_conversion())
divide = Button(mainFrame, text='\u00F7', bg=orange, fg=white, activebackground=active_operands, font=calc_font,
                bordercolor=darker_grey, bd=0, width=60, height=50,
                command=lambda: active_calculator.divide())
seven = Button(mainFrame, text='7', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
               bordercolor=darker_grey, bd=0, width=60, height=50,
               command=lambda: active_calculator.number_button('7'))
eight = Button(mainFrame, text='8', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
               bordercolor=darker_grey, bd=0, width=60, height=50,
               command=lambda: active_calculator.number_button('8'))
nine = Button(mainFrame, text='9', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
              bordercolor=darker_grey, bd=0, width=60, height=50,
              command=lambda: active_calculator.number_button('9'))
times = Button(mainFrame, text='x', bg=orange, fg=white, activebackground=active_operands, font=calc_font,
               bordercolor=darker_grey, bd=0, width=60, height=50,
               command=lambda: active_calculator.multiply())
four = Button(mainFrame, text='4', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
              bordercolor=darker_grey, bd=0, width=60, height=50,
              command=lambda: active_calculator.number_button('4'))
five = Button(mainFrame, text='5', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
              bordercolor=darker_grey, bd=0, width=60, height=50,
              command=lambda: active_calculator.number_button('5'))
six = Button(mainFrame, text='6', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
             bordercolor=darker_grey, bd=0, width=60, height=50,
             command=lambda: active_calculator.number_button('6'))
minus = Button(mainFrame, text='-', bg=orange, fg=white, activebackground=active_operands, font=calc_font,
               bordercolor=darker_grey, bd=0, width=60, height=50,
               command=lambda: active_calculator.subtract())
one = Button(mainFrame, text='1', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
             bordercolor=darker_grey, bd=0, width=60, height=50,
             command=lambda: active_calculator.number_button('1'))
two = Button(mainFrame, text='2', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
             bordercolor=darker_grey, bd=0, width=60, height=50,
             command=lambda: active_calculator.number_button('2'))
three = Button(mainFrame, text='3', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
               bordercolor=darker_grey, bd=0, width=60, height=50,
               command=lambda: active_calculator.number_button('3'))
plus = Button(mainFrame, text='+', bg=orange, fg=white, activebackground=active_operands, font=calc_font,
              bordercolor=darker_grey, bd=0, width=60, height=50,
              command=lambda: active_calculator.add())
zero = Button(mainFrame, text='0', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
              bordercolor=darker_grey, bd=0, width=60, height=50,
              command=lambda: active_calculator.number_button('0'))
decimal = Button(mainFrame, text='.', bg=light_grey, fg=white, activebackground=active_numpad, font=calc_font,
                 bordercolor=darker_grey, bd=0, width=60, height=50,
                 command=lambda: active_calculator.number_button('.'))
equals = Button(mainFrame, text='=', bg=orange, fg=white, activebackground=active_operands, font=calc_font,
                bordercolor=darker_grey, bd=0, width=60, height=50,
                command=lambda: active_calculator.equal_button())

# Attaches all the created button to the grid
clear_button.grid(row=1, column=0, sticky='NSEW')
sign_change.grid(row=1, column=1, sticky='NSEW')
percent_button.grid(row=1, column=2, sticky='NSEW')
divide.grid(row=1, column=3, sticky='NSEW')
seven.grid(row=2, column=0, sticky='NSEW')
eight.grid(row=2, column=1, sticky='NSEW')
nine.grid(row=2, column=2, sticky='NSEW')
times.grid(row=2, column=3, sticky='NSEW')
four.grid(row=3, column=0, sticky='NSEW')
five.grid(row=3, column=1, sticky='NSEW')
six.grid(row=3, column=2, sticky='NSEW')
minus.grid(row=3, column=3, sticky='NSEW')
one.grid(row=4, column=0, sticky='NSEW')
two.grid(row=4, column=1, sticky='NSEW')
three.grid(row=4, column=2, sticky='NSEW')
plus.grid(row=4, column=3, sticky='NSEW')
zero.grid(row=5, columnspan=2, sticky='NSEW')
decimal.grid(row=5, column=2, sticky='NSEW')
equals.grid(row=5, column=3, sticky='NSEW')

root.mainloop()
