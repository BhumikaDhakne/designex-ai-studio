from backend.app.services.ai_service import AIService


service = AIService()

result = service.test_connection()

print(result)