# TODO

## Done

- F1TENTH ROS 2 bridge working
- LaserScan publishing
- Odometry publishing
- TF publishing
- URDF / Robot State Publisher
- `/drive` subscriber
- Pure Pursuit planner
- WaypointManager
- CSV-based waypoint loading
- VehicleState abstraction
- Project reorganization

## Next

- Add Stanley controller
- Add MPC controller
- Add occupancy grid mapping
- Add A* planner

## Later

- Hybrid A*
- RRT
- Particle filter
- EKF localization
- SLAM
- Digital twin improvements
- Autoware integration

## Notes

- Keep ROS nodes separate from pure Python logic.
- Keep tuning values in `config/sim.yaml`.
- Keep waypoints in CSV files.
- Keep bridge and planner behavior stable before adding new algorithms.
