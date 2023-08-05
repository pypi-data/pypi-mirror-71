# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Union

from braincube_connector import client
from braincube_connector.bases import base_entity, resource_getter
from braincube_connector.memory_base import memory_base


class Braincube(base_entity.BaseEntity, resource_getter.ResourceGetter):
    """Braincube object that handles the feature of a braincube."""

    def __init__(self, bcid: str, name: str, metadata: Dict[str, Any]):
        """Initialize Braincube.

        Args:
            bcid: Braincube unique identifier.
            name: Braincube name.
            metadata: Raw metadata associated to the Braincube.
        """
        super().__init__(bcid, name, metadata, "braincube/{bc_name}".format(bc_name=name))

    def get_memory_base(self, mb_bcid: Union[str, int]) -> memory_base.MemoryBase:
        """Get a MemoryBase object from its id.

        Args:
            mb_bcid: Memory bases bcid.

        Returns:
            The selected MemoryBase object.
        """
        return self._get_resource(memory_base.MemoryBase, mb_bcid)

    def get_memory_base_list(self, **kwargs) -> List[memory_base.MemoryBase]:
        """Get a list of the memory bases available in the braincube.

        Args:
            **kwargs: Optional page and page_size.

        Returns:
            A list of the MemoryBase objects.
        """
        return self._get_resource_list(memory_base.MemoryBase, **kwargs)


def get_braincube(name: str) -> Braincube:
    """Get a braincube object from its name.

    Args:
        name: Name of the selected braincube.

    Returns:
        The selected Braincube object.
    """
    cli = client.get_instance()
    available_braincube_infos = cli.get_braincube_infos()
    return Braincube(*available_braincube_infos[name])


def get_braincube_list(names: List[str] = None) -> List[Braincube]:
    """Get a list of available memory bases in the braincube.

    Args:
        names: List of braincube names to return.

    Returns:
        List of the Braincube objects.
    """
    cli = client.get_instance()
    available_braincube_infos = cli.get_braincube_infos()
    if not names:
        names = list(available_braincube_infos.keys())
    return [Braincube(*available_braincube_infos[key]) for key in names]
