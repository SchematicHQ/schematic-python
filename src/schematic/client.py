from .base_client import AsyncBaseSchematic, BaseSchematic

class Schematic(BaseSchematic): 

    def initialize(self) -> None: 
        pass


class AsyncSchematic(AsyncBaseSchematic): 

    async def initialize(self) -> None: 
        pass