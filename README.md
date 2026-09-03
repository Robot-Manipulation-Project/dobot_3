# dobot_3

ROS 2 workspace containing the `turtle_chase` Python package, where:
- `leader` publishes random motion commands for a turtle.
- `follower` subscribes to leader/follower poses and drives the follower turtle to chase the leader.
- `/turbo` (`std_srvs/SetBool`) toggles leader forward speed between normal and turbo mode.

## Repository layout

- `src/turtle_chase/` – ROS 2 package source
- `build/`, `install/`, `log/` – generated colcon artifacts

## Requirements

- ROS 2 (with `rclpy`)
- `geometry_msgs`
- `turtlesim_msgs`
- `std_srvs`
- `turtlesim`

## Build

From the repository root:

```bash
colcon build
source install/setup.bash
```

## Run demo

1. Start turtlesim:

```bash
ros2 run turtlesim turtlesim_node
```

2. In another terminal, spawn named turtles:

```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.5, y: 8.5, theta: 0.0, name: 'leader'}"
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'follower'}"
```

3. Start the package nodes (separate terminals):

```bash
source install/setup.bash
ros2 run turtle_chase leader
```

```bash
source install/setup.bash
ros2 run turtle_chase follower
```

4. Toggle turbo mode for the leader:

```bash
ros2 service call /turbo std_srvs/srv/SetBool "{data: true}"   # enable
ros2 service call /turbo std_srvs/srv/SetBool "{data: false}"  # disable
```

## Test

```bash
colcon test --packages-select turtle_chase
colcon test-result --verbose
```
