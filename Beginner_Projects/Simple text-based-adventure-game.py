def main():
    print("\nWelcome to the Simple Text-Based Adventure Game!")

    while True:
        print("\nYou are at a crossroad. You can go left or right.")
        choice = input("Enter your choice (left/right): ").lower()

        if choice == "left":
            print("You encounter a friendly talking cat. It leads you to a hidden cave.")
            print("The cat offers to guide you to the treasure if you can solve a riddle.")
            
            riddle = {
                "question": "What has a face and two hands, but no arms or legs?",
                "options": ["A clock", "A man", "A table", "A book"],
                "correct_answer": "A clock"
            }   
            
            print(f"\nRiddle: {riddle['question']}")
            for i, option in enumerate(riddle['options'], start=1):
                print(f"{i}. {option}")

            user_answer = input("Enter the number of your answer: ").lower()    

            if user_answer == riddle['correct_answer'].lower():
                print("Congratulations! You solved the riddle. The cat leads you to the treasure.")
                break
            else:
                print("That's not the correct answer. Try again!")      
                
        elif choice == "right":
            print("You stumble into a dark forest. You hear a rustling in the bushes.")
            print("You see a path leading deeper into the forest.")
            
            while True:
                print("\nYou can either follow the path or turn back.")
                choice = input("Enter your choice (follow/back): ").lower()

                if choice == "follow":
                    print("You follow the path deeper into the forest.")
                    break
                elif choice == "back":
                    print("You decide to turn back. You head back to the crossroad.")
                    break
                else:
                    print("Invalid choice. Please enter 'follow' or 'back'.")
                    
        else:
            print("Invalid choice. Please enter 'left' or 'right'.")

if __name__ == "__main__":
    main()
