# backend/ollama_client.py
import requests
import json

# 假设 Ollama 接口地址（注意：如果后端运行在容器内，需使用 host.docker.internal 访问主机上的 Ollama 服务）
OLLAMA_API_URL = "https://192.168.5.116:11434"

def generate_weapon(model: str, system_prompt: str):
    # 传统调用，不流式
    payload = {
        "model": model,
        "prompt": f"System: {system_prompt}\nUser: 请根据上述世界观生成一件符合要求的游戏武器，并严格以JSON格式输出。", 
        "format": "json",
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL+"/api/generate", json=payload)
    data = response.json()
    if "response" in data:
        try:
            weapon_data = json.loads(data["response"])
            return weapon_data
        except Exception as e:
            raise ValueError("解析生成结果时出错: " + str(e))
    else:
        raise ValueError("未返回生成内容")

def generate_weapon_stream(model: str, system_prompt: str):
    # 构建结构化prompt
    last_system_prompt = f"""
    【世界观设定】
    {system_prompt}
    【生成规则】
    {open("weapon_rules.txt","r",encoding="utf-8").read()}  # 你之前定义的武器生成规则
    """
    payload = {
        "model": model,
        "prompt": f"{last_system_prompt}\n\nUser: 请根据上述世界观生成一件符合要求的游戏武器，尽量保证随机性，同时保证风格，同时描述和背景尽量详细，并严格以JSON格式输出。",
        "format": "json",
        "options": {
                "temperature": 0.3,  # 降低随机性保证格式
                "max_tokens": 1000
            },
        "stream": True
    }
    response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
    accumulated = ""
    # 遍历每一行响应
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            # 移除可能存在的 "data:" 前缀，并去除首尾空格
            clean_line = decoded_line.replace("data:", "").strip()
            # 如果清理后的内容不为空，则累加并 yield 输出
            if clean_line:
                accumulated += clean_line
                yield clean_line + "\n"
    
    # 流式结束后，尝试解析累积的字符串为 JSON 数据
    try:
        weapon_data = json.loads(accumulated)
        yield "\n最终解析的 JSON 数据:\n"
        yield json.dumps(weapon_data, ensure_ascii=False, indent=2)
    except Exception as e:
        yield f"\nJSON解析错误: {e}\n"

def get_models():
    try:
        # 调用 Ollama 接口获取模型列表（请根据实际接口调整 URL 和返回数据结构）
        response = requests.get("https://ollama.silvericekey.top/api/models")
        data = response.json()
        # 假设返回数据格式为：{ "models": [ {"name": "deepseek-r1:1.5b"}, {"name": "deepseek-r1:8b"}, {"name": "deepseek-r1:14b"} ] }
        models_list = [{"label": m["name"], "value": m["name"]} for m in data.get("data", [])]
        if not models_list:
            raise ValueError("未获取到模型数据")
        return models_list
    except Exception as e:
        # 如果调用 Ollama 接口失败，则返回默认模型列表
        return [
            {"label": "1.5B", "value": "deepseek-r1:1.5b"},
            {"label": "8B", "value": "deepseek-r1:8b"},
            {"label": "14B", "value": "deepseek-r1:14b"}
        ]