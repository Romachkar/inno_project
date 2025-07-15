from aiogram.fsm.state import State, StatesGroup

class UniversityForm(StatesGroup):
    location_choice = State()
    cities_russia = State()
    cities_other = State()
    direction = State()
    scores = State()