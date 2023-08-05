# 悟空python sdk 使用

这是优必选 alphamini 机器人 python sdk.

## 修改历史

|Version |Contributor| Date| Change Log|
|----|:---|:---|:---|
|v1.0|彭钉|20/06/09|1.文档init|
|v1.1|彭钉|20/06/11|1.重命名包名|


## 一. 安装环境

### 1.1 下载并安装python 

* > 下载地址: https://www.python.org/downloads/windows/

    * ![](https://github.com/marklogg/images/blob/master/1586771644743.jpeg?raw=true)

* > windows系统, 安装时默认勾选 "配置环境变量"

* > Linux/Unix系统, 参考 https://wiki.python.org/moin/BeginnersGuide/Download 下载安装介绍

* > 验证安装
  * > python --version & pip --version 
  * ![](https://github.com/marklogg/images/blob/master/15917037872928.png?raw=true)

### 1.2 安装/卸载alphamini sdk

* > pip install alphamini 
* > pip uninstall alphamini
  
### 1.3 安装pyCharm 

* > 下载地址: https://www.jetbrains.com/pycharm/download/
    * ![](https://github.com/marklogg/images/blob/master/1591690731543.png?raw=true)
    * > 建议安装Professional,但是需要激活


### 1.4 准备一台悟空教育版机器人

* > 版本号>=1.3.0

* > 给机器人配上网,确保机器人和PC在同一个局域网内 


### 1.5 下载demo并运行

* > 下载地址: xxxxx
* > 将demo导入pycharm, 结构如下
  * ![](https://github.com/marklogg/images/blob/master/15916910712019.png?raw=true)
  * 选中文件,右键运行 "Run xxx.py"
  
## 二. API介绍

### 2.1 扫描与连接--公共接口

* > 导入包 :
    ```python  
    import mini.mini_sdk as MiniSdk
    ```

#### 2.1.1. 扫描局域网内机器人-(异步方法)

```python
 
  # 搜索指定序列号(在机器人屁股后面)的机器人,可以只输入序列号尾部字符即可,长度任意, 建议5个字符以上可以准确匹配,10秒超时
  # 搜索的结果WiFiDevice, 包含机器人名称,ip,port等信息
  async def test_get_device_by_name():  
    result: WiFiDevice = await MiniSdk.get_device_by_name("00018", 10) 
    print(f"test_get_device_by_name result:{result}")
    return result

  # 搜索指定序列号(在机器人屁股后面)的机器人,
  async def test_get_device_list():
    results = await MiniSdk.get_device_list(10)
    print(f"test_get_device_list results = {results}")
    return results  
```

#### 2.1.2. 连接机器人-(异步方法)
根据扫描到的机器人结果,调用MiniSdk.connect可连接机器人
```python

# MiniSdk.connect 返回值为bool, 这里忽略返回值
async def test_connect(dev: WiFiDevice):
    await MiniSdk.connect(dev)

```

#### 2.1.3. 让机器人进入编程模式-(异步方法)
机器人进入编程模式,可防止机器人在执行命令时被其他技能中断
```python
# 进入编程模式,机器人有个tts播报,这里通过asyncio.sleep 让当前协程等6秒返回,让机器人播完 
async def test_start_run_program():
    await StartRunProgram().execute()
    await asyncio.sleep(6)

```

#### 2.1.4. 断开连接并释放资源-(异步方法)
```python
async def shutdown():
    await asyncio.sleep(1)
    await MiniSdk.release()
```

#### 2.1.5. sdk日志开关
```python
# 默认的日志级别是Warning, 设置为INFO
MiniSdk.set_log_level(logging.INFO)
```

### 2.2 悟空API简介 

* > 导入api
    ```python
    from mini.apis import *
    ```
* > 每个api返回是个元组,元组第一个元素是bool类型,第二个元素是response(protobuf值), 如果第一个元素是False,则第二个元素是None值

* > 每个api有个execute()方法, 这是一个async方法, 触发执行
  
* > 每个api都有个is_serial参数,默认为True,表示接口可以串行执行, 可以await获取执行结果, is_serial=False,表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回

#### 2.2.1 声音控制

```python

# 测试text合成声音
async def test_play_tts():
    # is_serial:串行执行
    # text:要合成的文本
    # control_type: TTSControlType.START: 播放tts; TTSCOntrolType.STOP: 停止tts 
    block: PlayTTS = PlayTTS(is_serial=True, text="你好， 我是悟空， 啦啦啦", control_type=TTSControlType.START)

    # 返回元组, response是个ControlTTSResponse
    (resultType, response) = await block.execute()

    # print response
    print(f'test_play_tts result: {response}')
    # PlayTTS block的response包含resultCode和isSuccess
    # 如果resultCode !=0 可以通过errors.get_speech_error_str(response.resultCode)) 查询错误描述信息
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

# 测试播放在线音效
async def test_play_audio():
    # 播放在线音效, url表示要播放的音效列表 
    block: PlayAudio = PlayAudio(
        url=["http://yun.lnpan.com/music/download/ring/000/075/5653bae83917a892589b372782175dd8.amr"])

    # response是个PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

# 测试获取机器人的音效资源
async def test_get_audio_list():
    #audio_type: AudioType.INNER 是指机器人内置的不可修改的音效, AudioType.CUSTOM 是放置在sdcard/customize/music目录下可别开发者修改的音效
    block: FetchAudioList = FetchAudioList(audio_type=AudioType.INNER)

    # response是个GetAudioListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_audio_list result: {response}')

# 测试停止正在播放的声音
async def test_stop_audio():
    #设置is_serial=False, 表示只需将指令发送给机器人,await不需要等机器人执行完结果再返回
    block: PlayTTS = PlayTTS(is_serial=False, text="你让我说，让我说，不要打断我，不要打断我，不要打断我")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(2)

    #停止所有声音
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

# 测试播放一首音乐
async def test_play_online_music():
    #播放qq音乐, 需要在手机端授权
    block: PlayOnlineMusic = PlayOnlineMusic(name='我的世界')

    # response:MusicResponse
    (resultType, response) = await block.execute()

    print(f'test_play_online_music result: {response}')

```
#### 2.2.2 红外/视觉/摄像头等传感器接口

* > 通过这些传感器接口,获取一次传感器结果

```python
# 测试人脸侦测
async def test_face_detect():
    #timeout: 指定侦测时长
    block: FaceDetect = FaceDetect(timeout=10)

    # response: FaceDetectResponse
    (resultType, response) = await block.execute()

    print(f'test_face_detect result: {response}')

# 测试人脸分析
async def test_face_analysis():
    block: FaceAnalysis = FaceAnalysis(timeout=10)
    # response: FaceAnalyzeResponse
    (resultType, response) = await block.execute()

    print(f'test_face_analysis result: {response}')

# 测试物体识别
async def test_object_Recognise():
    #object_type: 支持FLOWER, FRUIT, GESTURE 三类物体
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FLOWER, timeout=10)
    #response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_Recognise result: {response}')

# 测试拍照
async def test_take_picture():
    #response: TakePictureResponse
    #take_picture_type: IMMEDIATELY-立即拍照, FINDFACE-找到人脸再拍照 两种拍照效果
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.IMMEDIATELY).execute()

    print(f'test_take_picture result: {response}')

# 测试人脸识别
async def test_face_recognise():
    #response : FaceRecogniseResponse
    (resultType, response) = await FaceRecognise(timeout=10).execute()

    print(f'test_face_recognise result: {response}')

# 测试获取红外探测距离
async def test_get_infrared_distance():
    #response: GetInfraredDistanceResponse
    (resultType, response) = await GetInfraredDistance().execute()

    print(f'test_get_infrared_distance result: {response}')

# 测试获取目前机器人内注册的人脸个数
async def test_get_register_faces():
    # reponse : GetRegisterFacesResponse
    (resultType, response) = await GetRegisterFaces().execute()

    print(f'test_get_register_faces result: {response}')
```

#### 2.2.3 机器人表现力

```python
# 测试让眼睛演示个表情
async def test_play_expression():
    # express_type: INNER 是指机器人内置的不可修改的表情动画, CUSTOM 是放置在sdcard/customize/expresss目录下可被开发者修改的表情
    block: PlayExpression = PlayExpression(express_name="codemao1", express_type=RobotExpressionType.INNER)
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')

# 测试, 让机器人跳舞/停止跳舞
async def test_control_behavior():
    #control_type: START, STOP
    block: ControlBehavior = ControlBehavior(name="dance_0004", control_type=RobotBehaviorControlType.START)
    #response ControlBehaviorResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

# 测试, 设置嘴巴灯颜色
async def test_set_mouth_lamp():
    #color: 支持RED,GREEN,BLUE三种颜色
    #mode: 0,1
    #duration:-1
    #breath_duration: 
    block: SetMouthLamp = SetMouthLamp(color=MouthLampColor.GREEN, model=0, duration=-1, breath_duration=1000)
    #response:SetMouthLampResponse
    (resultType, response) = await block.execute()

    print(f'test_set_mouth_lamp result: {response}')

# 测试,开关嘴巴灯
async def test_control_mouth_lamp():
    # is_open: True,False
    # response :ControlMouthResponse
    (resultType, response) = await ControlMouthLamp(is_open=True).execute()

    print(f'test_control_mouth_lamp result: {response}')
```

#### 2.2.4 第三方内容接口
* > 查询百科, 翻译 
```python
# 测试, 查询wiki
async def test_query_wiki():
    #query:查询关键字
    block: QueryWiKi = QueryWiKi(query='优必选')
    # response : WikiResponse
    (resultType, response) = await block.execute()

    print(f'test_query_wiki result: {response}')

# 测试翻译接口
async def test_start_translate():
    # query:
    # from_lan: 源语言
    # to_lan: 目标语言
    # platform: BAIDU, GOOGLE, TENCENT
    block: StartTranslate = StartTranslate(query="张学友", from_lan=CN, to_lan=EN)
    # response: TranslateResponse
    (resultType, response) = await block.execute()

    print(f'test_start_translate result: {response}')
```

#### 2.2.5 运动控制
```python
# 测试, 执行一个动作文件
async def test_play_action():
    #action_name: 动作文件名, 可以通过GetActionList获取机器人支持的动作
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

# 测试, 控制机器人,向前/后/左/右 移动
async def test_move_robot():
    # step: 移动几步
    # direction: 方向,枚举类型
    block: MoveRobot = MoveRobot(step=10, direction=MoveRobotDirection.LEFTWARD)
    #response : MoveRobotResponse
    (resultType, response) = await block.execute()
    print(f'test_move_robot result:{response}')

# 测试, 获取支持的动作文件列表
async def test_get_action_list():
    # action_type: INNER 是指机器人内置的不可修改的动作文件, CUSTOM 是放置在sdcard/customize/action目录下可被开发者修改的动作
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    #response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

# 测试, 改变机器人的音量
async def test_change_robot_volume():
    #volume: 0~1.0
    block: ChangeRobotVolume = ChangeRobotVolume(volume=0.5)
    #response:ChangeRobotVolumeResponse
    (resultType, response) = await block.execute()

    print(f'test_change_robot_volume result:{response}')
```

#### 2.2.6 事件监听类接口

##### 2.2.6.1 触摸监听
```python
# 测试, 触摸监听
async def test_ObserveHeadRacket():
    # 创建监听
    observer: ObserveHeadRacket = ObserveHeadRacket()

    # 事件处理器
    # ObserveHeadRacketResponse.type:
    # @enum.unique
    # class HeadRacketType(enum.Enum):
    #     SINGLE_CLICK = 1  # 单击
    #     LONG_PRESS = 2  # 长按
    #     DOUBLE_CLICK = 3  # 双击
    def handler(msg: ObserveHeadRacketResponse):
        # 监听到一个事件后,停止监听,
        observer.stop()
        print("{0}".format(str(msg.type)))
        # 执行个舞动
        asyncio.create_task(__dance())

    observer.set_handler(handler)
    #启动
    observer.start()
    await asyncio.sleep(0)


async def __dance():
    await ControlBehavior(name="dance_0002").execute()
    # 结束event_loop
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

# 程序入口
if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveHeadRacket())
        asyncio.get_event_loop().run_forever() # 定义了事件监听对象,必须让event_loop.run_forver
        asyncio.get_event_loop().run_until_complete(shutdown())
```

##### 2.2.6.2 语音识别监听
```python
async def __tts():
    block: PlayTTS = PlayTTS(text="你好， 我是悟空， 啦里啦，啦里啦")
    response = await block.execute()
    print(f'tes_play_tts: {response}')

# 测试监听语音识别
async def test_speech_recognise():
    # 语音监听对象
    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

    # 处理器
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):
        print(f'=======handle speech recognise:{msg}')
        print("{0}".format(str(msg.text)))
        if str(msg.text) == "悟空":
            #监听到"悟空", tts打个招呼
            asyncio.create_task(__tts())

        elif str(msg.text) == "结束":
            #监听到结束, 停止监听
            observe.stop()
            #结束event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    #启动
    observe.start()
    await asyncio.sleep(0)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_speech_recognise())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
```

##### 2.2.6.3 红外监听
```python
async def test_ObserveInfraredDistance():
    #红外监听对象
    observer: ObserveInfraredDistance = ObserveInfraredDistance()

    # 定义处理器
    # ObserveInfraredDistanceResponse.distance
    def handler(msg: ObserveInfraredDistanceResponse):
        print("distance = {0}".format(str(msg.distance)))
        if msg.distance < 500:
            observer.stop()
            asyncio.create_task(__tts())

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts():
    result = await PlayTTS(text="是不是有人在啊， 你是谁啊").execute()
    print(f"tts over {result}")
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveInfraredDistance())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
```

##### 2.2.6.4 人脸识别/检测监听
```python
#测试, 检测到注册的人脸,则上报事件, 如果陌生人,返回"stranger"
async def test_ObserveFaceRecognise():
    observer: ObserveFaceRecognise = ObserveFaceRecognise()

    
    # FaceRecogniseTaskResponse.faceInfos: [FaceInfoResponse]
    # FaceInfoResponse.id, FaceInfoResponse.name,FaceInfoResponse.gender,FaceInfoResponse.age
    # FaceRecogniseTaskResponse.isSuccess
    # FaceRecogniseTaskResponse.resultCode
    def handler(msg: FaceRecogniseTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.faceInfos:
            observer.stop()
            asyncio.create_task(__tts(msg.faceInfos[0].name))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(name):
    await PlayTTS(text=f'你好， {name}').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

# 人脸检测,检测到人脸,则上报事件
async def test_ObserveFaceDetect():
    observer: ObserveFaceDetect = ObserveFaceDetect()

    # FaceDetectTaskResponse.count
    # FaceDetectTaskResponse.isSuccess
    # FaceDetectTaskResponse.resultCode
    def handler(msg: FaceDetectTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.count:
            observer.stop()
            asyncio.create_task(__tts(msg.count))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(count):
    await PlayTTS(text=f'在我面前好像有{count}个人').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)    
```

##### 2.2.6.5 姿态检测监听
```python
# 测试,姿态检测
async def test_ObserveRobotPosture():
    #创建监听对象
    observer: ObserveRobotPosture = ObserveRobotPosture()
    # 事件处理器
    # ObserveFallClimbResponse.status
    #     STAND = 1; //站立
    #     SPLITS_LEFT = 2; //左劈叉
    #     SPLITS_RIGHT = 3; //右劈叉
    #     SITDOWN = 4; //坐下
    #     SQUATDOWN = 5; //蹲下
    #     KNEELING = 6; //跪下
    #     LYING = 7; //侧躺
    #     LYINGDOWN = 8; //平躺
    #     SPLITS_LEFT_1 = 9; //左劈叉1
    #     SPLITS_RIGHT_2 = 10;//右劈叉2
    #     BEND = 11;//弯腰
    def handler(msg: ObserveFallClimbResponse):
        print("{0}".format(msg))
        if msg.status == 8 or msg.status == 7:
            observer.stop()
            asyncio.create_task(__tts())

    observer.set_handler(handler)
    #start
    observer.start()
    await asyncio.sleep(0)


async def __tts():
    await PlayTTS(text="我摔倒了").execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


if __name__ == '__main__':
    device: WiFiDevice = asyncio.get_event_loop().run_until_complete(test_get_device_by_name())
    if device:
        asyncio.get_event_loop().run_until_complete(test_connect(device))
        asyncio.get_event_loop().run_until_complete(test_start_run_program())
        asyncio.get_event_loop().run_until_complete(test_ObserveRobotPosture())
        asyncio.get_event_loop().run_forever()
        asyncio.get_event_loop().run_until_complete(shutdown())
```
