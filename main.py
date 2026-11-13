from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_title("Workout Tracker")

set_site_information(
    author="Aiden Hearn",
    description="Track workouts, record exercises, and monitor your fitness progress.",
    planning = [],
    sources="Thanks to the Drafter documentation and my CISC-108 course materials.",
    links=["https://aiden-h13.github.io/workout-tracker/"]
)

hide_debug_information()
set_website_framed(False)

@dataclass
class Workout:
    id: int
    date: str
    category: str
    exercises: str
    notes: str


@dataclass
class State:
    username: str
    fitness_goal: str
    workouts: list[Workout]
    next_workout_id: int


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Workout Tracker"),
        "Welcome to your workout tracker!",
        "What would you like to do?",
        Button("Add a workout", "add_workout"),
        Button("View workout history", "workout_history"),
        Button("View progress", "progress"),
        Button("Settings", "settings")
    ])


@route
def add_workout(state: State) -> Page:
    return Page(state, [
        Header("Add a Workout"),
        "Enter the details of your workout:",
        
        "Date:",
        TextBox("date", ""),
        
        "Category:",
        SelectBox("category", [
            "Chest",
            "Back",
            "Shoulders",
            "Arms",
            "Legs",
            "Cardio",
            "Other"
        ], "Chest"),
        
        "Exercises:",
        TextArea("exercises", ""),
        "Notes:",
        TextArea("notes", ""),

        Button("Save Workout", "save_workout"),
            
        Button("Home", "index")
    ])


@route
def workout_history(state: State) -> Page:
    content = [
        Header("Workout History"),
        "Here are your previous workouts:"
    ]

    if not state.workouts:
        content.append("You haven't saved any workouts yet.")

    else:
        for workout in state.workouts:
            content.append(HorizontalRule())
            content.append(Header(workout.category, 2))
            content.append("Date: " + workout.date)
            content.append("Exercises: " + workout.exercises)
            content.append("Notes: " + workout.notes)

    content.append(HorizontalRule())
    content.append(Button("Home", "index"))

    return Page(state, content)

@route
def save_workout(
    state: State,
    date: str,
    category: str,
    exercises: str,
    notes: str
) -> Page:

    new_workout = Workout(
        state.next_workout_id,
        date,
        category,
        exercises,
        notes
    )

    state.workouts.append(new_workout)
    state.next_workout_id += 1

    return Page(state, [
        Header("Workout Saved!"),
        "Your workout has been successfully saved!",
        Button("Home", "index"),
        Button("Add Another Workout", "add_workout")
    ])


@route
def settings(state: State) -> Page:
    return Page(state, [
        Header("Settings"),
        "Update your information below:",

        "Username:",
        TextBox("username", state.username),

        "Fitness Goal:",
        SelectBox("fitness_goal", [
            "Build muscle",
            "Improve endurance",
            "Increase strength",
            "Improve flexibility",
            "Stay active"
        ], state.fitness_goal),

        Button("Save Settings", "save_settings"),
        Button("Home", "index")
    ])

@route
def save_settings(state: State, username: str, fitness_goal: str) -> Page:

    if not username.strip() or not fitness_goal.strip():
        return Page(state, [
            Header("Missing Information"),
            "Please enter both a username and fitness goal.",
            Button("Back to Settings", "settings")
        ])

    state.username = username
    state.fitness_goal = fitness_goal

    return Page(state, [
        Header("Settings Saved!"),
        "Your information has been updated.",
        "Username: " + state.username,
        "Fitness Goal: " + state.fitness_goal,
        Button("Home", "index"),
        Button("Settings", "settings")
    ])

@route
def progress(state: State) -> Page:
    total_workouts = len(state.workouts)

    content = [
        Header("Your Progress"),
        "Fitness Goal: " + state.fitness_goal,
        "Total Workouts: " + str(total_workouts)
    ]

    if total_workouts == 0:
        content.append("You haven't recorded any workouts yet.")
    else:
        content.append("Here are your workouts:")

        for workout in state.workouts:
            content.append(
                workout.date + " - " + workout.category
            )

    content.append(Button("Home", "index"))

    return Page(state, content)


start_server(State("User", "Build muscle", [], 1))
