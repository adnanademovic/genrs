#!/usr/bin/env python

## ROS message source code generation for Rust
##
## Converts ROS .msg files in a package into Rust source code implementations.

import sys
import os
import genmsg.template_tools

msg_template_map = { 'msg.rs.template':'@NAME@_msg.rs' }
srv_template_map = { 'srv.rs.template':'@NAME@_msg.rs' }
mod_template_map = { 'mod.rs.template':'lib.rs' }

if __name__ == "__main__":
    print sys.argv
    genmsg.template_tools.generate_from_command_line_options(sys.argv,
                                                             msg_template_map,
                                                             srv_template_map,
                                                             mod_template_map)
