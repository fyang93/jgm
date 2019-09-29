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
                "67.1875% 81.222% 80.1875% 89.40937%"]
building_positions = {1: {"type": "location", "x": "29%", "y": "37%", "xOffset": "-10-0dp", "yOffset": "-10-0dp"},
                      2: {"type": "location", "x": "51%", "y": "30%", "xOffset": "-10-10dp", "yOffset": "-10-10dp"},
                      3: {"type": "location", "x": "73%", "y": "23%", "xOffset": "0-10dp", "yOffset": "0-10dp"},
                      4: {"type": "location", "x": "29%", "y": "50%", "xOffset": "-10-0dp", "yOffset": "-10-0dp"},
                      5: {"type": "location", "x": "51%", "y": "43%", "xOffset": "-10-10dp", "yOffset": "-10-10dp"},
                      6: {"type": "location", "x": "73%", "y": "36%", "xOffset": "0-10dp", "yOffset": "0-10dp"},
                      7: {"type": "location", "x": "29%", "y": "65%", "xOffset": "-10-0dp", "yOffset": "-10-0dp"},
                      8: {"type": "location", "x": "51%", "y": "58%", "xOffset": "-10-10dp", "yOffset": "-10-10dp"},
                      9: {"type": "location", "x": "73%", "y": "51%", "xOffset": "0-10dp", "yOffset": "0-10dp"}}
other_positions = {'edit': {"type": "location", "x": "93%", "y": "61%"},
                   'level_up': {"type": "location", "x": "77%", "y": "96%"}}

# genres = {'木材厂': '工业', '食品厂': '工业', '造纸厂': '工业', '电厂': '工业', '钢铁厂': '工业', '水厂': '工业', '企鹅机械': '工业', '纺织厂': '工业', '零件厂': '工业', '人民石油': '工业',
#           '便利店': '商业', '学校': '商业', '菜市场': '商业', '服装店': '商业', '五金店': '商业', '图书城': '商业', '商贸中心': '商业', '加油站': '商业', '民食斋': '商业', '媒体之声': '商业',
#           '木屋': '住宅', '居民楼': '住宅', '平房': '住宅', '钢结构房': '住宅', '小型公寓': '住宅', '人才公寓': '住宅', '花园洋房': '住宅', '中式小楼': '住宅', '空中别墅': '住宅', '复兴公馆': '住宅'}
settings = {'木材厂': 1, '食品厂': 2, '电厂': 3,
            '便利店': 4, '菜市场': 5, '五金店': 6,
            '小型公寓': 7, '居民楼': 8, '平房': 9}
num_goods = {'木材厂': '4', '食品厂': '4', '造纸厂': '4', '电厂': '4', '钢铁厂': '4', '水厂': '4', '企鹅机械': '4', '纺织厂': '4', '零件厂': '4', '人民石油': '4', '木屋': '4', '居民楼': '4', '平房': '4', '钢结构房': '4', '小型公寓': '4',
             '人才公寓': '4', '花园洋房': '4', '中式小楼': '4', '空中别墅': '4', '复兴公馆': '4', '便利店': '4', '学校': '4', '菜市场': '4', '服装店': '4', '五金店': '4', '图书城': '4', '商贸中心': '4', '加油站': '4', '民食斋': '4', '媒体之声': '4'}


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


def collect_goods(duration=500, delay=10):
    imgs = os.listdir("imgs")
    for filename in imgs:
        building = os.path.splitext(filename)[0]
        if building not in settings.keys():
            continue
        path = os.path.join("imgs", filename)
        w, h = get_img_size(path)
        data = img_to_base64(path)
        repeats = num_goods[building]
        end = building_positions[settings[building]]
        for start, area in zip(goods_positions, goods_ranges):
            img_data = {"data": data, "imageWidth": w, "imageHeight": h}
            img_data.update(device_info)
            condition = {"type": "image", "imageData": img_data,
                         "limitArea": area, "searchMode": "COLOR", "minSimilarPercent": 70, "codeVersion": "V1_7"}
            action = {"type": "滑动", "duration": duration, "delay": delay, "defaultUnit": 0,
                      "repeatCount": repeats, "condition": condition, "startPos": start, "endPos": end}
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


def jump_to_top(chance):
    condition = {"type": "random", "percent": chance}
    action = {"type": "控制执行", "delay": 0, "delayUnit": 0, "condition": condition,
              "controlRunType": "jumpTo", "jumpToPosition": "1"}
    actions.append(str(action))


logger = logging.getLogger()
fh = logging.FileHandler('script.zjs', mode='w')
logger.setLevel(logging.INFO)
logger.addHandler(fh)

# --- actions ---
# collect_goods()         # 收货
collect_coins(7, 9, 4)  # 收集住宅金币x4
collect_coins(4, 6)     # 收集商业金币x1
collect_coins(7, 9, 4)  # 收集住宅金币x4
collect_coins(4, 6)     # 收集商业金币x1
collect_coins(1, 3)     # 收集工业金币x1
jump_to_top(80)         # 以20%概率升级建筑
level_up(1)             # 升级建筑
# ---------------

header = {"repeatCount": 0, "pauseOnFail": False,
          "count": len(actions), "description": "", "minVerCode": 1}
header.update(device_info)
header = str(header)

logger.info(header)
for action in actions:
    logger.info(action)
