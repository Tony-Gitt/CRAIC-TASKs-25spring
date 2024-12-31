# Kuavo选拔任务

## 任务目的

- 熟悉基于MPC（Model Predictive Control）和WBC（Whole Body Control）机器人控制框架
- 了解git、python、C++、ROS、CMake

## 任务内容

- 项目源码及简介 [Github](https://github.com/pocketxjl/humanoid-control) & [Zhihu](https://zhuanlan.zhihu.com/p/686462478)

- 跑通项目中提到的ocs2的四足机器人例子，如下图所示，并尝试使用如第二张图的终端控制其移动到指定位置，明白其中参数的含义

![legged_robot](_static/legged_robot.gif)

<img src="_static/image-20241228183740044.png" alt="image-20241228183740044" style="zoom: 80%;" />

- 跑通项目的双足机器人的例子，如下图，并且编写一个脚本来向话题`/cmd_vel`发送数据控制机器人以指定的速度移动

  ![5-162301511824622913613429231167146](_static/5-162301511824622913613429231167146.gif)

- 有能力的同学可以实现自动切换步态的功能，即机器人在站立状态下向`/cmd_vel`发送不为 0 的速度可以自动向前走，同时发送为 0 的速度可以自动停止

## 任务提示

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

  - 如遇到`permission denied`报错，则需要进入root权限下执行命令
  - 如遇到`xxx.launch is neither a launch file in package`，则是因为没有`source /{path_to}/devel/setup.bash`，具体是`setup.bash`还是`setup.zsh`依赖于你的shell
  - 由于我们启动的是`legged_robot_sqp.launch`，该文件并不会启动`humanoid_target_trajectories_publisher`节点，所以有两种方法可以启动该节点：
    - 在`legged_robot_sqp.launch`种添加启动该节点的语句
    - 手动在终端启动该节点
  - `humanoid_target_trajectories_publisher`在`load_normal_controller.launch`文件中有提及，请参考之

