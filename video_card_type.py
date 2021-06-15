from typing import Optional


class VideoCard:
    """Video card class."""
    def __init__(self, name: str, msrp: int, strength: int = None):
        self.name: str = name
        self.msrp: int = msrp
        self.strength: Optional[int] = strength
        self.VfM: Optional[int] = int(strength/msrp) if strength else None
        self.enable = True
        self.id_tag = self.create_id_tag()

    def create_id_tag(self) -> str:
        name_token = self.name.split(' ')
        valid_token = [name_token[-1]] if name_token[-1] != 'Ti' and name_token[-1] != 'XT' else [name_token[-2], name_token[-1]]
        id_tag = '-'.join(valid_token)
        return id_tag

    def get_VfM(self) -> int:
        return self.VfM or 0

    def __str__(self) -> str:
        return str(self.__dict__)
