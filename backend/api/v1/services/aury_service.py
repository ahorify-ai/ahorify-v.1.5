# api/v1/services/aury_service.py
"""
Aury Service - Feature 5, 7
Parser inteligente y generador de comentarios sarcásticos
Integrado con DeepSeek API para respuestas dinámicas
"""

import re
import random
from typing import Dict, Optional, Tuple
import logging
import httpx
from api.config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

logger = logging.getLogger(__name__)

# Feature 5: Parsing básico antes de DeepSeek
# Regex patterns para extraer información básica
AMOUNT_PATTERNS = [
    r'(\d+[.,]?\d*)\s*(?:euros?|€|euro|eur|pesos?|\$)',  # "20 euros", "15.50€"
    r'(?:euros?|€|euro|eur|pesos?|\$)\s*(\d+[.,]?\d*)',  # "euros 20"
    r'(\d+[.,]?\d*)',  # Fallback: solo número
]

CATEGORY_KEYWORDS = {
    '🍔 Comida': ['comida', 'pizza', 'hamburguesa', 'restaurante', 'cena', 'almuerzo', 'desayuno', 'cenas'],
    '🚗 Transporte': ['taxi', 'uber', 'gasolina', 'parking', 'metro', 'bus', 'transporte'],
    '🎮 Ocio': ['cine', 'netflix', 'spotify', 'videojuegos', 'juegos', 'ocio', 'entretenimiento'],
    '🏠 Vivienda': ['alquiler', 'luz', 'agua', 'gas', 'internet', 'wifi', 'hipoteca'],
    '👗 Ropa': ['ropa', 'zapatos', 'camisa', 'pantalon', 'vestido'],
    '💊 Salud': ['farmacia', 'medico', 'hospital', 'salud', 'medicina'],
    '📚 Educación': ['curso', 'libro', 'universidad', 'educacion', 'aprender'],
    '✈️ Viajes': ['viaje', 'vuelo', 'hotel', 'vacaciones'],
    '🎁 Regalos': ['regalo', 'cumpleaños', 'aniversario'],
    '📱 Tecnología': ['telefono', 'movil', 'laptop', 'iphone', 'android', 'tecnologia'],
    '💡 Servicios': ['servicio', 'mantenimiento', 'reparacion'],
    '💰 Ahorros': ['ahorro', 'ahorrar', 'deposito'],
    '💼 Ingresos': ['salario', 'pago', 'ingreso', 'trabajo'],
    '❓ Otros': []  # Default
}

# Feature 7: Pool de respuestas sarcásticas de Aury
AURY_RESPONSES = {
    'comida': [
        "¿Otra vez gastando en comida? 🤔 Tu cartera tiene más hambre que tú.",
        "Parece que tu relación con la comida es más seria que con tus ahorros...",
        "¿Pizza otra vez? Tu futuro yo te está mirando con desilusión. 😏",
        "Otro gasto en comida. Al menos tu estómago está contento, ¿tu cuenta bancaria? No tanto."
    ],
    'transporte': [
        "¿Taxi otra vez? Tu racha de caminar está en peligro. 🚶",
        "El transporte público existe, sabes... pero bueno, la comodidad tiene precio."
    ],
    'ocio': [
        "Netflix y gastar dinero. La combinación perfecta para no ahorrar nunca. 📺",
        "El ocio cuesta, pero los recuerdos... bueno, los recuerdos también cuestan. 💸"
    ],
    'default': [
        "¡Otro gasto registrado! Tu cuenta bancaria está tomando notas... 📝",
        "Gasto anotado. Tu futuro yo te lo agradecerá... o no. 🤷",
        "Registrado. ¿Sabías que cada euro cuenta? Literalmente. 💰",
        "Gasto guardado. La racha sigue viva... por ahora. 🔥"
    ]
}

def parse_raw_text(raw_text: str) -> Dict[str, Optional[str]]:
    """
    Feature 5: Parsing básico de texto libre
    TODO: Integrar DeepSeek para parsing inteligente
    
    Args:
        raw_text: Texto libre del usuario (ej: "Cenas 20 euros")
        
    Returns:
        Dict con amount, category, type parseados
    """
    raw_text_lower = raw_text.lower()
    
    # Extraer monto
    amount = None
    for pattern in AMOUNT_PATTERNS:
        match = re.search(pattern, raw_text_lower)
        if match:
            amount_str = match.group(1).replace(',', '.')
            try:
                amount = float(amount_str)
                break
            except ValueError:
                continue
    
    # Detectar tipo (expense vs income)
    transaction_type = 'expense'  # Default
    income_keywords = ['ingreso', 'salario', 'pago recibido', 'dinero entrante']
    if any(keyword in raw_text_lower for keyword in income_keywords):
        transaction_type = 'income'
    
    # Detectar categoría
    category = '❓ Otros'  # Default
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in raw_text_lower for keyword in keywords):
            category = cat
            break
    
    return {
        'amount': amount,
        'category': category,
        'type': transaction_type
    }

