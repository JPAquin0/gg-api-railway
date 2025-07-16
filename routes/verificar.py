# routes/verificar.py
import os
import httpx
import random
import string
from fastapi import APIRouter, Request, JSONResponse

router = APIRouter()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@router.post("/api/verificar")
async def processar_verificacao(request: Request):
    # O conteúdo desta função é exatamente o mesmo da última versão.
    # Nenhuma mudança na lógica do checker é necessária aqui.
    if not ACCESS_TOKEN:
        return JSONResponse(status_code=500, content={"status": "DIE", "nome": "Erro de Configuração", "mensagem": "ACCESS_TOKEN não configurado."})
    try:
        dados = await request.json()
        token = dados.get("token")
        payment_method_id = dados.get("payment_method_id")
        if not token or not payment_method_id:
            return JSONResponse(status_code=400, content={"status": "DIE", "nome": "Dados Ausentes", "mensagem": "Token e payment_method_id são obrigatórios."})
        
        random_user = ''.join(random.choices(string.ascii_lowercase, k=10))
        payer_email = f"user_{random_user}@test.com"
        valor_aleatorio = round(random.uniform(0.77, 1.99), 2)
        url = "https://api.mercadopago.com/v1/payments"
        
        payload = {"transaction_amount": valor_aleatorio,"token": token,"payment_method_id": payment_method_id,"installments": 1,"payer": {"email": payer_email}}
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}","Content-Type": "application/json","X-Idempotency-Key": os.urandom(16).hex()}

        async with httpx.AsyncClient() as client:
            resposta = await client.post(url, json=payload, headers=headers, timeout=20.0)
        
        resultado = resposta.json()
        status_code = resposta.status_code
        
        if status_code in [200, 201] and resultado.get("status") == "approved":
            return {"status": "LIVE", "nome": "Aprovado", "mensagem": f"Pagamento de R${valor_aleatorio:.2f} debitado."}
        
        status_detail = resultado.get("status_detail", "desconhecido")
        
        if status_detail == "cc_rejected_insufficient_amount":
            return {"status": "LIVE", "nome": "Saldo Insuficiente", "mensagem": "Cartão existe e é válido."}
        
        if resultado.get("status") == "in_process":
            return {"status": "DIE", "nome": "Recusado (Antifraude)", "mensagem": "Pagamento retido para análise de risco."}
        
        return {"status": "DIE", "nome": f"Recusado ({status_detail})", "mensagem": "Pagamento não aprovado pelo emissor."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "DIE", "nome": "Erro Interno", "mensagem": str(e)})

