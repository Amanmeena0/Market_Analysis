from crew import run_crew

if __name__ == "__main__":
    company = input("Enter the company ticker (e.g., AAPL, TCS.NS): ")
    report = run_crew(company)
    print("\n--- Final Report ---\n")
    print(report)
