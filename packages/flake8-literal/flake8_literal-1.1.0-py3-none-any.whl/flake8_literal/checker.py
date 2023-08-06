"""Checker for quote handling on string literals."""

import ast
import tokenize
from abc import abstractproperty
from typing import ClassVar, FrozenSet, Iterator, List, Optional, Sequence, Set, Tuple, Type

from typing_extensions import Protocol


try:
	import pkg_resources
	package_version = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound:
	package_version = 'unknown'


IGNORE_TOKENS = frozenset((
	tokenize.ENCODING,
	tokenize.NEWLINE,
	tokenize.INDENT,
	tokenize.DEDENT,
	tokenize.NL,
	tokenize.COMMENT,
))

OPEN_BRACKET = frozenset(('(', '[', '{'))
CLOSE_BRACKET = frozenset((')', ']', '}'))


class Options(Protocol):
	"""Protocol for options."""

	literal_include_name: bool


class Message(Protocol):
	"""Messages."""

	@abstractproperty
	def code(self) -> str:
		...

	def text(self, **kwargs) -> str:
		...


LogicalResult = Tuple[Tuple[int, int], str]  # (line, column), text
PhysicalResult = Tuple[int, str]  # (column, text)
ASTResult = Tuple[int, int, str, Type]  # (line, column, text, Type)


class Checker:
	"""Base class for checkers."""

	name: ClassVar[str] = __package__.replace('_', '-')
	version: ClassVar[str] = package_version
	plugin_name: ClassVar[str]

	@classmethod
	def parse_options(cls, options: Options) -> None:
		cls.plugin_name = (' (' + cls.name + ')') if (options.literal_include_name) else ''

	def _logical_token_message(self, token: tokenize.TokenInfo, message: Message, **kwargs) -> LogicalResult:
		return (token.start, f'{message.code}{self.plugin_name} {message.text(**kwargs)}')

	def _pyhsical_token_message(self, token: tokenize.TokenInfo, message: Message, **kwargs) -> PhysicalResult:
		return (token.start[1], f'{message.code}{self.plugin_name} {message.text(**kwargs)}')

	def _ast_token_message(self, token: tokenize.TokenInfo, message: Message, **kwargs) -> ASTResult:
		return (token.start[0], token.start[1], f'{message.code}{self.plugin_name} {message.text(**kwargs)}', type(self))

	def _ast_node_message(self, node: ast.AST, message: Message, **kwargs) -> ASTResult:
		return (node.lineno, node.col_offset, f'{message.code}{self.plugin_name} {message.text(**kwargs)}', type(self))


class LiteralChecker(Checker):
	"""Base class for literal checkers."""

	tokens: Sequence[tokenize.TokenInfo]
	_docstring_tokens: Optional[FrozenSet[tokenize.TokenInfo]]

	def __init__(self, logical_line: str, tokens: Sequence[tokenize.TokenInfo]) -> None:
		self.tokens = tokens
		self._docstring_tokens = None

	@property
	def docstring_tokens(self) -> FrozenSet[tokenize.TokenInfo]:
		"""Find docstring tokens, which are initial strings or strings immediately after class or function defs."""
		if (self._docstring_tokens is None):
			docstrings: Set[tokenize.TokenInfo] = set()
			expect_docstring = True
			expect_colon = False
			bracket_depth = 0
			for token in self.tokens:
				if (token.type in IGNORE_TOKENS):
					continue
				if (tokenize.STRING == token.type):
					if (expect_docstring):
						docstrings.add(token)
				else:
					expect_docstring = False
					if ((tokenize.NAME == token.type) and (token.string in ('class', 'def'))):
						expect_colon = True
						bracket_depth = 0
					elif (tokenize.OP == token.type):
						if (':' == token.string):
							if (0 == bracket_depth):
								if (expect_colon):
									expect_docstring = True
								expect_colon = False
						elif (token.string in OPEN_BRACKET):
							bracket_depth += 1
						elif (token.string in CLOSE_BRACKET):
							bracket_depth -= 1
			self._docstring_tokens = frozenset(docstrings)
		return self._docstring_tokens

	def _process_literals(self, tokens: Sequence[tokenize.TokenInfo]) -> Iterator[LogicalResult]:
		raise NotImplementedError()

	def __iter__(self) -> Iterator[LogicalResult]:
		"""Primary call from flake8, yield error messages."""
		continuation: List[tokenize.TokenInfo] = []
		for token in self.tokens:
			if (token.type in IGNORE_TOKENS):
				continue

			if (tokenize.STRING == token.type):
				continuation.append(token)
				continue

			for message in self._process_literals(continuation):
				yield message
			continuation = []

		for message in self._process_literals(continuation):
			yield message
