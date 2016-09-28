install(
  FILES msg.rs.template srv.rs.template
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

catkin_install_python(
  PROGRAMS gen_rs.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
