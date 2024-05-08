from .base_client import AsyncBaseSchematic, BaseSchematic

class Schematic(BaseSchematic): 

    def initialize() -> None: 
        pass


class AsyncSchematic(BaseSchematic): 

    async def initialize() -> None: 
        pass