from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class SDLReader(BaseReader):
    """Schema definition langauge reader

    Reads GraphQL Schema files

    """

    def load_data(self, filename: str) -> List[Document]:
        """Parse file."""
        try:
            import graphql
        except ImportError:
            raise ImportError("Please install graphql 'pip install graphql-core' ")
        with open(filename, "r") as f:
            txt = f.read()

        ast = graphql.parse(txt)
        chunks = [
            txt[definition.loc.start : definition.loc.end]
            for definition in ast.definitions
        ]
        return [Document(text=chunk) for chunk in chunks]
