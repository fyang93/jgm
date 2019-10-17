import os
import base64
import logging
from PIL import Image


actions = []
device_info = {"screenWidth": 1600, "screenHeight": 2455, "screenDpi": 2.5}
goods_positions = [{"type": "location", "x": "58%", "y": "91%"},
                   {"type": "location", "x": "72%", "y": "85%"},
                   {"type": "location", "x": "86%", "y": "79%"}]
goods_ranges = ["54.812504% 84.92872% 67.8125% 93.116066%",
                "67.1875% 81.222% 80.1875% 89.40937%",
                "81.15625% 76.98574% 91.90625% 83.910385%"]
building_positions = {1: {"type": "location", "x": "29%", "y": "37%", "xOffset": "-10dp", "yOffset": "10dp"},
                      2: {"type": "location", "x": "51%", "y": "30%"},
                      3: {"type": "location", "x": "73%", "y": "23%", "xOffset": "10dp", "yOffset": "10dp"},
                      4: {"type": "location", "x": "29%", "y": "50%", "xOffset": "-10dp", "yOffset": "10dp"},
                      5: {"type": "location", "x": "51%", "y": "43%"},
                      6: {"type": "location", "x": "73%", "y": "36%", "xOffset": "10dp", "yOffset": "10dp"},
                      7: {"type": "location", "x": "29%", "y": "65%", "xOffset": "-10dp", "yOffset": "10dp"},
                      8: {"type": "location", "x": "51%", "y": "58%"},
                      9: {"type": "location", "x": "73%", "y": "51%", "xOffset": "10dp", "yOffset": "10dp"}}
other_positions = {'edit': {"type": "location", "x": "93%", "y": "61%"},
                   'level_up': {"type": "location", "x": "77%", "y": "96%"},
                   'ok': {"type": "location", "x": "50%", "y": "78%"},
                   'home': {"type": "location", "x": "18%", "y": "98%"}}

settings = {'纺织厂': 1, '食品厂': 2, '电厂': 3,
            '便利店': 4, '服装店': 5, '菜市场': 6,
            '居民楼': 7, '人才公寓': 8, '中式小楼': 9}

def get_img_size(path):
    with Image.open(path) as img:
        w, h = img.size
    return w, h


def img_to_base64(path):
    with open(path, 'rb') as img:
        encoded = base64.b64encode(img.read())
        encoded = str(encoded, encoding='utf-8')
    escaped = encoded.replace("/", "\\/")
    return escaped


def collect_goods(duration=1000, delay=0):
    imgs = os.listdir("imgs")
    for filename in imgs:
        building = os.path.splitext(filename)[0]
        if building not in settings.keys():
            continue
        path = os.path.join("imgs", filename)
        w, h = get_img_size(path)
        data = img_to_base64(path)
        end = building_positions[settings[building]]
        for start, area in zip(goods_positions, goods_ranges):
            img_data = {"data": data, "imageWidth": w, "imageHeight": h}
            img_data.update(device_info)
            condition = {"type": "image", "imageData": img_data,
                         "limitArea": area, "searchMode": "COLOR", "minSimilarPercent": 70, "codeVersion": "V1_7"}
            action = {"type": "滑动", "duration": duration, "delay": delay, "defaultUnit": 0,
                      "repeatCount": 1, "condition": condition, "startPos": start, "endPos": end}
            actions.append(str(action))


def collect_coins(i_start, i_end, repeats=1, duration=500, delay=10):
    start = building_positions[i_start]
    end = building_positions[i_end]
    action = {"type": "滑动", "duration": duration, "delay": delay, "defaultUnit": 0,
              "repeatCount": repeats, "startPos": start, "endPos": end}
    actions.append(str(action))


def level_up(i, duration=50, delay=100):
    action = {"type": "点击", "duration": duration,
              "delay": delay, "defaultUnit": 0, "posData": other_positions['edit']}
    actions.append(str(action))
    action = {"type": "点击", "duration": duration,
              "delay": delay, "defaultUnit": 0, "posData": building_positions[i]}
    actions.append(str(action))
    action = {"type": "点击", "duration": duration,
              "delay": delay, "defaultUnit": 0, "posData": other_positions['level_up']}
    actions.append(str(action))
    action = {"type": "点击", "duration": duration,
              "delay": delay, "defaultUnit": 0, "posData": other_positions['edit']}
    actions.append(str(action))


def jump_to_top_by_chance(chance):
    condition = {"type": "random", "percent": chance}
    action = {"type": "控制执行", "delay": 0, "delayUnit": 0, "condition": condition,
              "controlRunType": "jumpTo", "jumpToPosition": "1"}
    actions.append(str(action))


def jump_to_top_for_train():
    w, h = get_img_size('train.png')
    data = img_to_base64('train.png')
    img_data = {"data": data, "imageWidth": w, "imageHeight": h}
    img_data.update(device_info)
    condition = {"type": "image", "imageData": img_data,
                 "limitArea": "44.0625% 89.4501% 58.5625% 94.09369%",
                 "searchMode": "COLOR", "minSimilarPercent": 70, "codeVersion": "V1_7"}
    action = {"type": "控制执行", "delay": 0, "delayUnit": 0, "condition": condition,
              "controlRunType": "jumpTo", "jumpToPosition": "1"}
    actions.append(str(action))


def close_dialog():
    w, h = get_img_size('ok.png')
    data = img_to_base64('ok.png')
    img_data = {"data": data, "imageWidth": w, "imageHeight": h}
    img_data.update(device_info)
    condition = {"type": "image", "imageData": img_data,
                 "limitArea": "43.751415% 75.76282% 55.376415% 80.447136%",
                 "searchMode": "COLOR", "minSimilarPercent": 70, "codeVersion": "V1_7"}
    action = {"type": "点击", "duration": 50, "delay": 100, "defaultUnit": 0,
              "posData": other_positions['ok'], "condition": condition}
    actions.append(action)


def back_to_home():
    action = {"type": "点击", "duration": 50,
              "delay": 100, "defaultUnit": 0, "posData": other_positions['home']}
    actions.append(str(action))

logger = logging.getLogger()
fh = logging.FileHandler('script.zjs', mode='w')
logger.setLevel(logging.INFO)
logger.addHandler(fh)

# --- actions ---
back_to_home()              # 回到首页
collect_goods()             # 收货
jump_to_top_for_train()     # 检查列车是否开走
close_dialog()              # 关闭对话框
collect_coins(7, 9, 4)      # 收集住宅金币x4
collect_coins(4, 6)         # 收集商业金币x1
collect_coins(7, 9, 4)      # 收集住宅金币x4
collect_coins(4, 6)         # 收集商业金币x1
collect_coins(1, 3)         # 收集工业金币x1
jump_to_top_by_chance(80)   # 以20%概率升级建筑
level_up(1)                 # 升级建筑
# ---------------

header = {"repeatCount": 0, "pauseOnFail": False,
          "count": len(actions), "description": "", "minVerCode": 1}
header.update(device_info)
header = str(header)

logger.info(header)
for action in actions:
    logger.info(action)
