import yaml
import byml.byml as byml

def add_constructors(loader):
    yaml.add_constructor(u'tag:yaml.org,2002:int', lambda l, node: byml.Int(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'tag:yaml.org,2002:float', lambda l, node: byml.Float(l.construct_yaml_float(node)), Loader=loader)
    yaml.add_constructor(u'!u', lambda l, node: byml.UInt(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'!l', lambda l, node: byml.Int64(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'!ul', lambda l, node: byml.UInt64(l.construct_yaml_int(node)), Loader=loader)
    yaml.add_constructor(u'!f64', lambda l, node: byml.Double(l.construct_yaml_float(node)), Loader=loader)

def add_representers(dumper):
    yaml.add_representer(byml.Int, lambda d, data: d.represent_int(data), Dumper=dumper)
    yaml.add_representer(byml.Float, lambda d, data: d.represent_float(data), Dumper=dumper)
    yaml.add_representer(byml.UInt, lambda d, data: d.represent_scalar(u'!u', '0x%08x' % data), Dumper=dumper)
    yaml.add_representer(byml.Int64, lambda d, data: d.represent_scalar(u'!l', str(data)), Dumper=dumper)
    yaml.add_representer(byml.UInt64, lambda d, data: d.represent_scalar(u'!ul', str(data)), Dumper=dumper)
    yaml.add_representer(byml.Double, lambda d, data: d.represent_scalar(u'!f64', str(data)), Dumper=dumper)
