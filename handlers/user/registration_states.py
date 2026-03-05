from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    full_name = State()
    age = State()
    phone_number = State()
    education_status = State()
    sat_goal = State()


REGISTRATION_STATE_NAMES = {
    RegistrationStates.full_name.state,
    RegistrationStates.age.state,
    RegistrationStates.phone_number.state,
    RegistrationStates.education_status.state,
    RegistrationStates.sat_goal.state,
}
