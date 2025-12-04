from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    name: str = Field(index=True,description="Nombre de usuario" ,unique=True)
    email: str = Field(index=True,description="Email de usuario" ,unique=True)
    role: Optional[str] = Field(default="investigator")
    status: bool =Field(default=True,description="Activio o inactivo")
    img: Optional[str] = Field(default=None, description="User image")

class MetodologiaBase(SQLModel):
    titulo: str = Field(index=True,description="Titulo de la base de datos" ,unique=True)
    descripcion: Optional[str] = Field(index=True,description="Descripcion de la base de datos" ,unique=True)
    status: bool = Field(default=True,description="Activio o inactivo")
    user_id: Optional[int] = Field(default= None,foreign_key="user.id")

class AnalisisBase(SQLModel):
    nombre: str = Field(index=True,description="Nombre de la base de datos")
    alcance_medios: Optional[float] = Field(default=0, description="Medio de la alcance")
    participacion_redes: Optional[float] = Field(default=0, description="Rede de la participacion")
    status: bool = Field(default=True, description="Activio o inactivo")
    metodologia_id: Optional[int] = Field(default=None, foreign_key="metodologia.id")

class BeneficioBase(SQLModel):
    categoria: str = Field(index=True,description="Categoria de la base de datos")
    ingreso: float = Field(default=0, description="Ingreso de la base de datos")
    status: bool = Field(default=True, description="Activio o inactivo")
    analisis_id: Optional[int] = Field(default=None, foreign_key="analisis.id")

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    metodologias: list["Metodologia"] = Relationship(back_populates="usuario")

class Metodologia(MetodologiaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: User = Relationship(back_populates="metodologias")
    analisis: list["Analisis"] = Relationship(back_populates="metodologia")

class Analisis(AnalisisBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    metodologia: Metodologia = Relationship(back_populates="analisis")
    beneficios: list["Beneficio"] = Relationship(back_populates="analisis")

class Beneficio(BeneficioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analisis: Analisis = Relationship(back_populates="beneficios")

class UserCreate(UserBase):
    pass

class MetodologiaCreate(MetodologiaBase):
    user_id: int = Field(foreign_key="user.id")

class AnalisisCreate(AnalisisBase):
    metodologia_id: int = Field(foreign_key="metodologia.id")

class BeneficioCreate(BeneficioBase):
    analisis_id: int = Field(foreign_key="analisis.id")
