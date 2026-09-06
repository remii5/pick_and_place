from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("so_arm101", package_name="so_arm101_moveit_config")
        .robot_description(file_path="urdf/so_arm101.urdf.xacro")
        .robot_description_semantic(file_path="config/so_arm101.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .trajectory_execution(file_path="config/trajectory_execution.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    pnp_test_node = Node(
        package="so_arm_manipulation",
        executable="pnp_test",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription([pnp_test_node])