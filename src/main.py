import sys
from check_requirements import main as check_requirements




def main():
    # First check and install requirements
    check_requirements()
    
    # Your main program logic goes here
    print("Requirements checked and installed. Ready to proceed.")

if __name__ == "__main__":
    main()
