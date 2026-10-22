from pydantic import Basemodel

class Slide(Basemodel):
    title: str | None = None
    subtitle: str | None = None
    content: str | list[str] | None = None
    backgroudImage: str | None = None


class Config(Basemodel):
    pass
