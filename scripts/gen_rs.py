#!/usr/bin/env python

## ROS message source code generation for Rust
##
## Converts ROS .msg files in a package into Rust source code implementations.

import sys
import os
import genmsg.template_tools

msg_template_map = { 'msg.rs.template':'@NAME@.rs' }
srv_template_map = { 'srv.rs.template':'@NAME@.rs' }

if __name__ == "__main__":
    print sys.argv
    genmsg.template_tools.generate_from_command_line_options(sys.argv,
                                                             msg_template_map,
                                                             srv_template_map)
