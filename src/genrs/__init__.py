import genmsg.msgs

try:
    from cStringIO import StringIO  #Python 2.x
except ImportError:
    from io import StringIO  #Python 3.x

MSG_TYPE_TO_RS = {
    'byte': 'i8',
    'char': 'u8',
    'bool': 'bool',
    'uint8': 'u8',
    'uint16': 'u16',
    'uint32': 'u32',
    'uint64': 'u64',
    'int8': 'i8',
    'int16': 'i16',
    'int32': 'i32',
    'int64': 'i64',
    'float32': 'f32',
    'float64': 'f64',
    'string': '::std::string::String',
    'time': 'u32',
    'duration': 'i32',
}


def depending_on(spec):
    """
    Creates a list of unique packages based on dependencies
    """
    packages = []
    for field in spec.parsed_fields():
        if (not field.is_builtin):
            if (field.is_header):
                packages.append('std_msgs')
            else:
                (package,
                 name) = genmsg.names.package_resource_name(field.base_type)
                packages.append((package or spec.package) + ' ' +
                                name)  # convert '' to package
    return set(packages)


def msg_type_to_rs(type, package):
    """
    Converts a message type (e.g. uint32, std_msgs/String, etc.) into the Rust declaration
    for that type (e.g. u32, std_msgs.String)

    @param type: The message type
    @type type: str
    @return: The Rust declaration
    @rtype: str
    """
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(type)
    rs_type = None
    if (genmsg.msgs.is_builtin(base_type)):
        rs_type = MSG_TYPE_TO_RS[base_type]
    elif (len(base_type.split('/')) == 1):
        if (genmsg.msgs.is_header_type(base_type)):
            rs_type = 'super::std_msgs::Header'
        else:
            rs_type = base_type
    else:
        pkg = base_type.split('/')[0]
        msg = base_type.split('/')[1]
        rs_type = 'super::%s::%s' % (pkg, msg)

    if is_array:
        if array_len is None:
            return 'Vec<%s>' % (rs_type)
        else:
            return '(%s)' % (', '.join([rs_type for _ in range(array_len)]))
    else:
        return rs_type


def default_value(type, package):
    """
    Returns the value to initialize a message member with.

    0 for integer types and times,
    0.0 for floating point,
    false for bool,
    default string for string,
    ::new() for everything else

    @param type: The type
    @type type: str
    """
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(type)
    if is_array and array_len is None:
        return 'Vec::new()'
    rs_def = None
    rs_type = msg_type_to_rs(base_type, package)
    if base_type in [
            'byte', 'int8', 'int16', 'int32', 'int64', 'char', 'uint8',
            'uint16', 'uint32', 'uint64', 'time', 'duration'
    ]:
        rs_def = '0' + rs_type
    elif base_type in ['float32', 'float64']:
        rs_def = '0.0' + rs_type
    elif base_type == 'bool':
        rs_def = 'false'
    elif base_type == 'string':
        rs_def = '::std::string::String::new()'
    else:
        rs_def = rs_type + '::new()'
    if is_array and array_len is not None:
        return '(%s)' % (', '.join([rs_def for _ in range(array_len)]))
    else:
        return rs_def


def _escape_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return s


def escape_message_definition(definition):
    lines = definition.splitlines()
    if not lines:
        lines.append('')
    s = StringIO()
    for line in lines:
        line = _escape_string(line)
        s.write('%s\\n\\\n' % (line))

    val = s.getvalue()
    s.close()
    return val
