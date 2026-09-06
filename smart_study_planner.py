# ================================================================
# INDIVIDUAL ASSIGNMENT
# PROJECT TITLE: THE SMART STUDY PLANNER
# ================================================================
#
# Student Name: ODONGO EMMANUEL LUMUMBA
# Course: Bachelor of Science in Information Technology
# Assignment: Individual Assignment – The Smart Study Planner
# Programming Language: Python
# Storage File: study_log.txt
#
# ================================================================
# PROJECT DESIGN
# ================================================================
#
# The Smart Study Planner is a console-based Python program
# designed to help a student record, view, search and analyse
# study sessions throughout a semester.
#
# The program uses a modular design. Each function performs
# a specific task, making the program easy to understand,
# test and maintain.
#
# Study sessions are stored as dictionaries inside a list.
# JSON is used to save the list of dictionaries into
# study_log.txt.
#
# When the program starts, previously saved sessions are
# automatically loaded from study_log.txt.
#
# When the user selects "Save and exit", all study sessions
# are saved to study_log.txt.
#
# The storage file is created in the same folder as this
# Python program.
#
# ================================================================


import json
import os


# ================================================================
# FILE LOCATION
# ================================================================

# Find the folder where this Python program is stored
PROGRAM_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Store study_log.txt in the same folder as the Python program
FILE_NAME = os.path.join(PROGRAM_FOLDER, "study_log.txt")


# ================================================================
# Function: classify_session()
# Purpose: Classifies a study session according to its duration.
# ================================================================

def classify_session(duration):
    """
    Classifies a study session according to its duration.

    Under 30 minutes = Short
    30 to 90 minutes = Medium
    Over 90 minutes = Long
    """

    if duration < 30:
        return "Short"

    elif duration <= 90:
        return "Medium"

    else:
        return "Long"


# ================================================================
# Function: get_valid_duration()
# Purpose: Gets a valid positive study duration from the user.
# ================================================================

def get_valid_duration():
    """
    Gets a valid positive study duration from the user.

    The function keeps asking until the user enters
    a positive number.
    """

    while True:

        try:
            duration = float(
                input("Enter duration in minutes: ").strip()
            )

            if duration > 0:
                return duration

            print("Duration must be a positive number.")

        except ValueError:
            print("Invalid input. Please enter a number.")


# ================================================================
# Function: add_session()
# Purpose: Adds a new study session to the sessions list.
# ================================================================

def add_session(sessions):
    """
    Prompts the user for study session details and adds
    the new session to the sessions list.
    """

    print("\n" + "-" * 60)
    print("ADD STUDY SESSION")
    print("-" * 60)

    # Ask the user for study session information
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day label: ").strip()

    # Ask for a valid positive duration
    duration = get_valid_duration()

    # Store the study session as a dictionary
    new_session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    # Add the new session to the list
    sessions.append(new_session)

    print("\nStudy session added successfully!")


# ================================================================
# Function: view_sessions()
# Purpose: Displays all recorded study sessions.
# ================================================================

def view_sessions(sessions):
    """
    Displays every recorded study session in a
    neatly formatted table.
    """

    print("\n" + "-" * 90)
    print("ALL STUDY SESSIONS")
    print("-" * 90)

    # Check whether there are any sessions
    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    # Display table headings
    print(
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Minutes':<12}"
        f"{'Class':<10}"
    )

    print("-" * 90)

    # Display each recorded session
    for session in sessions:

        # Classify the session using classify_session()
        session_class = classify_session(
            session["duration"]
        )

        print(
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12.1f}"
            f"{session_class:<10}"
        )

    print("-" * 90)


# ================================================================
# Function: search_by_subject()
# Purpose: Searches for sessions by subject.
# ================================================================

def search_by_subject(sessions):
    """
    Searches for study sessions by subject.

    The search is case-insensitive, so Python, python
    and PYTHON are treated as the same subject.
    """

    print("\n" + "-" * 75)
    print("SEARCH SESSIONS BY SUBJECT")
    print("-" * 75)

    subject_to_find = input(
        "Enter subject name to search: "
    ).strip()

    matching_sessions = []

    # Search through all recorded sessions
    for session in sessions:

        # Convert both values to lowercase for case-insensitive search
        if session["subject"].lower() == subject_to_find.lower():
            matching_sessions.append(session)

    # Display a clear message if no sessions are found
    if not matching_sessions:

        print(
            f"\nNo study sessions found for "
            f"'{subject_to_find}'."
        )

        return

    # Calculate the total time spent on the subject
    total_minutes = sum(
        session["duration"]
        for session in matching_sessions
    )

    print(f"\nSessions recorded for: {subject_to_find}")

    print("-" * 75)

    # Display table headings
    print(
        f"{'Topic':<30}"
        f"{'Date':<15}"
        f"{'Minutes':<12}"
        f"{'Class':<10}"
    )

    print("-" * 75)

    # Display matching sessions
    for session in matching_sessions:

        # Reuse classify_session() when displaying sessions
        session_class = classify_session(
            session["duration"]
        )

        print(
            f"{session['topic']:<30}"
            f"{session['date']:<15}"
            f"{session['duration']:<12.1f}"
            f"{session_class:<10}"
        )

    print("-" * 75)

    # Display total time spent on the selected subject
    print(
        f"Total time spent on {subject_to_find}: "
        f"{total_minutes:.1f} minutes"
    )

    print(
        f"Total time in hours: "
        f"{total_minutes / 60:.2f} hours"
    )


# ================================================================
# Function: calculate_subject_totals()
# Purpose: Calculates total study time for every subject.
# ================================================================

