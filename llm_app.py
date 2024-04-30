import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# 加载环境变量
load_dotenv()

# 配置 API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# 设定提示模板，增加更具体的指示以提高生成内容的质量和相关性
prompt_template = """
You are an expert chef with extensive experience in using a wide range of ingredients to prepare exquisite dishes.

Please take the following ingredients provided by the user and suggest a dish. Include a brief description of the dish, followed by detailed step-by-step cooking instructions.

use more emojis to make the dish more appealing to the user.
be more brief and concise in your response.
Ingredients:
- {formatted_ingredients}

Your response should be engaging, clear, and precise, suitable for someone cooking at home.
"""

def format_ingredients(ingredients):
    # 格式化输入的食材列表为更适合提示的格式
    ingredients_list = ingredients.split(',')
    formatted_list = '\n- '.join([ingredient.strip().capitalize() for ingredient in ingredients_list])
    return formatted_list

def generate_content(ingredients):
    formatted_ingredients = format_ingredients(ingredients)
    prompt = prompt_template.format(formatted_ingredients=formatted_ingredients)
    response = model.generate_content(prompt)
    return response.text

# 设置 Streamlit 页面
st.title("🍽️ AI Cooking Assistant")

# 创建文本区域让用户输入食材
ingredients = st.text_area("Enter the ingredients you have (separated by commas):")
if st.button("Suggest a dish!"):
    reply = generate_content(ingredients)
    st.write(reply)
