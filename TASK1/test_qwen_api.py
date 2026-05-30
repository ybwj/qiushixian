import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    # 1. 读取当前目录下的 .env 文件
    load_dotenv()

    # 2. 从环境变量中读取 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")

    # 3. 检查 API Key 是否存在
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY is not set. Please check your .env file.")

    # 4. 创建阿里云百炼 OpenAI 兼容客户端
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 5. 调用 qwen-plus
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "请回复：Qwen-Plus API test successful."}
        ],
        temperature=0
    )

    # 6. 打印模型返回内容
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()