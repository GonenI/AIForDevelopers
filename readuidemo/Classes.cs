using System;

namespace ReadUIDemo
{
    /// <summary>
    /// Interface IA
    /// </summary>
    public interface IA
    {
        // Interface method declaration
        void Method();
    }

    /// <summary>
    /// Class A implements interface IA
    /// </summary>
    public class A : IA
    {
        // Class A specific properties and methods
        public void Method()
        {
            Console.WriteLine("A Method");
        }

        public virtual void ASpecificMethod()
        {
            Console.WriteLine("A Specific Method");
        }
    }

    /// <summary>
    /// Class B inherits from class A
    /// </summary>
    public class B : A
    {
        // Class B specific properties and methods
        public override void Method()
        {
            Console.WriteLine("B Method");
        }

        public void BSpecificMethod()
        {
            Console.WriteLine("B Specific Method");
        }
    }

    /// <summary>
    /// Class C inherits from class A
    /// </summary>
    public class C : A
    {
        // Class C specific properties and methods
        public override void Method()
        {
            Console.WriteLine("C Method");
        }

        public void CSpecificMethod()
        {
            Console.WriteLine("C Specific Method");
        }
    }
}
