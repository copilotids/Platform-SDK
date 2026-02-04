from pydantic import BaseModel


class CommandDescriptor(BaseModel):
    """
    Describe a command that can be sent to the Platform.
    """

    name: str
    """
    The name of the command.
    """
    payload: BaseModel
    """
    The payload schema of the command.
    """
    result: BaseModel
    """
    The result schema of the command.
    """


# descriptor = CommandDescriptor(
#     name="user.create",
#     payload=BaseModel.model_validate(
#         {
#             "email": str,
#             "name": str,
#             "surname": str,
#         },
#     ),
#     result=BaseModel.model_validate(
#         {
#             "email": str,
#             "name": str,
#             "surname": str,
#         },
#     ),
# )
