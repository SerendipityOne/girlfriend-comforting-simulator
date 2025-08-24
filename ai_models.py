"""
AI模型封装工具
支持智谱AI（ZhipuAI）和千问AI（Qwen）模型的统一调用接口
"""

import json
import os
from typing import List, Dict, Optional, Tuple, Union

from openai import OpenAI
from zhipuai import ZhipuAI


class AIModelManager:
    """AI模型管理器，支持多种AI模型的统一调用"""

    def __init__(self):
        """初始化AI模型管理器"""
        # 初始化千问客户端
        self.qwen_client = OpenAI(
            api_key=os.environ.get('DASHSCOPE_API_KEY'),  # 您的千问API Key
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # 初始化智谱AI客户端
        self.zhipu_client = ZhipuAI(
            api_key=os.environ.get('ZHIPUAI_API_KEY')  # 您的智谱API Key
        )

        # 支持的模型列表
        self.supported_models = {
            'qwen': ['qwen-plus', 'qwen-max', 'qwen-turbo'],
            'zhipu': ['glm-4.5', 'glm-4.5-flash', 'glm-4.5-plus', 'glm-4.5-air', 'glm-4.5-airx']
        }

    def get_model_provider(self, model_name: str) -> str:
        """
        根据模型名称获取提供商
        
        Args:
            model_name: 模型名称
            
        Returns:
            提供商名称 ('qwen' 或 'zhipu')
        """
        for provider, models in self.supported_models.items():
            if model_name in models:
                return provider

        # 如果没有找到精确匹配，根据名称前缀判断
        if model_name.startswith('qwen'):
            return 'qwen'
        elif model_name.startswith('glm'):
            return 'zhipu'
        else:
            raise ValueError(f"不支持的模型: {model_name}")

    def chat(self,
             messages: List[Dict[str, str]],
             model: str = "qwen-plus",
             temperature: float = 0.7,
             max_tokens: int = 1000) -> Optional[str]:
        """
        统一的对话接口
        
        Args:
            messages: 对话消息列表，格式为 [{"role": "user", "content": "消息内容"}, ...]
            model: 模型名称
            temperature: 控制生成随机性，0-1之间
            max_tokens: 最大生成token数
            
        Returns:
            模型生成的响应内容
        """
        try:
            provider = self.get_model_provider(model)

            if provider == 'qwen':
                return self._qwen_chat(messages, model, temperature, max_tokens)
            elif provider == 'zhipu':
                return self._zhipu_chat(messages, model, temperature, max_tokens)
            else:
                raise ValueError(f"不支持的提供商: {provider}")

        except Exception as e:
            print(f"对话生成错误: {e}")
            return None

    def simple_chat(self,
                    prompt: str,
                    model: str = "qwen-plus",
                    temperature: float = 0.7,
                    max_tokens: int = 1000) -> Optional[str]:
        """
        简单对话接口（单轮对话）
        
        Args:
            prompt: 用户输入的提示词
            model: 模型名称
            temperature: 控制生成随机性
            max_tokens: 最大生成token数
            
        Returns:
            模型生成的响应内容
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model, temperature, max_tokens)

    def _qwen_chat(self,
                   messages: List[Dict[str, str]],
                   model: str,
                   temperature: float,
                   max_tokens: int) -> Optional[str]:
        """千问模型对话实现"""
        try:
            completion = self.qwen_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"千问API调用错误: {e}")
            return None

    def _zhipu_chat(self,
                    messages: List[Dict[str, str]],
                    model: str,
                    temperature: float,
                    max_tokens: int) -> Optional[str]:
        """智谱AI模型对话实现"""
        try:
            completion = self.zhipu_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"智谱AI API调用错误: {e}")
            return None

    def get_chat_with_tokens(self,
                             messages: List[Dict[str, str]],
                             model: str = "qwen-plus",
                             temperature: float = 0.7,
                             max_tokens: int = 1000) -> Tuple[Optional[str], Optional[Dict]]:
        """
        获取对话响应和token使用情况
        
        Args:
            messages: 对话消息列表
            model: 模型名称
            temperature: 控制生成随机性
            max_tokens: 最大生成token数
            
        Returns:
            (响应内容, token使用情况字典)
        """
        try:
            provider = self.get_model_provider(model)

            if provider == 'qwen':
                completion = self.qwen_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                content = completion.choices[0].message.content
                token_dict = {
                    'prompt_tokens': completion.usage.prompt_tokens,
                    'completion_tokens': completion.usage.completion_tokens,
                    'total_tokens': completion.usage.total_tokens,
                }
                return content, token_dict

            elif provider == 'zhipu':
                completion = self.zhipu_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                content = completion.choices[0].message.content
                token_dict = {
                    'prompt_tokens': completion.usage.prompt_tokens,
                    'completion_tokens': completion.usage.completion_tokens,
                    'total_tokens': completion.usage.total_tokens,
                }
                return content, token_dict
            else:
                raise ValueError(f"不支持的提供商: {provider}")

        except Exception as e:
            print(f"API调用错误: {e}")
            return None, None

    def get_embedding(self,
                      text: str,
                      model: str = "embedding-3") -> Optional[List[float]]:
        """
        获取文本嵌入向量（目前仅支持智谱AI）
        
        Args:
            text: 要获取嵌入的文本
            model: 嵌入模型名称
            
        Returns:
            嵌入向量列表
        """
        try:
            response = self.zhipu_client.embeddings.create(
                model=model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"获取嵌入向量错误: {e}")
            return None

    def content_moderation(self,
                           input_text: str,
                           model: str = "qwen-plus") -> Optional[Dict]:
        """
        内容审核功能
        
        Args:
            input_text: 待审核的文本
            model: 用于审核的模型
            
        Returns:
            审核结果字典
        """
        prompt = f"""
        请对以下文本进行内容审核，判断是否包含以下类型的不当内容：
        1. 暴力威胁
        2. 仇恨言论
        3. 自残内容
        4. 性相关内容
        5. 骚扰内容
        6. 违法活动

        请以JSON格式返回审核结果，包含：
        - flagged: true/false (是否被标记)
        - categories: 各类别的判断结果
        - category_scores: 各类别的置信度分数(0-1)

        待审核文本：{input_text}
        注意不要输出```json与```
        """

        response = self.simple_chat(prompt, model)
        try:
            moderation_result = json.loads(response)
            return moderation_result
        except json.JSONDecodeError:
            print("无法解析JSON格式的审核结果")
            return None

    def list_models(self) -> Dict[str, List[str]]:
        """
        获取支持的模型列表
        
        Returns:
            按提供商分组的模型列表
        """
        return self.supported_models.copy()


# 创建全局实例
ai_manager = AIModelManager()


# 便捷函数
def chat_with_qwen(messages: Union[str, List[Dict[str, str]]],
                   model: str = "qwen-plus",
                   temperature: float = 0.7,
                   max_tokens: int = 1000) -> Optional[str]:
    """
    使用千问模型进行对话
    
    Args:
        messages: 消息内容，可以是字符串或消息列表
        model: 千问模型名称
        temperature: 控制生成随机性
        max_tokens: 最大生成token数
        
    Returns:
        模型响应
    """
    if isinstance(messages, str):
        return ai_manager.simple_chat(messages, model, temperature, max_tokens)
    else:
        return ai_manager.chat(messages, model, temperature, max_tokens)


def chat_with_zhipu(messages: Union[str, List[Dict[str, str]]],
                    model: str = "glm-4.5",
                    temperature: float = 0.7,
                    max_tokens: int = 1000) -> Optional[str]:
    """
    使用智谱AI模型进行对话
    
    Args:
        messages: 消息内容，可以是字符串或消息列表
        model: 智谱AI模型名称
        temperature: 控制生成随机性
        max_tokens: 最大生成token数
        
    Returns:
        模型响应
    """
    if isinstance(messages, str):
        return ai_manager.simple_chat(messages, model, temperature, max_tokens)
    else:
        return ai_manager.chat(messages, model, temperature, max_tokens)


def get_embedding_zhipu(text: str, model: str = "embedding-3") -> Optional[List[float]]:
    """
    使用智谱AI获取文本嵌入向量
    
    Args:
        text: 要获取嵌入的文本
        model: 嵌入模型名称
        
    Returns:
        嵌入向量列表
    """
    return ai_manager.get_embedding(text, model)
