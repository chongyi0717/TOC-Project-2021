from fsm import TocMachine
def create_machine():
    machine = TocMachine(
        states=["user", "menu","location", "chinese","japanese","america","bbq","others"],
        transitions=[
            {
                "trigger": "advance",
                "source": "user",
                "dest": "location",
                "conditions": "is_going_to_location",
            },
            {
                "trigger": "advance",
                "source": "location",
                "dest": "menu",
                "conditions": "is_going_to_menu",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "chinese",
                "conditions": "is_going_to_chinese",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "japanese",
                "conditions": "is_going_to_japanese",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "america",
                "conditions": "is_going_to_america",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "bbq",
                "conditions": "is_going_to_bbq",
            },
            {
                "trigger": "advance",
                "source": "menu",
                "dest": "others",
                "conditions": "is_going_to_others",
            },
            {"trigger": "go_back", "source": ["menu", "chinese","japanese","america","bbq","location","others"], "dest": "user"},
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,
    )
    return machine