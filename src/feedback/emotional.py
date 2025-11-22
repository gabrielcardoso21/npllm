"""
Análise emocional: modelo de sentimento simples
Detecta positivo/negativo/neutro do feedback do usuário
"""

import torch
from typing import Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.utils.config import get_config
from src.utils.logging import get_logger


class EmotionalAnalyzer:
    """
    Analisador emocional simples
    Detecta sentimento (positivo/negativo/neutro) do texto do usuário
    """
    
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """
        Inicializa analisador emocional
        
        Args:
            model_name: Nome do modelo de sentimento
        """
        self.logger = get_logger(self.__class__.__name__)
        self.model_name = model_name
        self.device = "cpu"
        
        # Lazy loading do modelo
        self._model = None
        self._tokenizer = None
        
        self.logger.info(f"Emotional analyzer initialized (model: {model_name})")
    
    def _load_model(self):
        """Carrega modelo de sentimento (lazy loading)"""
        if self._model is not None:
            return
        
        self.logger.info("Loading sentiment analysis model...")
        
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name
            )
            self._model.to(self.device)
            self._model.eval()
            
            self.logger.info("Sentiment model loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading sentiment model: {e}")
            raise
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analisa sentimento do texto
        
        Args:
            text: Texto para analisar
        
        Returns:
            Dicionário com sentimento e intensidade
        """
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "intensity": 0.0,
                "signal": 0.0
            }
        
        # Carrega modelo se necessário
        self._load_model()
        
        # Tokeniza e processa
        inputs = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)
        
        # Analisa sentimento
        with torch.no_grad():
            outputs = self._model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)[0]
        
        # Mapeia labels (depende do modelo)
        # twitter-roberta-base-sentiment-latest: LABEL_0=negative, LABEL_1=neutral, LABEL_2=positive
        negative_prob = probs[0].item()
        neutral_prob = probs[1].item()
        positive_prob = probs[2].item()
        
        # Determina sentimento dominante
        if positive_prob > negative_prob and positive_prob > neutral_prob:
            sentiment = "positive"
            intensity = positive_prob
            signal = positive_prob  # 0.0 a 1.0
        elif negative_prob > positive_prob and negative_prob > neutral_prob:
            sentiment = "negative"
            intensity = negative_prob
            signal = -negative_prob  # -1.0 a 0.0
        else:
            sentiment = "neutral"
            intensity = neutral_prob
            signal = 0.0
        
        return {
            "sentiment": sentiment,
            "intensity": intensity,
            "signal": signal,  # -1.0 (muito negativo) a +1.0 (muito positivo)
            "probabilities": {
                "positive": positive_prob,
                "neutral": neutral_prob,
                "negative": negative_prob
            }
        }
    
    def get_emotional_reward(self, text: str) -> float:
        """
        Calcula recompensa emocional (-1.0 a +1.0)
        
        Args:
            text: Texto do usuário
        
        Returns:
            Recompensa emocional
        """
        analysis = self.analyze(text)
        return analysis["signal"]

