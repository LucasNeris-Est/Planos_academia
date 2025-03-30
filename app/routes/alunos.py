from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import psycopg2
import json
import os

# ----------------------------
# Configuração do banco
# ----------------------------
dir_atual = os.path.dirname(__file__)
dir_pai = os.path.dirname(dir_atual)
dir_avo = os.path.dirname(dir_pai)

config_path = os.path.join(dir_avo, "banco.json")

with open(config_path, "r") as f:
    db_config = json.load(f)

def get_connection():
    return psycopg2.connect(**db_config)

# ----------------------------
# Inicializa o router
# ----------------------------
router = APIRouter()

# ---------------------
# MODELOS
# ---------------------
class AlunoCreate(BaseModel):
    nome: str = Field(..., example="João da Silva")
    email: str = Field(..., example="joao@email.com")
    data_nascimento: str = Field(..., example="1990-05-12", description="Data no formato YYYY-MM-DD")
    plano_id: int = Field(..., example=1)

    class Config:
        schema_extra = {
            "example": {
                "nome": "Maria Oliveira",
                "email": "maria@email.com",
                "data_nascimento": "1988-11-23",
                "plano_id": 2
            }
        }

class CheckinRequest(BaseModel):
    aluno_id: int = Field(..., example=42)

# ---------------------
# ENDPOINTS
# ---------------------

# ----------------------------
# Endpoint para registrar novo aluno
# ----------------------------
@router.post("/registro", summary="Registrar novo aluno", response_description="Aluno criado com sucesso")
def registrar_aluno(aluno: AlunoCreate):
    """
    Registra um novo aluno na base de dados da academia.
    """
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO alunos (nome, email, data_nascimento, plano_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (aluno.nome, aluno.email, aluno.data_nascimento, aluno.plano_id))
        aluno_id = cur.fetchone()[0]
        con.commit()
        cur.close()
        con.close()
        return {"mensagem": "Aluno registrado com sucesso", "aluno_id": aluno_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------------------
# Endpoint para retornar dados de frequência do aluno
# ----------------------------
@router.get("/{id}/frequencia", summary="Histórico de check-ins do aluno")
def obter_frequencia(id: int = Path(..., description="ID do aluno", example=42)):
    """
    Retorna o histórico de frequência (check-ins) do aluno, ordenado da data mais recente para a mais antiga.
    """
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT data_checkin
            FROM checkins
            WHERE aluno_id = %s
            ORDER BY data_checkin DESC
        """, (id,))
        resultados = cur.fetchall()
        cur.close()
        con.close()
        return {"aluno_id": id, "checkins": [r[0].isoformat() for r in resultados]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------
# Endpoint para verificar risco de churn (desistência)
# ----------------------------
@router.get("/{id}/risco-churn", summary="Verificar risco de churn (desistência)")
def risco_churn(id: int = Path(..., description="ID do aluno", example=42)):
    """
    Analisa a frequência do aluno e retorna a probabilidade de desistência com base no tempo sem check-in.
    """
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT data_checkin
            FROM checkins
            WHERE aluno_id = %s
            ORDER BY data_checkin DESC
        """, (id,))
        checkins = cur.fetchall()
        cur.close()
        con.close()

        if not checkins:
            return {"aluno_id": id, "risco_churn": "alto", "motivo": "Sem check-ins registrados"}

        ultimo_checkin = checkins[0][0]
        dias_sem_frequencia = (datetime.now() - ultimo_checkin).days

        if dias_sem_frequencia > 15:
            risco = "alto"
        elif dias_sem_frequencia > 7:
            risco = "moderado"
        else:
            risco = "baixo"

        return {
            "aluno_id": id,
            "dias_sem_frequencia": dias_sem_frequencia,
            "risco_churn": risco
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))