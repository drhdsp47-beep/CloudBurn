from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn

app = FastAPI(title="CloudBurn: Zero-Cost Router")

# الرابط الافتراضي لمحرك Ollama الذي سيقوم مستخدم المشروع بتشغيله على جهازه هو
OLLAMA_URL = "http://localhost:11434/api/generate"

class QueryRequest(BaseModel):
    prompt: str
    model_name: str = "llama3"

@app.post("/v1/chat/completions")
async def route_to_free_local_ai(request: QueryRequest):
    # حساب حجم التوفير المالي للمستخدم مقارنة بالنماذج المدفوعة
    words_count = len(request.prompt.split())
    estimated_saved_money = (words_count / 1000) * 0.005
    
    ollama_payload = {
        "model": request.model_name,
        "prompt": request.prompt,
        "stream": False
    }
    
    try:
        # توجيه الطلب إلى السيرفر المحلي الخاص بالمستخدم النهائي مجاناً 100%
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_URL, json=ollama_payload, timeout=60.0)
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="خطأ: تأكد من تشغيل Ollama على جهازك وتحميل النموذج المختار.")
                
            result = response.json()
            
            return {
                "status": "success",
                "ai_response": result.get("response"),
                "cost_incurred": "$0.00000",
                "estimated_savings": f"${estimated_saved_money:.5f}",
                "security": "100% Offline & Local Data"
            }
            
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="فشل الاتصال بمحرك الذكاء الاصطناعي المحلي للمستخدم.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
