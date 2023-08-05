COMMON = (
    (400, "悟空忙碌中，请稍后再试"),
    (401, "悟空忙碌中，请稍后再试"),
    (403, "悟空忙碌中，请稍后再试"),
    (404, "系统错误，请升级系统"),
    (408, "悟空忙碌中，请稍后再试"),
    (409, "悟空忙碌中，请稍后再试"),
    (500, "悟空忙碌中，请稍后再试"),
    (501, "系统错误，请升级系统"),
    (504, "系统错误，请升级系统"),
    (1006, "系统错误，请升级系统"),
    (1007, "系统错误，请升级系统"),
    (-61, "该账户已欠费"),
    (-64, "该账户已冻结"),
    (-81, "已开启隐私模式，无法使用该功能"),
    (-92, "已开启隐私模式，无法使用该功能"),
    (-1, "机器人站起失败"),
)

SPEECH = (
    (1, "悟空忙碌中，请稍后再试"),
    (2, "网络错误，请稍后再试"),
    (-1, "TTS内容为空，合成失败"),
    (4404, "播放失败，音频资源已失效"),
    (4400, "音频为空，请选择音效"),
    (4408, "网络错误，请稍后再试"),
    (4500, "网络错误，请稍后再试"),
    (4200, ""),
)

CONTENT = (
    (4404, "悟空忙碌中，请稍后再试"),
    (4400, "网络错误，请稍后再试"),
    (4408, "TTS内容为空，合成失败"),
    (4500, "播放失败，音频资源已失效"),
    (4200, "音频为空，请选择音效"),
)

VISION = (
    (1, "为检测到人脸，请看着悟空的眼睛，不要晃动"),
    (2, "你已经录入过人脸信息"),
    (3, "人脸信息数量已达到上限，请在APP悟空好友中删除人脸后再试"),
    (4, "人脸信息数量已达到上限，请在APP悟空好友中删除人脸后再试"),
    (5, "悟空正在录入人脸信息，请稍后再试"),
    (6, "检测到的人脸过多，请稍后再试"),
    (7, "人脸录入被打断，请稍后再试"),
    (8, "悟空电量低，无法添加新的好友"),
    (9, "网络错误，请稍后再试"),
    (10, "悟空忙碌中，请稍后再试"),
    (11, "悟空正在绘本阅读，请稍后再试"),
    (12, "悟空正处于监控中，请稍后再试"),
    (13, "悟空正在通话中，请稍后再试"),
    (1700, "网络错误，请稍后再试"),
    (2504, "摄像头启动失败，请重试一下"),
    (2505, "摄像头好像被遮挡了，请移开遮挡物再试试"),
    (1600, "识别超时"),
)

MOTION = (
    (1, "悟空忙碌中，请稍后再试"),
    (2, "悟空忙碌中，请稍后再试"),
    (10002, "机器人舵机出现故障"),
    (10003, "机器人舵机自我保护"),
    (10005, "缺少文件，请升级系统"),
    (10006, "数据异常，请升级系统"),
    (10007, "数据异常，请升级系统"),
    (10008, "数据异常，请升级系统"),
    (10009, "数据异常，请升级系统"),
    (10090, "动作正在下载中，请稍后再试"),
    (10004, "执行新动作被中断"),
    (10001, "动作stop中断"),
)

EXPRESS = (
    (10001, "动作stop中断"),
    (10002, "机器人舵机出现故障"),
    (10003, "机器人舵机自我保护"),
    (10004, "执行新动作被中断"),
    (10005, "缺少文件，请升级系统"),
    (10006, "数据异常，请升级系统"),
    (10007, "数据异常，请升级系统"),
    (10008, "数据异常，请升级系统"),
    (10009, "数据异常，请升级系统"),

    (10090, "动作正在下载中，请稍后再试"),

    (1001, "缺少文件，请升级系统"),
    (1002, "缺少文件，请升级系统"),
    (1003, "数据异常，请升级系统"),
    (1004, "数据异常，请升级系统"),
    (1005, "数据异常，请升级系统"),
    (1007, "悟空忙碌中，请稍后再试"),
    (1008, "数据异常，请升级系统"),
)


def get_common_error_str(error_code: int) -> str:
    if error_code == 0:
        return ""

    ret: str = "未知错误"
    for t in COMMON:
        if t[0] == error_code:
            ret = t[1]
            break
    return ret


def get_speech_error_str(error_code: int) -> str:
    ret = None
    for t in SPEECH:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_content_error_str(error_code: int) -> str:
    ret = None
    for t in CONTENT:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_vision_error_str(error_code: int) -> str:
    ret = None
    for t in VISION:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_motion_error_str(error_code: int) -> str:
    ret = None
    for t in MOTION:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)


def get_express_error_str(error_code: int) -> str:
    ret = None
    for t in EXPRESS:
        if t[0] == error_code:
            ret = t[1]
            break
    if ret:
        return ret
    else:
        return get_common_error_str(error_code)
