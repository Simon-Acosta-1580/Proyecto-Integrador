from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class AnalisisBeneficioLink(SQLModel, table=True):
    analisis_id: Optional[int] = Field(default=None, foreign_key="analisis.id", primary_key=True)
    beneficio_id: Optional[int] = Field(default=None, foreign_key="beneficio.id", primary_key=True)

class UserBase(SQLModel):
    name: str
    email: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: Optional[str] = Field(default="investigator")
    activo: bool = Field(default=True)

    metodologias: List["Metodologia"] = Relationship(back_populates="usuario")

class UserCreate(UserBase):
    pass

class MetodologiaBase(SQLModel):
    titulo: str
    descripcion: Optional[str] = None

class Metodologia(MetodologiaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: Optional[str] = None
    impacto: Optional[float] = Field(default=0.0)
    activo: bool = Field(default=True)

    usuario_id: Optional[int] = Field(default=None, foreign_key="user.id")
    usuario: Optional[User] = Relationship(back_populates="metodologias")

    analisis: Optional["Analisis"] = Relationship(back_populates="metodologia", sa_relationship_kwargs={"uselist": False})

class AnalisisBase(SQLModel):
    nombre: str
    resultado: Optional[str] = None
    alcance_medios: Optional[float] = 0.0
    participacion_redes: Optional[float] = 0.0
    impacto_total: Optional[float] = 0.0
    activo: bool = Field(default=True)

class Analisis(AnalisisBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    metodologia_id: Optional[int] = Field(default=None, foreign_key="metodologia.id", unique=True)
    metodologia: Optional[Metodologia] = Relationship(back_populates="analisis")
    beneficios: List["Beneficio"] = Relationship(back_populates="analisises", link_model=AnalisisBeneficioLink)

class BeneficioBase(SQLModel):
    categoria: str
    ingreso: float
    periodo: Optional[str] = None
    activo: bool = Field(default=True)

class Beneficio(BeneficioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: Optional[str] = None
    analises: List[Analisis] = Relationship(back_populates="beneficios", link_model=AnalisisBeneficioLink)
