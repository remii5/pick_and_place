// Copyright 2015 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef FEETECH_ROS2_DRIVER__VERSION_H_
#define FEETECH_ROS2_DRIVER__VERSION_H_

/// \def FEETECH_ROS2_DRIVER_VERSION_MAJOR
/// Defines FEETECH_ROS2_DRIVER major version number
#define FEETECH_ROS2_DRIVER_VERSION_MAJOR (0)

/// \def FEETECH_ROS2_DRIVER_VERSION_MINOR
/// Defines FEETECH_ROS2_DRIVER minor version number
#define FEETECH_ROS2_DRIVER_VERSION_MINOR (2)

/// \def FEETECH_ROS2_DRIVER_VERSION_PATCH
/// Defines FEETECH_ROS2_DRIVER version patch number
#define FEETECH_ROS2_DRIVER_VERSION_PATCH (2)

/// \def FEETECH_ROS2_DRIVER_VERSION_STR
/// Defines FEETECH_ROS2_DRIVER version string
#define FEETECH_ROS2_DRIVER_VERSION_STR "0.2.2"

/// \def FEETECH_ROS2_DRIVER_VERSION_GTE
/// Defines a macro to check whether the version of FEETECH_ROS2_DRIVER is greater than or equal to
/// the given version triple.
#define FEETECH_ROS2_DRIVER_VERSION_GTE(major, minor, patch) ( \
     (major < FEETECH_ROS2_DRIVER_VERSION_MAJOR) ? true \
     : ((major > FEETECH_ROS2_DRIVER_VERSION_MAJOR) ? false \
     : ((minor < FEETECH_ROS2_DRIVER_VERSION_MINOR) ? true \
     : ((minor > FEETECH_ROS2_DRIVER_VERSION_MINOR) ? false \
     : ((patch < FEETECH_ROS2_DRIVER_VERSION_PATCH) ? true \
     : ((patch > FEETECH_ROS2_DRIVER_VERSION_PATCH) ? false \
     : true))))))

#endif  // FEETECH_ROS2_DRIVER__VERSION_H_
