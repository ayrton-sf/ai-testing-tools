from enum import Enum, auto

from mcp import StdioServerParameters


class DataSource(Enum):
    WEB = auto()
    SQL = auto()
    VECTOR = auto()

    @property
    def required_args(self):
        return {
            DataSource.WEB: ["urls"],
            DataSource.SQL: ["db_string"],
        }[self]


def get_postgres_mcp(db_string: str) -> StdioServerParameters:
    return StdioServerParameters(
        command="postgres-mcp",
        args=["--access-mode=unrestricted"],
        env={"DATABASE_URI": db_string},
    )
