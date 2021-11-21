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
