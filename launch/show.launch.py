import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.conditions import IfCondition, LaunchConfigurationEquals
from launch.substitutions import FindExecutable, Command, LaunchConfiguration


def generate_launch_description():

    # Аргументы запуска
    rviz2_launch_argument_declare = DeclareLaunchArgument(
        'rviz2_run',
        default_value = 'true',
        description = 'Start Rviz2 when starting descriptions.'
    )


    # Параметры окружения
    description_pkg_name = 'smartbox_description'
    description_file_name = 'main.urdf.xacro'
    rviz2_config_file_name = 'rviz2_description_config.rviz'


    # Пути к пакетам
    description_pkg_path = get_package_share_directory(description_pkg_name)


    # Пути к конфигурационным файлам
    rviz2_config_file_path = os.path.join(
        description_pkg_path,
        'config',
        rviz2_config_file_name
    )


    # Парсинг описания робота
    robot_description = Command([
        FindExecutable(name='xacro'),
        ' ',
        os.path.join(description_pkg_path, 'urdf', description_file_name),
    ])


    # Ноды
    robot_state_publisher_node = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher', 
        name = 'robot_state_publisher',
        output = 'screen',
        parameters = [{
            'robot_description' : robot_description
        }]
    )

    joint_state_publisher_node = Node(
        package = 'joint_state_publisher_gui',
        executable = 'joint_state_publisher_gui',
        name = 'joint_state_publisher_gui',
        output = 'screen',
        condition = IfCondition(LaunchConfiguration('rviz2_run')),
    )

    rviz2_launch_node = Node(
        package = 'rviz2',
        executable = 'rviz2',
        name = 'rviz2',
        output = 'screen',
        arguments = ['-d', rviz2_config_file_path],
        condition = IfCondition(LaunchConfiguration('rviz2_run')),
    )


    # Запуск
    ld = LaunchDescription()

    ld.add_action(rviz2_launch_argument_declare)

    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz2_launch_node)

    return ld