# API Monitoramento de Idosos

## Autenticação
- **Session Auth**: Use cookies de sessão Django
- **Token Auth**: Adicione `Authorization: Token &lt;token&gt;` no header

## Endpoints

### Idosos
- `GET /api/idosos/` - Lista todos os idosos
- `POST /api/idosos/` - Cria novo idoso
- `GET /api/idosos/{id}/` - Detalhes do idoso
- `POST /api/idosos/{id}/receber_dados/` - Recebe dados de dispositivo

### Dispositivos
- `GET /api/dispositivos/` - Lista dispositivos
- `POST /api/dispositivos/` - Cria dispositivo

### Dados de Saúde
- `GET /api/dados-saude/?idoso=1` - Filtra por idoso
- `GET /api/dados-saude/?start_date=2024-01-01&end_date=2024-01-31` - Filtra por data

### Alertas
- `GET /api/alertas/?visualizado=false` - Alertas não lidos
- `POST /api/alertas/{id}/marcar-lido/` - Marca alerta como lido

## Exemplos

### Enviar dados de dispositivo:
```bash
curl -X POST http://127.0.0.1:8000/api/idosos/1/receber_dados/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token seu_token" \
  -d '{
    "dispositivo_id": "AW9-11122233344",
    "frequencia_cardiaca": 75,
    "pressao_sistolica": 120,
    "pressao_diastolica": 80,
    "saturacao_oxigenio": 98.5,
    "temperatura": 36.8,
    "passos": 5420,
    "queda_detectada": false
  }'