using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace ReadUIDemo.Tests
{
    /// <summary>
    /// Unit tests for the Calculator class
    /// </summary>
    [TestClass]
    public class CalculatorTest
    {
        private Calculator calculator;

        /// <summary>
        /// Initialize test setup - runs before each test
        /// </summary>
        [TestInitialize]
        public void Setup()
        {
            calculator = new Calculator();
        }

        /// <summary>
        /// Test the Add method with positive numbers
        /// </summary>
        [TestMethod]
        public void Add_PositiveNumbers_ReturnsCorrectSum()
        {
            // Arrange
            double a = 10.5;
            double b = 5.3;
            double expected = 15.8;

            // Act
            double result = calculator.Add(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Addition of positive numbers should return correct sum");
        }

        /// <summary>
        /// Test the Add method with negative numbers
        /// </summary>
        [TestMethod]
        public void Add_NegativeNumbers_ReturnsCorrectSum()
        {
            // Arrange
            double a = -10.5;
            double b = -5.3;
            double expected = -15.8;

            // Act
            double result = calculator.Add(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Addition of negative numbers should return correct sum");
        }

        /// <summary>
        /// Test the Subtract method with positive numbers
        /// </summary>
        [TestMethod]
        public void Subtract_PositiveNumbers_ReturnsCorrectDifference()
        {
            // Arrange
            double a = 10.5;
            double b = 5.3;
            double expected = 5.2;

            // Act
            double result = calculator.Subtract(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Subtraction should return correct difference");
        }

        /// <summary>
        /// Test the Subtract method resulting in negative number
        /// </summary>
        [TestMethod]
        public void Subtract_ResultingInNegative_ReturnsCorrectDifference()
        {
            // Arrange
            double a = 5.3;
            double b = 10.5;
            double expected = -5.2;

            // Act
            double result = calculator.Subtract(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Subtraction resulting in negative should return correct difference");
        }

        /// <summary>
        /// Test the Multiply method with positive numbers
        /// </summary>
        [TestMethod]
        public void Multiply_PositiveNumbers_ReturnsCorrectProduct()
        {
            // Arrange
            double a = 10.0;
            double b = 5.0;
            double expected = 50.0;

            // Act
            double result = calculator.Multiply(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Multiplication should return correct product");
        }

        /// <summary>
        /// Test the Multiply method with zero
        /// </summary>
        [TestMethod]
        public void Multiply_WithZero_ReturnsZero()
        {
            // Arrange
            double a = 10.5;
            double b = 0.0;
            double expected = 0.0;

            // Act
            double result = calculator.Multiply(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Multiplication with zero should return zero");
        }

        /// <summary>
        /// Test the Divide method with positive numbers
        /// </summary>
        [TestMethod]
        public void Divide_PositiveNumbers_ReturnsCorrectQuotient()
        {
            // Arrange
            double a = 10.0;
            double b = 5.0;
            double expected = 2.0;

            // Act
            double result = calculator.Divide(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Division should return correct quotient");
        }

        /// <summary>
        /// Test the Divide method with decimal result
        /// </summary>
        [TestMethod]
        public void Divide_DecimalResult_ReturnsCorrectQuotient()
        {
            // Arrange
            double a = 10.0;
            double b = 3.0;
            double expected = 3.333333333333333;

            // Act
            double result = calculator.Divide(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0001, "Division with decimal result should return correct quotient");
        }

        /// <summary>
        /// Test the Divide method throws exception when dividing by zero
        /// </summary>
        [TestMethod]
        [ExpectedException(typeof(DivideByZeroException))]
        public void Divide_ByZero_ThrowsDivideByZeroException()
        {
            // Arrange
            double a = 10.0;
            double b = 0.0;

            // Act & Assert
            calculator.Divide(a, b);
        }

        /// <summary>
        /// Test the Divide method throws exception with correct message when dividing by zero
        /// </summary>
        [TestMethod]
        public void Divide_ByZero_ThrowsExceptionWithCorrectMessage()
        {
            // Arrange
            double a = 10.0;
            double b = 0.0;

            // Act & Assert
            var exception = Assert.ThrowsException<DivideByZeroException>(() => calculator.Divide(a, b));
            Assert.AreEqual("Cannot divide by zero", exception.Message, "Exception message should match expected text");
        }

        /// <summary>
        /// Test edge case with very small numbers
        /// </summary>
        [TestMethod]
        public void Add_VerySmallNumbers_ReturnsCorrectSum()
        {
            // Arrange
            double a = 0.0001;
            double b = 0.0002;
            double expected = 0.0003;

            // Act
            double result = calculator.Add(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.0000001, "Addition of very small numbers should work correctly");
        }

        /// <summary>
        /// Test edge case with very large numbers
        /// </summary>
        [TestMethod]
        public void Multiply_VeryLargeNumbers_ReturnsCorrectProduct()
        {
            // Arrange
            double a = 1000000.0;
            double b = 1000000.0;
            double expected = 1000000000000.0;

            // Act
            double result = calculator.Multiply(a, b);

            // Assert
            Assert.AreEqual(expected, result, 0.1, "Multiplication of very large numbers should work correctly");
        }
    }
}
