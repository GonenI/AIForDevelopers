using System;

namespace ReadUIDemo
{
    /// <summary>
    /// Simple calculator class for basic arithmetic operations
    /// </summary>
    public class Calculator
    {
        /// <summary>
        /// Adds two double values
        /// </summary>
        /// <param name="a">First number</param>
        /// <param name="b">Second number</param>
        /// <returns>Sum of a and b</returns>
        public double Add(double a, double b)
        {
            return a + b;
        }

        /// <summary>
        /// Subtracts the second double value from the first
        /// </summary>
        /// <param name="a">First number</param>
        /// <param name="b">Second number</param>
        /// <returns>Difference of a and b</returns>
        public double Subtract(double a, double b)
        {
            return a - b;
        }

        /// <summary>
        /// Multiplies two double values
        /// </summary>
        /// <param name="a">First number</param>
        /// <param name="b">Second number</param>
        /// <returns>Product of a and b</returns>
        public double Multiply(double a, double b)
        {
            return a * b;
        }

        /// <summary>
        /// Divides the first double value by the second
        /// </summary>
        /// <param name="a">Dividend</param>
        /// <param name="b">Divisor</param>
        /// <returns>Quotient of a and b</returns>
        /// <exception cref="DivideByZeroException">Thrown when divisor is zero</exception>
        public double Divide(double a, double b)
        {
            if (b == 0)
            {
                throw new DivideByZeroException("Cannot divide by zero");
            }
            return a / b;
        }

 

        /// <summary>
        /// Demonstrates the calculator functionality
        /// </summary>
        public void Demo()
        {
            Console.WriteLine("Calculator Demo:");
            Console.WriteLine($"Add: 10.5 + 5.3 = {Add(10.5, 5.3)}");
            Console.WriteLine($"Subtract: 10.5 - 5.3 = {Subtract(10.5, 5.3)}");
            Console.WriteLine($"Multiply: 10.5 * 5.3 = {Multiply(10.5, 5.3)}");
            Console.WriteLine($"Divide: 10.5 / 5.3 = {Divide(10.5, 5.3)}");
        }
    }
}
