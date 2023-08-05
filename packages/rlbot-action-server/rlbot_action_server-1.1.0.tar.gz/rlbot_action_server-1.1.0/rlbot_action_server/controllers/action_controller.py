import connexion
from rlbot_action_server import bot_holder
from rlbot_action_server.models.action_choice import ActionChoice  # noqa: E501
from rlbot_action_server.models.api_response import ApiResponse  # noqa: E501


def choose_action(body):
    if connexion.request.is_json:
        body = ActionChoice.from_dict(connexion.request.get_json())
        action_broker = bot_holder.get_bot_action_broker()
        if action_broker is not None:
            response = action_broker.set_action(body)
            if response:
                return response
            return ApiResponse(200, f'Probably set action: {body.action.description}')


def get_actions_currently_available():
    action_broker = bot_holder.get_bot_action_broker()
    if action_broker is not None:
        return action_broker.get_actions_currently_available()