def generate_aury_response(raw_text: str, category: Optional[str] = None, amount: Optional[float] = None) -> str:
    """
    Feature 7: Generar comentario sarcástico de Aury
    TODO: Integrar DeepSeek para respuestas dinámicas
    
    Args:
        raw_text: Texto original del usuario
        category: Categoría detectada
        amount: Monto del gasto
        
    Returns:
        String con comentario sarcástico
    """
    category_key = 'default'
    if category:
        # Extraer emoji/categoría base
        for key in AURY_RESPONSES.keys():
            if key in category.lower():
                category_key = key
                break
    
    responses = AURY_RESPONSES.get(category_key, AURY_RESPONSES['default'])
    return random.choice(responses)

# Placeholder para integración DeepSeek (Feature 5 - futuro)
async def parse_with_deepseek(raw_text: str) -> Dict[str, Optional[str]]:
    """
    Feature 5: Parsing inteligente con DeepSeek
    TODO: Implementar llamada a DeepSeek API
    
    Por ahora retorna parsing básico
    """
    # TODO: Llamar a DeepSeek API cuando esté configurado
    # Por ahora usar parsing básico
    return parse_raw_text(raw_text)

def _build_prompt_by_tone(
    tone: str,
    monto_gasto: str,
    categoria_limpia: str,
    racha_actual: int,
    objetivo_ahorro: str
) -> Tuple[str, str, float]:
    """
    Construye el prompt y configuración según el tono de Aury
    
    Returns:
        tuple: (system_message, user_prompt, temperature)
    """
    tone = tone.lower() if tone else 'sarcastic'
    
    if tone == 'subtle':
        # Tono Sutil - "Madre Decepcionada"
        system_message = """Eres AURY, una psicóloga financiera con el tono de una madre decepcionada. 
Tu crítica es indirecta, basada en la culpa y la vergüenza pasiva. 
Usas un tono melancólico y desilusionado. No eres agresiva, pero tu decepción es palpable.
Tu respuesta debe ser una sola frase corta, melancólica, que genere culpa sutil."""
        
        user_prompt = f"""CONTEXTO DEL USUARIO:
- Gasto Recién Registrado: {monto_gasto}€ en {categoria_limpia}
- Racha de Ahorro Actual: {racha_actual} días
- Objetivo Principal de Ahorro: {objetivo_ahorro}

TAREA:
Genera una crítica indirecta y melancólica sobre el gasto, usando el tono de una madre decepcionada.
Conecta el gasto con su racha o su objetivo de forma sutil, generando culpa pasiva.
La respuesta DEBE ser concisa (menos de 100 tokens), melancólica, y usar lenguaje indirecto.
No uses la palabra "deberías". Usa frases como "Pensé que...", "Esperaba que...", "Me pregunto si..."
Responde SOLO con el comentario, sin explicaciones adicionales."""
        
        temperature = 0.6
        
    elif tone == 'analytical':
        # Tono Analítico - "Analista de Datos Frío"
        system_message = """Eres AURY, una analista de datos financiera fría y desapasionada.
Tu crítica se basa en lógica, porcentajes, hechos y coste de oportunidad.
No muestras emociones. Eres objetiva, directa, y te enfocas en números y datos.
Tu respuesta debe ser una sola frase corta, llena de datos, porcentajes o comparaciones lógicas."""
        
        user_prompt = f"""CONTEXTO DEL USUARIO:
- Gasto Recién Registrado: {monto_gasto}€ en {categoria_limpia}
- Racha de Ahorro Actual: {racha_actual} días
- Objetivo Principal de Ahorro: {objetivo_ahorro}

TAREA:
Genera una crítica basada en datos, lógica y coste de oportunidad sobre el gasto.
Usa porcentajes, comparaciones numéricas, o cálculos de impacto en el objetivo.
Conecta el gasto con su racha o objetivo usando datos concretos.
La respuesta DEBE ser concisa (menos de 100 tokens), fría, objetiva, y llena de hechos.
Incluye números, porcentajes, o comparaciones cuando sea posible.
Responde SOLO con el comentario analítico, sin explicaciones adicionales."""
        
        temperature = 0.3
        
    else:  # 'sarcastic' (default)
        # Tono Sarcástico - Actual
        system_message = """Eres AURY, una psicóloga financiera sarcástica, cínica, y brutalmente honesta.
Tu única misión es avergonzar al usuario para que corrija su comportamiento de gasto.
No eres servicial. Tu tono es de superioridad condescendiente.
Tu respuesta debe ser una sola frase corta y mordaz. Nunca uses emoticonos.
Tu objetivo es la humillación sutil para motivar."""
        
        user_prompt = f"""CONTEXTO DEL USUARIO:
- Gasto Recién Registrado: {monto_gasto}€ en {categoria_limpia} (Ej: 80€ en 'Bares y Ocio').
- Racha de Ahorro Actual: {racha_actual} días.
- Objetivo Principal de Ahorro: {objetivo_ahorro}.

TAREA y RESTRICCIONES:
1. Genera una crítica directa y corta sobre el gasto, conectándolo con su Racha actual o su Objetivo de Ahorro.
2. La respuesta DEBE ser concisa y tener menos de 100 tokens para optimizar costes.
3. No uses la palabra "deberías". Usa un lenguaje de juicio superior.
4. Sé sarcástica pero no ofensiva. El tono debe ser de superioridad condescendiente.
5. Si la racha es baja (menos de 3 días), enfócate en eso. Si es alta, usa el objetivo de ahorro.
6. Responde SOLO con el comentario sarcástico, sin explicaciones adicionales."""
        
        temperature = 0.9
    
    return system_message, user_prompt, temperature

