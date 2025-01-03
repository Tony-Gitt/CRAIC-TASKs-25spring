# Kuavo选拔任务

> ***NOTE：kuavo赛道任务为小组任务，每个组内成员共同完成所有任务，任务成果提交一份即可，但请在提交仓库的readme文档中注明你们组内的任务分配情况***

## 1 基础知识了解
- 至少掌握aelos&roban组任务所需的全部技术栈
- ETH **Robot Dynamics Lecture Note**
- 阅读A Unified MPC Framework for Whole-Body Dynamic Locomotion and Manipulation，了解MPC&WBC控制框架基本原理 [Link](https://arxiv.org/abs/2103.00946)
--- 

## 2 运动控制框架实战

### 2.1 任务目的

- 熟悉基于MPC（Model Predictive Control）和WBC（Whole Body Control）机器人控制框架
- 了解git、python、C++、ROS、CMake

### 2.2 任务内容

- 项目源码及简介 [Github](https://github.com/pocketxjl/humanoid-control) & [Zhihu](https://zhuanlan.zhihu.com/p/686462478)

- 跑通项目中提到的ocs2的四足机器人例子，如下图所示，并尝试使用如第二张图的终端控制其移动到指定位置，明白其中参数的含义

![legged_robot](_static/legged_robot.gif)

<img src="_static/image-20241228183740044.png" alt="image-20241228183740044" style="zoom: 80%;" />

- 跑通项目的双足机器人的例子，如下图，并且编写一个脚本来向话题`/cmd_vel`发送数据控制机器人以指定的速度移动

  ![5-162301511824622913613429231167146](_static/5-162301511824622913613429231167146.gif)

- 有能力的同学可以实现自动切换步态的功能，即机器人在站立状态下向`/cmd_vel`发送不为 0 的速度可以自动向前走，同时发送为 0 的速度可以自动停止

### 2.3 任务提示

- 由于本项目并不完善，所以如果你到了Getting Start部分，请你执行其中的命令，也就是在编译完后，启动`humanoid_dummy`功能包下的`legged_robot_sqp.launch`文件，该文件不会启动状态估计和wbc模块，但不妨碍大家阅读代码理解框架

  ```
  catkin config -DCMAKE_BUILD_TYPE=RelWithDebInfo #important
  catkin build humanoid_controllers humanoid_legged_description mujoco_sim
  # To start only the NMPC module and simulate with OCS2 dummy node
  roslaunch humanoid_dummy legged_robot_sqp.launch
  ```

- 本任务的环境最好使用ubuntu20.04，ros推荐安装ros1的noetic版本，python推荐安装3以上的版本，并且根据项目仓库的readme配置好本项目所需的环境

- 安装ros有一个自动化的脚本，参考[小鱼的一键安装系列 | 鱼香ROS](https://fishros.org.cn/forum/topic/20/小鱼的一键安装系列)

- 一些可能会踩的坑：
  - 开始本项目的时候需要先创建一个ros工作空间，然后将需要clone的仓库clone到workspace/src下
  - 如遇到`permission denied`报错，则需要进入root权限下执行命令
  - 如遇到`xxx.launch is neither a launch file in package`，则是因为没有`source /{path_to}/devel/setup.bash`，具体是`setup.bash`还是`setup.zsh`依赖于你的shell
  - 由于我们启动的是`legged_robot_sqp.launch`，该文件并不会启动`humanoid_target_trajectories_publisher`节点，所以有两种方法可以启动该节点：
    - 在`legged_robot_sqp.launch`中添加启动该节点的语句
    - 手动在终端启动该节点
  - `humanoid_target_trajectories_publisher`在`load_normal_controller.launch`文件中有提及，请参考之
--- 

## 3 视觉感知
#### 3.1 跑通yolo模型，完成基础的图像识别功能
  - yolo版本不限，能完成目标即可
  - 将yolo识别到的物体在视频中的像素坐标发布到ros话题中
#### 3.2 尝试使用自己的数据集进行训练
  - 根据去年比赛经验，我们提供一份按钮数据集，你可以使用这个数据集进行训练，并将识别效果和模型提交
  - 不需要实现强干扰情况下很准确的区分，能在给出数据集类似的条件下完成识别任务即可
#### 3.3 加入卡尔曼滤波，增强跟踪效果
  - 为了防止yolo暂时失去跟踪或者摄像头暂时被遮挡的情况，可以尝试在yolo中加入卡尔曼滤波，可以自行搜索相关开源实现
##### 效果演示：
<video src="_static/32_1735871085.mp4" controls="controls" style="width: 50%"></video>

--- 

## 4 补充说明
- 我们鼓励有一定基础的kuavo组同学在过程中使用ai工具，但你至少要能看懂ai的代码，明白程序背后的逻辑
