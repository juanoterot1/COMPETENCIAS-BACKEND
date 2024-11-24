import boto3
import json

class BedrockService:
    @staticmethod
    def generate_text(prompt, model_id="ai21.jamba-1-5-mini-v1:0", max_tokens=200, temperature=0.7, top_p=0.9, region_name="us-east-1"):
        """
        Genera texto utilizando el modelo especificado en Amazon Bedrock.
        :param prompt: El texto de entrada para generar el resultado.
        :param model_id: ID del modelo a utilizar (por defecto `ai21.jamba-1-5-mini-v1:0`).
        :param max_tokens: Número máximo de tokens en la respuesta.
        :param temperature: Valor de temperatura para controlar la creatividad del modelo.
        :param top_p: Valor de top-p para controlar la aleatoriedad del modelo.
        :param region_name: Región de AWS donde se encuentra Bedrock.
        :return: Respuesta generada por el modelo.
        """
        try:
            # Inicializar cliente de Amazon Bedrock
            client = boto3.client("bedrock-runtime", region_name=region_name)
            
            # Preparar el payload para la solicitud
            payload = {
                "prompt": prompt,
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p,
            }
            
            # Llamar al modelo en Bedrock
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(payload),
                contentType="application/json"
            )
            
            # Parsear la respuesta del modelo
            result = json.loads(response["body"])
            return result.get("generatedText", "No response generated.")
        except Exception as e:
            return f"Error invoking Bedrock model: {str(e)}"

