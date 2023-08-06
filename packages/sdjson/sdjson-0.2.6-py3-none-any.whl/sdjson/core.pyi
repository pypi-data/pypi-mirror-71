#  !/usr/bin/env python
#
#  __init__.pyi
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Based on https://treyhunner.com/2013/09/singledispatch-json-serializer/
#  Copyright © 2013 Trey Hunner
#  He said "Feel free to use it however you like." So I have.
#
#  Also based on the `json` module (version 2.0.9) by Bob Ippolito from Python 3.7
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#
#  Type annotations from Typeshed
#  https://github.com/python/typeshed
#  Apache 2.0 Licensed
#

# stdlib
import json
from functools import singledispatch
from typing import IO, Any, Callable, Dict, Iterator, List, Optional, Protocol, Tuple, Type, TypeVar, Union

# 3rd party
from domdf_python_tools.doctools import append_docstring_from, is_documented_by

__author__: str
__copyright__: str

__license__: str
__version__: str
__email__: str

_T_co = TypeVar("_T_co", covariant=True)
_LoadsString = Union[str, bytes]


class SupportsRead(Protocol[_T_co]):
	def read(self, __length: int = ...) -> _T_co: ...


def allow_unregister(func) -> Callable: ...


def sphinxify_json_docstring() -> Callable: ...


@allow_unregister
@singledispatch
class _Encoders:
	register: Callable
	unregister: Callable


encoders = _Encoders
register_encoder = _Encoders.register  # type: ignore
unregister_encoder = _Encoders.unregister  # type: ignore


def dump(
		obj: Any,
		 fp: IO[str],
		 *,
		 skipkeys: bool = ...,
		 ensure_ascii: bool = ...,
		 check_circular: bool = ...,
		 allow_nan: bool = ...,
		 cls: Optional[Type[json.JSONEncoder]] = ...,
		 indent: Union[None, int, str] = ...,
		 separators: Optional[Tuple[str, str]] = ...,
		 default: Optional[Callable[[Any], Any]] = ...,
		 sort_keys: bool = ...,
		 **kwargs: Any) -> None: ...


def dumps(
		obj: Any,
		  *,
		  skipkeys: bool = ...,
		  ensure_ascii: bool = ...,
		  check_circular: bool = ...,
		  allow_nan: bool = ...,
		  cls: Optional[Type[json.JSONEncoder]] = ...,
		  indent: Union[None, int, str] = ...,
		  separators: Optional[Tuple[str, str]] = ...,
		  default: Optional[Callable[[Any], Any]] = ...,
		  sort_keys: bool = ...,
		  **kwargs: Any) -> str: ...


@sphinxify_json_docstring()
@append_docstring_from(json.load)
def loads(
		s: _LoadsString,
		  *,
		  cls: Optional[Type[json.JSONDecoder]] = ...,
		  object_hook: Optional[Callable[[Dict[Any, Any]], Any]] = ...,
		  parse_float: Optional[Callable[[str], Any]] = ...,
		  parse_int: Optional[Callable[[str], Any]] = ...,
		  parse_constant: Optional[Callable[[str], Any]] = ...,
		  object_pairs_hook: Optional[Callable[[List[Tuple[Any, Any]]], Any]] = ...,
		  **kwargs: Any) -> Any: ...


@sphinxify_json_docstring()
@append_docstring_from(json.loads)
def load(
		fp: SupportsRead[_LoadsString],
		 *,
		 cls: Optional[Type[json.JSONDecoder]] = ...,
		 object_hook: Optional[Callable[[Dict[Any, Any]], Any]] = ...,
		 parse_float: Optional[Callable[[str], Any]] = ...,
		 parse_int: Optional[Callable[[str], Any]] = ...,
		 parse_constant: Optional[Callable[[str], Any]] = ...,
		 object_pairs_hook: Optional[Callable[[List[Tuple[Any, Any]]], Any]] = ...,
		 **kwargs: Any) -> Any: ...


@sphinxify_json_docstring()
@append_docstring_from(json.JSONEncoder)
class JSONEncoder(json.JSONEncoder):

	def __init__(
		self,
		*,
		skipkeys: bool = ...,
		ensure_ascii: bool = ...,
		check_circular: bool = ...,
		allow_nan: bool = ...,
		sort_keys: bool = ...,
		indent: Optional[int] = ...,
		separators: Optional[Tuple[str, str]] = ...,
		default: Optional[Callable[..., Any]] = ...
		) -> None: ...

	@sphinxify_json_docstring()
	@is_documented_by(json.JSONEncoder.default)
	def default(self, o: Any) -> Any: ...

	@sphinxify_json_docstring()
	@is_documented_by(json.JSONEncoder.encode)
	def encode(self, o: Any) -> str: ...

	@sphinxify_json_docstring()
	@is_documented_by(json.JSONEncoder.iterencode)
	def iterencode(self, o: Any, _one_shot: bool = ...) -> Iterator[str]: ...



@sphinxify_json_docstring()
@append_docstring_from(json.JSONDecoder)
class JSONDecoder:
	object_hook: Callable[[Dict[str, Any]], Any]
	parse_float: Callable[[str], Any]
	parse_int: Callable[[str], Any]
	parse_constant = ...  # Callable[[str], Any]
	strict: bool
	object_pairs_hook: Callable[[List[Tuple[str, Any]]], Any]

	def __init__(
		self,
		*,
		object_hook: Optional[Callable[[Dict[str, Any]], Any]] = ...,
		parse_float: Optional[Callable[[str], Any]] = ...,
		parse_int: Optional[Callable[[str], Any]] = ...,
		parse_constant: Optional[Callable[[str], Any]] = ...,
		strict: bool = ...,
		object_pairs_hook: Optional[Callable[[List[Tuple[str, Any]]], Any]] = ...
	) -> None: ...

	@sphinxify_json_docstring()
	@is_documented_by(json.JSONDecoder.decode)
	def decode(self, s: str, _w: Callable[..., Any] = ...) -> Any: ...  # _w is undocumented

	@sphinxify_json_docstring()
	@is_documented_by(json.JSONDecoder.raw_decode)
	def raw_decode(self, s: str, idx: int = ...) -> Tuple[Any, int]: ...


JSONDecodeError = json.JSONDecodeError


# Custom encoder for sdjson
class _CustomEncoder(JSONEncoder):

	def default(self, obj):
		for type_, handler in encoders.registry.items():
			if isinstance(obj, type_) and type_ is not object:
				return handler(obj)
		return super().default(obj)


_default_encoder = _CustomEncoder(
		skipkeys=False,
		ensure_ascii=True,
		check_circular=True,
		allow_nan=True,
		indent=None,
		separators=None,
		default=None,
		)
