def is_even(num):
    return num % 2 == 0

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def factorial(num):
    fact = 1
    for i in range(1, num + 1):
        fact *= i
    return fact

def fibonacci(n):
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

def sum_of_digits(num):
    return sum(int(d) for d in str(num))

# Main program
num = int(input("Enter a number: "))

print("Even/Odd:", "Even" if is_even(num) else "Odd")
print("Prime:", "Yes" if is_prime(num) else "No")
print("Factorial:", factorial(num))
print("Fibonacci Series:", fibonacci(num))
print("Sum of digits:", sum_of_digits(num))
