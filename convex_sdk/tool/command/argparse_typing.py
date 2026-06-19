from argparse import (
    ArgumentParser,
    Namespace
)
from typing import (
    Any,
    Protocol
)

from pydantic import (
    BaseModel,
    Field
)


class SubParsersAction(Protocol):
    @property
    def choices(self) -> dict[str, ArgumentParser]:
        ...

    def add_parser(self, name: str, **kwargs: Any) -> ArgumentParser:
        ...

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any, option_string: str | None = None) -> None:
        ...


class BaseArgs(BaseModel):
    keyfile: None | str = None
    keytext: None | str = None
    password: None | str = None
    keywords: None | str = None
    debug: bool = False
    output_json: bool = Field(alias='json', default=False)
    url: str
