# Naive Localization using Dead Reckoning
This rosnode performs naive dead reckoning using the IMU (accelerometer, gyroscope).
This works with RealSense data, but can be adapted to work with your tello.

## Step 1: Clone this repo into your `~/catkin_ws/src` folder.

```
cd ~/catkin_ws/src
git clone https://github.com/BWSI-UAV/localization_naive.git
cd ..
```

## Step 2: Build code and source environment.

```
catkin_make
source ~/catkin_ws/devel/setup/bash
```

## Step 3: Download localization test data and save to `~/catkin_ws/src/localization_data`

Download the data from [here](https://drive.google.com/drive/folders/1teG22aWzBdCmb1oLQIcWpft_Cf3wPWx8?usp=sharing).

## Step 4: Start localization viewer

```
roslaunch localization_naive start_rqt.launch
```

## Step 5: Drag and drop the `/processed_pose` topic to the cube. 


![Drag the topic to the cube.](https://user-images.githubusercontent.com/1864821/179127975-8cdd62c0-be4c-4aef-8977-2f6d5f41f3d3.gif)

## Step 6: Start dead reckoning
```
roslaunch localization_naive dead_reckoning.launch
```