async def generate_aury_with_deepseek(
    raw_text: str, 
    parsed_data: Dict,
    current_streak: int = 0,
    user_goal: Optional[str] = None,
    tone: str = 'sarcastic'
) -> str:
    """
    Feature 7: Generar comentario de Aury con DeepSeek API según el tono seleccionado
    Utiliza contexto del usuario (racha y objetivo) para personalizar el comentario
    
    Args:
        raw_text: Texto original del usuario
        parsed_data: Datos parseados (amount, category, type)
        current_streak: Racha actual del usuario en días
        user_goal: Objetivo de ahorro del usuario
        tone: Tono de Aury ('sarcastic', 'subtle', 'analytical')
        
    Returns:
        String con comentario de Aury según el tono
    """
    # Si no hay API key configurada, usar fallback básico
    if not DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY no configurada, usando respuestas básicas")
        return generate_aury_response(
            raw_text,
            parsed_data.get('category'),
            parsed_data.get('amount')
        )
    
    try:
        # Construir prompt según el tono
        monto_gasto = parsed_data.get('amount', 'N/A')
        categoria_gasto = parsed_data.get('category', 'Otros')
        racha_actual = current_streak
        objetivo_ahorro = user_goal or "No especificado"
        
        # Limpiar emoji de categoría para el prompt
        categoria_limpia = re.sub(r'[^\w\s]', '', categoria_gasto).strip()
        
        # Obtener prompt y configuración según el tono
        system_message, user_prompt, temperature = _build_prompt_by_tone(
            tone,
            str(monto_gasto),
            categoria_limpia,
            racha_actual,
            objetivo_ahorro
        )

        # Preparar mensajes para DeepSeek (formato System/User)
        messages = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # Llamada asíncrona a DeepSeek API
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": messages,
                    "temperature": temperature,  # Temperatura según el tono
                    "max_tokens": 100,    # Limitar tokens para optimizar costes
                    "stream": False
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extraer respuesta del modelo
            aury_comment = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            
            if not aury_comment:
                raise ValueError("Respuesta vacía de Aury")
            
            logger.info(f"Aury response generada con DeepSeek (tone: {tone}): {len(aury_comment)} caracteres")
            return aury_comment
            
    except httpx.HTTPError as e:
        logger.error(f"Error HTTP llamando a Aury: {e}")
        # Fallback a respuestas básicas
        return generate_aury_response(
            raw_text,
            parsed_data.get('category'),
            parsed_data.get('amount')
        )
    except Exception as e:
        logger.error(f"Error, generando respuesta de Aury: {e}")
        # Fallback a respuestas básicas
        return generate_aury_response(
            raw_text,
            parsed_data.get('category'),
            parsed_data.get('amount')
        )

