#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "feetech_driver::serial_port" for configuration ""
set_property(TARGET feetech_driver::serial_port APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(feetech_driver::serial_port PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libserial_port.so.0.1.0"
  IMPORTED_SONAME_NOCONFIG "libserial_port.so.0"
  )

list(APPEND _cmake_import_check_targets feetech_driver::serial_port )
list(APPEND _cmake_import_check_files_for_feetech_driver::serial_port "${_IMPORT_PREFIX}/lib/libserial_port.so.0.1.0" )

# Import target "feetech_driver::communication_protocol" for configuration ""
set_property(TARGET feetech_driver::communication_protocol APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(feetech_driver::communication_protocol PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libcommunication_protocol.so.0.1.0"
  IMPORTED_SONAME_NOCONFIG "libcommunication_protocol.so.0"
  )

list(APPEND _cmake_import_check_targets feetech_driver::communication_protocol )
list(APPEND _cmake_import_check_files_for_feetech_driver::communication_protocol "${_IMPORT_PREFIX}/lib/libcommunication_protocol.so.0.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
