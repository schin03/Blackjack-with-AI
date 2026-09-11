from pydantic import BaseModel, ConfigDict, Field

class UserCredentials(BaseModel):
    username: str = Field(
        min_length = 3,
        max_length = 50,
        pattern = r"^[A-Za-z0-9_]+"
    )
    password: str = Field(min_length = 8, max_length = 128)


class UserPublic (BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)