from dataclasses import dataclass
from typing import Optional


@dataclass
class FifaPlayer:
    """Classe para representar dados de jogadores do FIFA 23"""
    name: str
    full_name: str
    age: int
    height_cm: int
    weight_kg: int
    nationality: str
    club: str
    position: str
    overall: int
    value_eur: float
    wage_eur: float
    release_clause_eur: Optional[float]
    potential: int
    preferred_foot: str
    attacking_work_rate: str
    defensive_work_rate: str
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defending: int
    physicality: int

    @classmethod
    def from_csv_row(cls, row: dict) -> 'FifaPlayer':
        """Cria uma instância de FifaPlayer a partir de uma linha do CSV"""
        return cls(
            name=str(row.get('Name', '')),
            full_name=str(row.get('LongName', '')),
            age=int(row.get('Age', 0)),
            height_cm=int(row.get('Height', 0)),
            weight_kg=int(row.get('Weight', 0)),
            nationality=str(row.get('Nationality', '')),
            club=str(row.get('Club', '')),
            position=str(row.get('BestPosition', '')),
            overall=int(row.get('Overall', 0)),
            value_eur=float(row.get('Value', 0)),
            wage_eur=float(row.get('Wage', 0)),
            release_clause_eur=float(row.get('ReleaseClause', 0)) if row.get('ReleaseClause') else None,
            potential=int(row.get('Potential', 0)),
            preferred_foot=str(row.get('Foot', '')),
            attacking_work_rate=str(row.get('AttackingWorkRate', '')),
            defensive_work_rate=str(row.get('DefensiveWorkRate', '')),
            pace=int(row.get('Pace', 0)),
            shooting=int(row.get('Shooting', 0)),
            passing=int(row.get('Passing', 0)),
            dribbling=int(row.get('Dribbling', 0)),
            defending=int(row.get('Defending', 0)),
            physicality=int(row.get('Physicality', 0))
        )

    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'Name': self.name,
            'LongName': self.full_name,
            'Age': self.age,
            'Height': self.height_cm,
            'Weight': self.weight_kg,
            'Nationality': self.nationality,
            'Club': self.club,
            'BestPosition': self.position,
            'Overall': self.overall,
            'Value': self.value_eur,
            'Wage': self.wage_eur,
            'ReleaseClause': self.release_clause_eur,
            'Potential': self.potential,
            'Foot': self.preferred_foot,
            'AttackingWorkRate': self.attacking_work_rate,
            'DefensiveWorkRate': self.defensive_work_rate,
            'Pace': self.pace,
            'Shooting': self.shooting,
            'Passing': self.passing,
            'Dribbling': self.dribbling,
            'Defending': self.defending,
            'Physicality': self.physicality
        }
