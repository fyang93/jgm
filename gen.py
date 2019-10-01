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
                   'level_up': {"type": "location", "x": "77%", "y": "96%"}}

# genres = {'木材厂': '工业', '食品厂': '工业', '造纸厂': '工业', '电厂': '工业', '钢铁厂': '工业', '水厂': '工业', '企鹅机械': '工业', '纺织厂': '工业', '零件厂': '工业', '人民石油': '工业',
#           '便利店': '商业', '学校': '商业', '菜市场': '商业', '服装店': '商业', '五金店': '商业', '图书城': '商业', '商贸中心': '商业', '加油站': '商业', '民食斋': '商业', '媒体之声': '商业',
#           '木屋': '住宅', '居民楼': '住宅', '平房': '住宅', '钢结构房': '住宅', '小型公寓': '住宅', '人才公寓': '住宅', '花园洋房': '住宅', '中式小楼': '住宅', '空中别墅': '住宅', '复兴公馆': '住宅'}
settings = {'钢铁厂': 1, '食品厂': 2, '电厂': 3,
            '便利店': 4, '民食斋': 5, '菜市场': 6,
            '钢结构房': 7, '人才公寓': 8, '居民楼': 9}


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


def collect_goods(duration=1000, delay=10):
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


def level_up(i, duration=50, delay=10):
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


def jump_to_top_random(chance):
    condition = {"type": "random", "percent": chance}
    action = {"type": "控制执行", "delay": 0, "delayUnit": 0, "condition": condition,
              "controlRunType": "jumpTo", "jumpToPosition": "1"}
    actions.append(str(action))


def jump_to_top():
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


logger = logging.getLogger()
fh = logging.FileHandler('script.zjs', mode='w')
logger.setLevel(logging.INFO)
logger.addHandler(fh)

# --- actions ---
collect_goods()         # 收货
jump_to_top()           # 检查列车是否开走
collect_coins(7, 9, 4)  # 收集住宅金币x4
collect_coins(4, 6)     # 收集商业金币x1
collect_coins(7, 9, 4)  # 收集住宅金币x4
collect_coins(4, 6)     # 收集商业金币x1
collect_coins(1, 3)     # 收集工业金币x1
jump_to_top_random(80)  # 以20%概率升级建筑
level_up(1)             # 升级建筑
# ---------------

header = {"repeatCount": 0, "pauseOnFail": False,
          "count": len(actions), "description": "", "minVerCode": 1}
header.update(device_info)
header = str(header)

logger.info(header)
for action in actions:
    logger.info(action)
