#!/usr/bin/env python3
# Copyright 2018 leoetlino <leo@leolam.fr>
# Licensed under MIT

from enum import IntEnum
import ctypes
from sortedcontainers import SortedDict # type: ignore
import struct
import typing

class NodeType(IntEnum):
    STRING = 0xa0
    ARRAY = 0xc0
    HASH = 0xc1
    STRING_TABLE = 0xc2
    BOOL = 0xd0
    INT = 0xd1
    FLOAT = 0xd2
    UINT = 0xd3
    INT64 = 0xd4
    UINT64 = 0xd5
    DOUBLE = 0xd6
    NULL = 0xff

_NUL_CHAR = b'\x00'

def _get_unpack_endian_character(big_endian: bool):
    return '>' if big_endian else '<'

def _align_up(value: int, size: int) -> int:
    return value + (size - value % size) % size

def _is_container_type(node_type: int) -> bool:
    return node_type == NodeType.ARRAY or node_type == NodeType.HASH

def _is_value_type(node_type: NodeType) -> bool:
    return node_type == NodeType.STRING or (NodeType.BOOL <= node_type <= NodeType.UINT) or node_type == NodeType.NULL

def _is_float(value: float) -> bool:
    # If a value can be represented as a float with no loss of precision,
    # then we assume that it is a float.
    return ctypes.c_float(value).value == ctypes.c_double(value).value

class Byml:
    """A simple BYMLv2 parser that handles both big endian and little endian documents."""

    def __init__(self, data: bytes) -> None:
        self._data = data

        magic = self._data[0:2]
        if magic == b'BY':
            self._be = True
        elif magic == b'YB':
            self._be = False
        else:
            raise ValueError("Invalid magic: %s (expected 'BY' or 'YB')" % magic)

        version = self._read_u16(2)
        if not (1 <= version <= 3):
            raise ValueError("Invalid version: %u (expected 1-3)" % version)
        if version == 1 and self._be:
            raise ValueError("Invalid version: %u-wiiu (expected 1-3)" % version)

        self._hash_key_table_offset = self._read_u32(4)
        self._string_table_offset = self._read_u32(8)

        self._hash_key_table = self._parse_string_table(self._hash_key_table_offset)
        if self._string_table_offset != 0:
            self._string_table = self._parse_string_table(self._string_table_offset)

    def parse(self) -> typing.Union[list, dict]:
        """Parse the BYML and get the root node with all children."""
        node_type = self._data[self._read_u32(12)]
        if not _is_container_type(node_type):
            raise ValueError("Invalid root node: expected array or dict, got type 0x%x" % node_type)
        return self._parse_node(node_type, 12)

    def _parse_string_table(self, offset) -> typing.List[str]:
        if self._data[offset] != NodeType.STRING_TABLE:
            raise ValueError("Invalid node type: 0x%x (expected 0xc2)" % self._data[offset])

        array = list()
        size = self._read_u24(offset + 1)
        for i in range(size):
            string_offset = offset + self._read_u32(offset + 4 + 4*i)
            array.append(self._read_string(string_offset))
        return array

    def _parse_node(self, node_type: int, offset: int):
        if node_type == NodeType.STRING:
            return self._parse_string_node(self._read_u32(offset))
        if node_type == NodeType.ARRAY:
            return self._parse_array_node(self._read_u32(offset))
        if node_type == NodeType.HASH:
            return self._parse_hash_node(self._read_u32(offset))
        if node_type == NodeType.BOOL:
            return self._parse_bool_node(offset)
        if node_type == NodeType.INT:
            return self._parse_int_node(offset)
        if node_type == NodeType.FLOAT:
            return self._parse_float_node(offset)
        if node_type == NodeType.UINT:
            return self._parse_uint_node(offset)
        if node_type == NodeType.INT64:
            return self._parse_int64_node(self._read_u32(offset))
        if node_type == NodeType.UINT64:
            return self._parse_uint64_node(self._read_u32(offset))
        if node_type == NodeType.DOUBLE:
            return self._parse_double_node(self._read_u32(offset))
        if node_type == NodeType.NULL:
            return None
        raise ValueError("Unknown node type: 0x%x" % node_type)

    def _parse_string_node(self, index: int) -> str:
        return self._string_table[index]

    def _parse_array_node(self, offset: int) -> list:
        size = self._read_u24(offset + 1)
        array: list = list()
        value_array_offset: int = offset + _align_up(size, 4) + 4
        for i in range(size):
            node_type = self._data[offset + 4 + i]
            array.append(self._parse_node(node_type, value_array_offset + 4*i))
        return array

    def _parse_hash_node(self, offset: int) -> dict:
        size = self._read_u24(offset + 1)
        result: dict = dict()
        for i in range(size):
            entry_offset: int = offset + 4 + 8*i
            string_index: int = self._read_u24(entry_offset + 0)
            name: str = self._hash_key_table[string_index]

            node_type = self._data[entry_offset + 3]
            result[name] = self._parse_node(node_type, entry_offset + 4)

        return result

    def _parse_bool_node(self, offset: int) -> bool:
        return self._parse_uint_node(offset) != 0

    def _parse_int_node(self, offset: int) -> int:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'i', self._data, offset)[0]

    def _parse_float_node(self, offset: int) -> float:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'f', self._data, offset)[0]

    def _parse_uint_node(self, offset: int) -> int:
        return self._read_u32(offset)

    def _parse_int64_node(self, offset: int) -> int:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'q', self._data, offset)[0]

    def _parse_uint64_node(self, offset: int) -> int:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'Q', self._data, offset)[0]

    def _parse_double_node(self, offset: int) -> float:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'd', self._data, offset)[0]

    def _read_u16(self, offset: int) -> int:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'H', self._data, offset)[0]

    def _read_u24(self, offset: int) -> int:
        if self._be:
            return struct.unpack('>I', _NUL_CHAR + self._data[offset:offset+3])[0]
        return struct.unpack('<I', self._data[offset:offset+3] + _NUL_CHAR)[0]

    def _read_u32(self, offset: int) -> int:
        return struct.unpack_from(_get_unpack_endian_character(self._be) + 'I', self._data, offset)[0]

    def _read_string(self, offset: int) -> str:
        end = self._data.find(_NUL_CHAR, offset)
        return self._data[offset:end].decode('utf-8')

