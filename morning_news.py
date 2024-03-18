import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://dayu.qqsuu.cn/weiyujianbao/apis.php" 

@plugins.register(name="morning_news",
                  desc="获取早报",
                  version="1.0",
                  author="wyh",
                  desire_priority=100)
class morning_news(Plugin):
    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【早报】获取摸鱼日历"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        if self.content == "早报":
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.morning_news()
            if result != None:
                reply.type = ReplyType.IMAGE_URL if type(result) == str else ReplyType.IMAGE
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS

    def morning_news(self):
        url = BASE_URL_DM
        parameter = "type=json"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            response = requests.get(url, params=parameter,headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('code') == 200 and json_data['data']:
                    img_url = json_data['data']
                    logger.info(json_data)
                    return img_url
                else:
                    logger.info(json_data)
            else:
                logger.info(f"接口异常：{response.status_code}")
        except Exception as e:
            logger.error(f"接口异常：{e}")
                
        logger.error("所有接口都挂了,无法获取")
        return None
