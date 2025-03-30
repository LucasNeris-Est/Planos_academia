from fastapi import APIRouter
from app.producer import send_to_queue

router = APIRouter()

@router.post("/checkins", summary="Processar check-ins em massa")
def processar_checkins_em_massa():
    """
    Envia uma mensagem para a fila 'fila_checkin' para processar check-ins em massa.
    """
    send_to_queue("fila_checkin", {"acao": "processar_checkins"})
    return {"mensagem": "Solicitação enviada para processar check-ins"}

@router.post("/relatorio", summary="Gerar relatório de frequência")
def gerar_relatorio():
    """
    Envia uma mensagem para a fila 'fila_relatorio' para gerar o relatório de frequência diária.
    """
    send_to_queue("fila_relatorio", {"acao": "gerar_relatorio"})
    return {"mensagem": "Solicitação enviada para gerar relatório"}

@router.post("/churn", summary="Atualizar modelo de churn")
def atualizar_modelo_churn():
    """
    Envia uma mensagem para a fila 'fila_churn' para atualizar o modelo de previsão de churn.
    """
    send_to_queue("fila_churn", {"acao": "atualizar_modelo"})
    return {"mensagem": "Solicitação enviada para atualizar modelo de churn"}
