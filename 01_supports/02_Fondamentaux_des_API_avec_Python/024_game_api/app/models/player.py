from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    name: str = Field(min_length=3, max_length=99)
    score: int = Field(ge=0, le=99999)
    level: int = Field(ge=1, le=99)


class Player(PlayerCreate):
    id: int