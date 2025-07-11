from src.cli import Application

if __name__ == "__main__":
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("The application will now exit.")