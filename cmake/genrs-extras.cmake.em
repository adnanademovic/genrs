@[if DEVELSPACE]@
# bin and template dir variables in develspace
set(GENRS_BIN "@(CMAKE_CURRENT_SOURCE_DIR)/scripts/gen_rs.py")
set(GENRS_TEMPLATE_DIR "@(CMAKE_CURRENT_SOURCE_DIR)/scripts")
@[else]@
# bin and template dir variables in installspace
set(GENRS_BIN "${genrs_DIR}/../../../@(CATKIN_PACKAGE_BIN_DESTINATION)/gen_rs.py")
set(GENRS_TEMPLATE_DIR "${genrs_DIR}/..")
@[end if]@

# Generate .msg->.rs for Rust
# The generated .rs files should be added ALL_GEN_OUTPUT_FILES_rs
macro(_generate_msg_rs ARG_PKG ARG_MSG ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  set(GEN_OUTPUT_DIR ${ARG_GEN_OUTPUT_DIR}/src)
  file(MAKE_DIRECTORY ${GEN_OUTPUT_DIR})

  #Create input and output filenames
  get_filename_component(MSG_NAME ${ARG_MSG} NAME)
  get_filename_component(MSG_SHORT_NAME ${ARG_MSG} NAME_WE)

  set(MSG_GENERATED_NAME ${MSG_SHORT_NAME}_msg.rs)
  set(GEN_OUTPUT_FILE ${GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})

  assert(CATKIN_ENV)
  add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
    DEPENDS ${GENRS_BIN} ${ARG_MSG} ${ARG_MSG_DEPS} "${GENRS_TEMPLATE_DIR}/msg.rs.template" ${ARGN}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENRS_BIN} ${ARG_MSG}
    ${ARG_IFLAGS}
    -p ${ARG_PKG}
    -o ${GEN_OUTPUT_DIR}
    -e ${GENRS_TEMPLATE_DIR}
    COMMENT "Generating Rust code from ${ARG_PKG}/${MSG_NAME}"
    )
  list(APPEND ALL_GEN_OUTPUT_FILES_rs ${GEN_OUTPUT_FILE})
endmacro()

#genrs uses the same program to generate srv and msg files, so call the same macro
macro(_generate_srv_rs ARG_PKG ARG_SRV ARG_IFLAGS ARG_MSG_DEPS ARG_GEN_OUTPUT_DIR)
  _generate_msg_rs(${ARG_PKG} ${ARG_SRV} "${ARG_IFLAGS}" "${ARG_MSG_DEPS}" ${ARG_GEN_OUTPUT_DIR} "${GENRS_TEMPLATE_DIR}/srv.rs.template")
endmacro()

macro(_generate_module_rs ARG_PKG ARG_GEN_OUTPUT_DIR ARG_GENERATED_FILES)
  set(GEN_OUTPUT_DIR ${ARG_GEN_OUTPUT_DIR}/src)
  file(MAKE_DIRECTORY ${GEN_OUTPUT_DIR})

  set(MSG_GENERATED_NAME lib.rs)
  set(GEN_OUTPUT_FILE ${GEN_OUTPUT_DIR}/${MSG_GENERATED_NAME})

  assert(CATKIN_ENV)
  add_custom_command(OUTPUT ${GEN_OUTPUT_FILE}
    DEPENDS ${GENRS_BIN} "${GENRS_TEMPLATE_DIR}/mod.rs.template" ${ARGN}
    COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENRS_BIN}
    -p ${ARG_PKG}
    -o ${GEN_OUTPUT_DIR}
    -e ${GENRS_TEMPLATE_DIR}
    -m
    COMMENT "Generating Rust module code for package ${ARG_PKG}"
    )

  list(APPEND ALL_GEN_OUTPUT_FILES_rs ${GEN_OUTPUT_FILE})

  # generate boilerplate cargo files
  if(NOT EXISTS ${ARG_GEN_OUTPUT_DIR}/Cargo.toml)
    file(WRITE ${ARG_GEN_OUTPUT_DIR}/Cargo.toml "[package]\nname = \"${ARG_PKG}-msg\"\nversion = \"1.0.0\"\n\n[dependencies]\nrosrust = \"*\"\nrustc-serialize = \"*\"\n")
  endif()
endmacro()

set(genrs_INSTALL_DIR rust)
