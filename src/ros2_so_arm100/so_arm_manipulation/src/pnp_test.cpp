#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.hpp>

#include <moveit_msgs/msg/display_robot_state.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>

#include <moveit_msgs/msg/attached_collision_object.hpp>
#include <moveit_msgs/msg/collision_object.hpp>

//#include <moveit_visual_tools/moveit_visual_tools.h>

static const rclcpp::Logger LOGGER = rclcpp::get_logger("pnp_test");

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::NodeOptions node_options;
    node_options.automatically_declare_parameters_from_overrides(true);

    auto move_group_node = rclcpp::Node::make_shared("pnp_test", node_options);

    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(move_group_node);
    std::thread([&executor]() {executor.spin();}).detach();

    static const std::string MANIP_PLANNING_GROUP = "manipulator";
    static const std::string GRIP_PLANNING_GROUP = "gripper";

    moveit::planning_interface::MoveGroupInterface move_group(move_group_node, MANIP_PLANNING_GROUP);
    moveit::planning_interface::MoveGroupInterface gripper_group(move_group_node, GRIP_PLANNING_GROUP);
    gripper_group.setMaxVelocityScalingFactor(0.03);
    gripper_group.setMaxAccelerationScalingFactor(0.03);

    std::vector<std::string> target_seq = {"rest", "extended", "zero"};
    for (const auto &target_name: target_seq) {
        RCLCPP_INFO(LOGGER, "Setting target to: '%s'", target_name.c_str());
        move_group.setNamedTarget(target_name);

        moveit::planning_interface::MoveGroupInterface::Plan pnp_plan;
        bool success = (move_group.plan(pnp_plan) == moveit::core::MoveItErrorCode::SUCCESS);
        if (success) {
            move_group.execute(pnp_plan);
        } else {
            RCLCPP_ERROR(LOGGER, "Planning to '%s' failed!", target_name.c_str());
            break;
        }
    }

    std::vector<std::string> grip_target_seq = {"open", "closed"};
    for (const auto &target_name: grip_target_seq) {
        RCLCPP_INFO(LOGGER, "Setting target to: '%s'", target_name.c_str());
        gripper_group.setNamedTarget(target_name);

        moveit::planning_interface::MoveGroupInterface::Plan pnp_plan;
        bool success = (gripper_group.plan(pnp_plan) == moveit::core::MoveItErrorCode::SUCCESS);
        if (success) {
            gripper_group.execute(pnp_plan);
        } else {
            RCLCPP_ERROR(LOGGER, "Planning to '%s' failed!", target_name.c_str());
            break;
        }
    }


    
}
