from enum import Enum


class WeaponType(Enum):
    Sword = 1
    Greatsword = 2
    Axe = 3
    Club = 4
    Fist = 5
    Gun = 6
    Epee = 7
    Spear = 8
    Bow = 9
    Staff = 10
    IntFist = 11
    Spell = 12


str_weapon_types = [WeaponType.Sword, WeaponType.Greatsword, WeaponType.Axe, WeaponType.Club, WeaponType.Spear]
dex_weapon_types = [WeaponType.Epee, WeaponType.Bow, WeaponType.Gun]
agi_weapon_types = [WeaponType.Fist]
int_weapon_types = [WeaponType.IntFist, WeaponType.Staff, WeaponType.Spell]


class MagicType(Enum):
    Fire = 51
    Water = 52
    Earth = 53
    Wind = 54
    Light = 55
    Dark = 56


class DamageType(Enum):
    Slash = 1
    Blunt = 2
    Pierce = 3
    Heat = 4
    Cold = 5
    Lightning = 6
    Sun = 7
    Shadow = 8


class SkillRange(Enum):
    Self = 1
    OneAlly = 2
    AllAllies = 3
    OneEnemy = 4
    AllEnemies = 5
    Row = 6
    Column = 7
    RandomEnemy = 9
    AiExclusive = 11


class FormationBonus:
    def __init__(self):
        self.str = 0
        self.end = 0
        self.dex = 0
        self.agi = 0
        self.int = 0
        self.wil = 0
        self.lov = 0
        self.cha = 0
