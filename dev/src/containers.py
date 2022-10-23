from dependency_injector import containers
from data import (
    Repository,
)

class Container(containers.DeclarativeContainer):
    ### test ###
    wiring_config = containers.WiringConfiguration(modules=["endpoints"])
    repository = Repository()

    def get_repository(self):
        return self.repository