def calculate_subject_totals(sessions):
    """
    Calculates the total study time for each subject.

    Returns a dictionary containing each subject and
    its total study time in minutes.
    """

    subject_totals = {}

    # Go through every study session
    for session in sessions:

        subject = session["subject"]
        duration = session["duration"]

        # Add the duration to the subject's total
        if subject in subject_totals:

            subject_totals[subject] += duration

        else:

            subject_totals[subject] = duration

    return subject_totals


# ================================================================
# Function: study_statistics()
# Purpose: Calculates and displays study statistics.
# ================================================================

def study_statistics(sessions):
    """
    Calculates and displays:

    1. Total hours studied overall.
    2. Total hours studied per subject.
    3. Subject with the least study time.
    4. Single longest study session.
    """

    print("\n" + "-" * 60)
    print("STUDY STATISTICS")
    print("-" * 60)

    # Check whether there are sessions to analyse
    if not sessions:

        print(
            "No study sessions available for statistics."
        )

        return

    # Calculate total study time
    total_minutes = sum(
        session["duration"]
        for session in sessions
    )

    total_hours = total_minutes / 60

    print(
        f"\nTotal hours studied overall: "
        f"{total_hours:.2f} hours"
    )

    # Calculate total study time for each subject
    subject_totals = calculate_subject_totals(sessions)

    print("\nTotal study time per subject:")

    for subject, minutes in subject_totals.items():

        print(
            f"- {subject}: "
            f"{minutes:.1f} minutes "
            f"({minutes / 60:.2f} hours)"
        )

    # Find the subject with the least study time
    weakest_subject = min(
        subject_totals,
        key=subject_totals.get
    )

    print("\nSubject with the least study time:")
    print(weakest_subject)

    print(
        f"Time studied: "
        f"{subject_totals[weakest_subject]:.1f} minutes"
    )

    # Find the longest individual study session
    longest_session = max(
        sessions,
        key=lambda session: session["duration"]
    )

    print("\nLongest study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Date: {longest_session['date']}")
    print(
        f"Duration: "
        f"{longest_session['duration']:.1f} minutes"
    )

    # Classify the longest study session
    print(
        f"Classification: "
        f"{classify_session(longest_session['duration'])}"
    )


# ================================================================
# Function: save_sessions()
# Purpose: Saves all study sessions to study_log.txt.
# ================================================================

def save_sessions(sessions):
    """
    Saves all study sessions to study_log.txt.

    JSON format is used to store the list of dictionaries.
    """

    try:

        # Open the file in write mode.
        # If it does not exist, Python creates it.
        with open(
            FILE_NAME,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                sessions,
                file,
                indent=4
            )

        print("\nStudy sessions saved successfully!")

        # Show the exact location of the saved file
        print(f"File saved at: {FILE_NAME}")

    except IOError as error:

        print("\nError: Unable to save study sessions.")
        print(f"Error details: {error}")


# ================================================================
# Function: load_sessions()
# Purpose: Loads previously saved sessions from study_log.txt.
# ================================================================

def load_sessions():
    """
    Loads previously saved study sessions from study_log.txt.

    If the file does not exist, an empty list is returned.
    """

    # Check whether study_log.txt exists
    if not os.path.exists(FILE_NAME):

        print("\nNo previous study sessions found.")

        return []

    try:

        # Open the existing file and read its contents
        with open(
            FILE_NAME,
            "r",
            encoding="utf-8"
        ) as file:

            sessions = json.load(file)

        # Make sure the loaded information is a list
        if isinstance(sessions, list):

            print(
                f"\nPrevious study sessions loaded "
                f"from '{FILE_NAME}'."
            )

            return sessions

        print("Invalid data found in study_log.txt.")

        return []

    except (IOError, json.JSONDecodeError) as error:

        print("\nCould not load existing study data.")
        print(f"Error details: {error}")

        return []


# ================================================================
# Function: display_menu()
# Purpose: Displays the main program menu.
# ================================================================

def display_menu():
    """
    Displays the main menu of the Smart Study Planner.
    """

    print("\n" + "=" * 60)
    print("              SMART STUDY PLANNER")
    print("=" * 60)
    print("                 MAIN MENU")
    print("=" * 60)

    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")

    print("=" * 60)


# ================================================================
# Function: main()
# Purpose: Controls the main operation of the program.
# ================================================================

def main():
    """
    Controls the overall operation of the Smart Study Planner.
    """

    # Load any previously saved sessions when the program starts
    sessions = load_sessions()

    print("\n" + "=" * 60)
    print("         WELCOME TO THE SMART STUDY PLANNER")
    print("=" * 60)

    # Continue displaying the menu until the user exits
    while True:

        # Display the main menu
        display_menu()

        # Ask the user to select a menu option
        choice = input(
            "Enter your choice (1-5): "
        ).strip()

        # Option 1: Add a new study session
        if choice == "1":

            add_session(sessions)

        # Option 2: View all recorded sessions
        elif choice == "2":

            view_sessions(sessions)

        # Option 3: Search for sessions by subject
        elif choice == "3":

            search_by_subject(sessions)

        # Option 4: View study statistics
        elif choice == "4":

            study_statistics(sessions)

        # Option 5: Save all data and exit
        elif choice == "5":

            save_sessions(sessions)

            print(
                "\nThank you for using "
                "the Smart Study Planner."
            )

            print("Goodbye!")

            break

        # Handle invalid menu choices
        else:

            print(
                "\nInvalid choice."
                "\nPlease select a number from 1 to 5."
            )


# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

if __name__ == "__main__":
    main()