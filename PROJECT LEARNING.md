# Project概要
- OpenCV・Python 运用人体细微的面部方向以及眼神方向，从心理学以及逻辑学来推测接下来可能做出的行为，与已经做出的行为。


# 正确识别面向
## 创建环境
- 在本次项目中我们用到了Multi-task CNN 和 Open CV的DNN模型
- 我们分别使用了Tensorflow和mediapipe来识别脸部旋转方向，最终目的都是相同的，由于Pytorch能在后续中运用，所以着重在Tensorflow上，mediapipe作为Google本身已经完成基础训练的模型，很容易便可以达成。

MEDIEPIPE ref:https://github.com/Mostafa-Nafie/Head-Pose-Estimation

### 软件背景
- MTCNN进行校准检测对齐
- DNN模型是基于SSD并使用ResNet-10架构为主干的Caffe模型，基于Tensorflow来引入，是目前来说较为准确模型之一，其训练模型已经包含在基础数据中。
### 安装OpenCV
- 在win+R中输入cmd指令，运用pip指令安装opencv最新版本
"pip install opencv–python" "pip install tensorflow"
- 运行python环境，确认可以正确导入cv2库
- 初始化模型，调整图片像素韦300x300
### CNN与Dlib的比较
- Dlib主要用于面部界标检测，提供了68个界标，但是没有提供较好的准确性
- Tensorflow CNN是在五个训练集上已经训练过的模型，具有更高的面部标志稳定性
### 面部方向
- 为了得到面部具体的方向，我们需要建立一个3D空间，将点转化为线，来尝试记录随着头运动，夹角的变化
- x，y两个轴将为脸部的旋转角度提供了可靠的依据
### 出现的问题
#### 代码输入错误
- 将github代码下载后，部分地址指令会出现错误，这是由于在GitHub上在本文件夹内搜索得到的文件，在电脑中有较长的前缀，文件也会跑到错误的文件夹。
- 解决方法：直接使用指令强制指向所需要的文件即可。
#### 版本不匹配
- 在运行过程中会出现（-2）的错误，显示open cv2的导入有问题，但是本身下载的软件导入无问题，这是可能是opencv-python的两个文件版本不匹配，如4.5版本与4.7版本。
- 解决方案：卸载两个文件并重新装载最新版，查询 pip list 确认版本一致，重启python即可解决。
### 感想
- 使用OpenCV-python，找到基础CNN模型来带入对我来说是一个崭新的尝试。本来希望直接用OpenCV软件来制作，发现现在大部分都是基于Python软件本身的应用，较少用OpenCV本身软件来制作，如果以后也想尝试运用OpenCV
- 对于机器学习已经拥有了好多不同框架，但是对于其不同框架有各自的偏好方向。

