"""
天气技能模块

使用和风天气 API 获取城市天气信息
"""

import requests
from config import QWEATHER_API_KEY


def get_weather(city: str) -> str:
    """
    使用和风天气 API 获取城市天气信息
    
    Args:
        city: 城市名称，如 "北京"
    
    Returns:
        天气信息描述
    """
    if not QWEATHER_API_KEY:
        return "错误: 未配置 QWEATHER_API_KEY，请在环境变量中设置"
    
    try:
        geo_url = "https://geoapi.qweather.com/v2/city/lookup"
        geo_params = {"location": city, "key": QWEATHER_API_KEY}
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()
        
        if geo_data.get("code") != "200":
            return f"未找到城市 '{city}'，请检查城市名称"
        
        location_id = geo_data["location"][0]["id"]
        location_name = geo_data["location"][0]["name"]
        
        weather_url = "https://devapi.qweather.com/v7/weather/now"
        weather_params = {"location": location_id, "key": QWEATHER_API_KEY}
        weather_response = requests.get(weather_url, params=weather_params, timeout=10)
        weather_data = weather_response.json()
        
        if weather_data.get("code") != "200":
            return f"获取天气信息失败"
        
        now = weather_data["now"]
        
        result = f"""{location_name} 当前天气:
天气: {now['text']}
温度: {now['temp']}°C
体感温度: {now['feelsLike']}°C
风向: {now['windDir']} {now['windScale']}级
湿度: {now['humidity']}%
能见度: {now['vis']}公里
更新时间: {weather_data['updateTime']}"""
        
        return result
    
    except requests.exceptions.RequestException as e:
        return f"获取天气出错: {str(e)}"


SKILL_INFO = {
    "name": "get_weather",
    "description": "获取指定城市的实时天气信息",
    "args": {"city": "城市名称"},
    "example": '{"city": "北京"}'
}
