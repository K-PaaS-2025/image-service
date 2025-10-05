from openai import OpenAI

import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized successfully")

    def generate_letter(self, image_url: str) -> Optional[str]:
        # Create message with image URL and prompt
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """이 강아지 사진을 보고 강아지의 관점에서 마음이 따뜻한 편지를 한국어로 작성해주세요.

                                강아지의 외모, 표정, 주변 환경 및 관찰할 수 있는 모든 세부 사항을 고려하세요.
                                강아지가 사랑하는 누군가(주인, 친구, 가족)에게 직접 말하는 것처럼 작성하세요.

                                편지는 다음과 같아야 합니다:
                                - 강아지의 관점에서 1인칭으로 작성
                                - 따뜻하고 감동적
                                - 강아지가 그 순간 보고 느끼는 것에 대한 관찰 포함
                                - 2-3 문장 분량
                                - 외모를 바탕으로 한 강아지의 성격 표현
                                - 한국어로 작성

                                "사랑하는 [특별한 사람]에게,"로 시작하고 강아지의 사랑스러운 서명으로 마무리하세요."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )

            letter = response.choices[0].message.content
            logger.info("Generated letter from image URL successfully")
            return letter

        except Exception as e:
            logger.error(f"Failed to generate letter: {e}")
            return None