from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    cities = State()
    direction = State()
    score = State()