class _PlaceholderOffsetWriter:
    """Writes a placeholder offset value that will be filled later."""
    def __init__(self, stream: typing.BinaryIO, parent) -> None:
        self._stream = stream
        self._offset = stream.tell()
        self._parent = parent
    def write_placeholder(self) -> None:
        self._stream.write(self._parent._u32(0xffffffff))
    def write_current_offset(self, base: int = 0) -> None:
        current_offset = self._stream.tell()
        self._stream.seek(self._offset)
        self._stream.write(self._parent._u32(current_offset - base))
        self._stream.seek(current_offset)

class Writer:
    """BYMLv2 writer."""

    def __init__(self, data: typing.Union[dict, list], be=False, version=2) -> None:
        self._data = data
        self._be = be
        self._version = version

        if not isinstance(data, list) and not isinstance(data, dict):
            raise ValueError("Data should be a dict or a list")

        if not (1 <= version <= 3):
            raise ValueError("Invalid version: %u (expected 1-3)" % version)
        if version == 1 and be:
            raise ValueError("Invalid version: %u-wiiu (expected 1-3)" % version)

        self._hash_key_table: SortedDict[str, int] = SortedDict()
        self._string_table: SortedDict[str, int] = SortedDict()
        self._make_string_table(self._data, self._hash_key_table, self._string_table)
        # Nintendo seems to sort entries in alphabetical order.
        self._sort_string_table(self._hash_key_table)
        self._sort_string_table(self._string_table)

    def write(self, stream: typing.BinaryIO) -> None:
        # Header
        stream.write(b'BY' if self._be else b'YB')
        stream.write(self._u16(self._version))
        hash_key_table_offset_writer = self._write_placeholder_offset(stream)
        string_table_offset_writer = self._write_placeholder_offset(stream)
        root_node_offset_writer = self._write_placeholder_offset(stream)

        # Hash key table
        hash_key_table_offset_writer.write_current_offset()
        self._write_string_table(stream, self._hash_key_table)
        stream.seek(_align_up(stream.tell(), 4))

        # String table
        string_table_offset_writer.write_current_offset()
        self._write_string_table(stream, self._string_table)
        stream.seek(_align_up(stream.tell(), 4))

        # Root node
        root_node_offset_writer.write_current_offset()
        self._write_nonvalue_node(stream, self._data)
        stream.seek(_align_up(stream.tell(), 4))

    def _make_string_table(self, data, hash_key_table: SortedDict, string_table: SortedDict):
        if isinstance(data, str) and data not in string_table:
            string_table[data] = 0xffffffff
        elif isinstance(data, list):
            for item in data:
                self._make_string_table(item, hash_key_table, string_table)
        elif isinstance(data, dict):
            for (key, value) in data.items():
                if key not in hash_key_table:
                    hash_key_table[key] = 0xffffffff
                self._make_string_table(value, hash_key_table, string_table)

    def _sort_string_table(self, table: SortedDict):
        for (i, key) in enumerate(table.keys()):
            table[key] = i

    def _write_string_table(self, stream: typing.BinaryIO, table: typing.Dict[str, int]):
        base = stream.tell()
        stream.write(self._u8(NodeType.STRING_TABLE))
        stream.write(self._u24(len(table)))
        offset_writers: typing.List[_PlaceholderOffsetWriter] = []
        for i in range(len(table)):
            offset_writers.append(self._write_placeholder_offset(stream))
        last_offset_writer = self._write_placeholder_offset(stream)

        for (string, offset_writer) in zip(table.keys(), offset_writers):
            offset_writer.write_current_offset(base)
            stream.write(bytes(string, "utf8"))
            stream.write(_NUL_CHAR)
        last_offset_writer.write_current_offset(base)

    def _write_nonvalue_node(self, stream: typing.BinaryIO, data) -> None:
        nonvalue_nodes: typing.List[typing.Tuple[typing.Any, _PlaceholderOffsetWriter]] = []

        if isinstance(data, list):
            stream.write(self._u8(NodeType.ARRAY))
            stream.write(self._u24(len(data)))
            for item in data:
                stream.write(self._u8(self._to_byml_type(item)))
            stream.seek(_align_up(stream.tell(), 4))
            for item in data:
                if _is_value_type(self._to_byml_type(item)):
                    stream.write(self._to_byml_value(item))
                else:
                    nonvalue_nodes.append((item, self._write_placeholder_offset(stream)))
        elif isinstance(data, dict):
            stream.write(self._u8(NodeType.HASH))
            stream.write(self._u24(len(data)))
            for (key, value) in data.items():
                stream.write(self._u24(self._hash_key_table[key]))
                node_type = self._to_byml_type(value)
                stream.write(self._u8(node_type))
                if _is_value_type(node_type):
                    stream.write(self._to_byml_value(value))
                else:
                    nonvalue_nodes.append((value, self._write_placeholder_offset(stream)))
        elif isinstance(data, int) and 32 < data.bit_length() <= 64:
            stream.write(self._s64(data) if data < 0 else self._u64(data))
        elif isinstance(data, float) and not _is_float(data):
            stream.write(self._f64(data))
        else:
            raise ValueError("Invalid non-value type")

        for (data, offset_writer) in nonvalue_nodes:
            offset_writer.write_current_offset()
            self._write_nonvalue_node(stream, data)

    def _to_byml_type(self, data) -> NodeType:
        if isinstance(data, str):
            return NodeType.STRING
        if isinstance(data, list):
            return NodeType.ARRAY
        if isinstance(data, dict):
            return NodeType.HASH
        if isinstance(data, bool):
            return NodeType.BOOL
        if isinstance(data, int):
            size = data.bit_length()
            if size <= 32:
                return NodeType.INT if data < 0 else NodeType.UINT
            if size <= 64:
                return NodeType.INT64 if data < 0 else NodeType.UINT64
        if isinstance(data, float):
            return NodeType.FLOAT if _is_float(data) else NodeType.DOUBLE
        raise ValueError("Invalid value type")

    def _to_byml_value(self, value) -> bytes:
        if isinstance(value, str):
            return self._u32(self._string_table[value])
        if isinstance(value, bool):
            return self._u32(1 if value != 0 else 0)
        if isinstance(value, int):
            if value.bit_length() <= 32:
                return self._s32(value) if value < 0 else self._u32(value)
        if isinstance(value, float) and _is_float(value):
            return self._f32(value)
        raise ValueError("Invalid value type")

    def _write_placeholder_offset(self, stream) -> _PlaceholderOffsetWriter:
        p = _PlaceholderOffsetWriter(stream, self)
        p.write_placeholder()
        return p

    def _u8(self, value) -> bytes:
        return struct.pack('B', value)
    def _u16(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'H', value)
    def _s16(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'h', value)
    def _u24(self, value) -> bytes:
        b = struct.pack(_get_unpack_endian_character(self._be) + 'I', value)
        return b[1:] if self._be else b[:-1]
    def _u32(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'I', value)
    def _s32(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'i', value)
    def _u64(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'Q', value)
    def _s64(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'q', value)
    def _f32(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'f', value)
    def _f64(self, value) -> bytes:
        return struct.pack(_get_unpack_endian_character(self._be) + 'd', value)
