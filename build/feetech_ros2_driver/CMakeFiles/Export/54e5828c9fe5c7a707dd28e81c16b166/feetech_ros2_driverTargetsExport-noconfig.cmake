#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "feetech_ros2_driver::feetech_ros2_driver" for configuration ""
set_property(TARGET feetech_ros2_driver::feetech_ros2_driver APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(feetech_ros2_driver::feetech_ros2_driver PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libfeetech_ros2_driver.so"
  IMPORTED_SONAME_NOCONFIG "libfeetech_ros2_driver.so"
  )

list(APPEND _cmake_import_check_targets feetech_ros2_driver::feetech_ros2_driver )
list(APPEND _cmake_import_check_files_for_feetech_ros2_driver::feetech_ros2_driver "${_IMPORT_PREFIX}/lib/libfeetech_ros2_driver.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
