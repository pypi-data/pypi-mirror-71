from collections import Counter, namedtuple
from enum import Enum
import inspect
from typing import List, Optional

import click
import commonmark.node    # type: ignore
import monotable

from phmdoctest import tool
from phmdoctest import print_capture


class Role(Enum):
    """Role that markdown fenced code block plays in testing."""
    UNKNOWN = '--'
    CODE = 'code'
    OUTPUT = 'output'
    SESSION = 'session'
    SKIP_CODE = 'skip-code'
    SKIP_OUTPUT = 'skip-output'
    SKIP_SESSION = 'skip-session'


class FencedBlock:
    """Selected fields from commonmark node plus new field role."""
    def __init__(self, node: commonmark.node.Node) -> None:
        """Extract fields from commonmark fenced code block node."""
        self.type = node.info
        self.line = node.sourcepos[0][0] + 1
        self.role = Role.UNKNOWN
        self.contents = node.literal
        self.output = None    # type: Optional['FencedBlock']
        self.skip_reasons = list()    # type: List[str]

    def __str__(self) -> str:
        return 'FencedBlock(role={}, line={})'.format(
            self.role.value, self.line)

    def set(self, role: Role) -> None:
        """Set the role for the fenced code block in subsequent testing."""
        self.role = role

    def set_link_to_output(self, fenced_block: 'FencedBlock') -> None:
        """Save a reference to the code block's output block."""
        assert self.role == Role.CODE, 'only allowed to be code'
        assert fenced_block.role == Role.OUTPUT, 'only allowed to be output'
        self.output = fenced_block

    def skip(self, reason: str) -> None:
        """Skip an already designated code block. Re-skip is OK."""
        if self.role == Role.CODE:
            self.set(Role.SKIP_CODE)
            if self.output:
                self.output.set(Role.SKIP_OUTPUT)
        elif self.role == Role.SESSION:
            self.set(Role.SKIP_SESSION)
        else:
            is_skipped = any(
                [self.role == Role.SKIP_CODE,
                 self.role == Role.SKIP_SESSION])
            assert is_skipped, 'cannot skip this Role {}'.format(self.role)
        self.skip_reasons.append(reason)


Args = namedtuple(
    'Args',
    [
        'markdown_file',
        'outfile',
        'skips',
        'is_report',
        'fail_nocode'
    ]
)
"""Command line arguments with some renames."""


@click.command()
@click.argument(
    'markdown_file',
    nargs=1,
    type=click.Path(
        exists=True,
        dir_okay=False,
        allow_dash=True,    # type: ignore
    )
)
@click.option(
    '--outfile',
    nargs=1,
    help=(
        'Write generated test case file to path TEXT. "-"'
        ' writes to stdout.'
    )
)
@click.option(
    '-s', '--skip',
    multiple=True,
    help=(
        'Any Python code or interactive session block that contains'
        ' the substring TEXT is not tested.'
        ' More than one --skip TEXT is ok.'
        ' Double quote if TEXT contains spaces.'
        ' For example --skip="python 3.7" will skip every Python block that'
        ' contains the substring "python 3.7".'
        ' If TEXT is one of the 3 capitalized strings FIRST SECOND LAST'
        ' the first, second, or last Python block in the'
        ' Markdown file is skipped.'
        ' The fenced code block info string is not searched.'
    )
)
@click.option(
    '--report',
    is_flag=True,
    help='Show how the Markdown fenced code blocks are used.'
)
@click.option(
    '--fail-nocode',
    is_flag=True,
    help=(
        'This option sets behavior when the Markdown file has no Python'
        ' fenced code blocks or interactive session blocks'
        ' or if all such blocks are skipped.'
        ' When this option is present the generated pytest file'
        ' has a test function called test_nothing_fails() that'
        ' will raise an assertion.'
        ' If this option is not present the generated pytest file'
        ' has test_nothing_passes() which will never fail.'
    )
)
@click.version_option()
# Note- docstring for entry point shows up in click's usage text.
def entry_point(markdown_file, outfile, skip, report, fail_nocode):
    args = Args(
        markdown_file=markdown_file,
        outfile=outfile,
        skips=skip,
        is_report=report,
        fail_nocode=fail_nocode,
    )

    # Find markdown blocks and pair up code and output blocks.
    with click.open_file(args.markdown_file, encoding='utf-8') as fp:
        blocks = convert_nodes(tool.fenced_block_nodes(fp))
    identify_code_and_output_blocks(blocks)
    apply_skips(args, blocks)
    if args.is_report:
        print_report(args, blocks)

    # build test cases and write to the --outfile path
    if args.outfile:
        test_case_string = build_test_cases(args, blocks)
        with click.open_file(args.outfile, 'w', encoding='utf-8') as ofp:
            ofp.write(test_case_string)


def convert_nodes(nodes: List[commonmark.node.Node]) -> List[FencedBlock]:
    """Create FencedBlock objects from commonmark fenced code block nodes."""
    blocks = []
    for node in nodes:
        blocks.append(FencedBlock(node))
    return blocks


PYTHON_FLAVORS = ['python', 'py3', 'python3']
"""Python fenced code blocks info string will start with one of these."""


def identify_code_and_output_blocks(blocks: List[FencedBlock]) -> None:
    """
    Designate which blocks are Python or session and guess which are output.

    The block.type is a copy of the Markdown fenced code block info_string.
    This string may start with the language intended for syntax coloring.
    A block is an output block if it has an empty markdown info field
    and follows a designated python code block.

    A block is a session block if the info_string starts with 'py'
    and the first line of the block starts with the session prompt '>>> '.
    """
    for block in blocks:
        for flavor in PYTHON_FLAVORS:
            if block.type.startswith(flavor):
                block.set(Role.CODE)
        if block.contents.startswith('>>> ') and block.type.startswith('py'):
            block.set(Role.SESSION)

    # When we find an output block we update the preceding
    # code block with a link to it.
    previous_block = None
    for block in blocks:
        if previous_block is not None:
            if not block.type and previous_block.role == Role.CODE:
                block.set(Role.OUTPUT)
                previous_block.set_link_to_output(block)
        previous_block = block
    # If we didn't find an output block for a code block
    # it can still be run, but there will be no comparison
    # to expected output.  If assertions are needed, they can
    # be added to the code block.


def apply_skips(args: Args, blocks: List[FencedBlock]) -> None:
    """Designate Python code/session blocks that are exempt from testing."""
    skip_candidates = []     # type: List[FencedBlock]
    for b in blocks:
        if b.role in [Role.CODE, Role.SESSION]:
            skip_candidates.append(b)

    # Skip blocks identified by patterns 'FIRST', 'SECOND', 'LAST'
    if skip_candidates:
        apply_special_skips(skip_candidates, args.skips)

    # Skip blocks identified by pattern matches.
    # Try to find each skip pattern in each block.
    # If there is a match, skip the block.  Blocks can
    # be skipped more than once.
    for block in skip_candidates:
        for pattern in args.skips:
            if block.contents.find(pattern) > -1:
                block.skip(pattern)


def apply_special_skips(blocks: List[FencedBlock], skips: List[str]) -> None:
    """Skip blocks identified by patterns 'FIRST', 'SECOND', 'LAST'"""
    for pattern in skips:
        index = None
        if pattern == 'FIRST':
            index = 0
        elif pattern == 'LAST':
            index = -1
        elif pattern == 'SECOND' and len(blocks) > 1:
            index = 1
        if index is not None:
            blocks[index].skip(pattern)


def print_report(args: Args, blocks: List[FencedBlock]) -> None:
    """Print Markdown fenced block report and skips report."""
    report = []
    filename = click.format_filename(args.markdown_file)
    title1 = filename + ' fenced blocks'
    text1 = fenced_block_report(blocks, title=title1)
    report.append(text1)

    roles = [b.role.name for b in blocks]
    counts = Counter(roles)

    number_of_test_cases = counts['CODE'] + counts['SESSION']
    report.append('{} test cases'.format(number_of_test_cases))
    if counts['SKIP_CODE'] > 0:
        report.append('{} skipped code blocks'.format(
            counts['SKIP_CODE']
        ))
    if counts['SKIP_SESSION'] > 0:
        report.append('{} skipped interactive session blocks'.format(
            counts['SKIP_SESSION']
        ))

    num_missing_output = counts['CODE'] - counts['OUTPUT']
    report.append(
        '{} code blocks missing an output block'.format(
            num_missing_output
        )
    )

    if args.skips:
        report.append('')
        title2 = 'skip pattern matches (blank means no match)'
        text2 = skips_report(args.skips, blocks, title=title2)
        report.append(text2)
    print('\n'.join(report))


def fenced_block_report(blocks: List[FencedBlock], title: str = '') -> str:
    """Generate text report about the input file fenced code blocks."""
    table = monotable.MonoTable()
    table.max_cell_height = 7
    table.more_marker = '...'
    cell_grid = []
    for block in blocks:
        if block.role in [Role.SKIP_CODE, Role.SKIP_SESSION]:
            quoted_skips = [r.join(['"', '"']) for r in block.skip_reasons]
            skips = '\n'.join(quoted_skips)
        else:
            skips = ''
        cell_grid.append([block.type, block.line, block.role.value, skips])
    headings = [
        'block\ntype', 'line\nnumber', 'test\nrole',
        'skip pattern/reason\nquoted and one per line']
    formats = ['', '', '', '(width=30)']
    text = table.table(headings, formats, cell_grid, title)    # type: str
    return text


def skips_report(
        skips: List[str], blocks: List[FencedBlock], title: str = '') -> str:
    """Generate text report about the disposition of --skip options."""
    # Blocks with role OUTPUT and SKIP_OUTPUT will always have an
    # empty skip_reasons list even if the linking code block is skipped.
    table = monotable.MonoTable()
    table.max_cell_height = 5
    table.more_marker = '...'
    cell_grid = []
    for skip in skips:
        code_lines = []
        for block in blocks:
            if skip in block.skip_reasons:
                code_lines.append(str(block.line))

        cell_grid.append([skip, ', '.join(code_lines)])
    headings = ['skip pattern', 'matching code block line number(s)']
    formats = ['', '(width=36;wrap)']
    text = table.table(headings, formats, cell_grid, title)    # type: str
    return text


def test_nothing_fails() -> None:
    """Fail if no Python code blocks or sessions were processed."""
    assert False, 'nothing to test'


def test_nothing_passes() -> None:
    """Succeed  if no Python code blocks or sessions were processed."""
    # nothing to test
    pass


_ASSERTION_MESSAGE = 'zero length {} block at line {}'


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""
    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = 'pytest file built from {}'.format(markdown_path)
    builder = print_capture.PytestFile(docstring_text)
    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            code_identifier = 'code_' + str(block.line)
            output_identifier = ''
            code = block.contents
            assert code, _ASSERTION_MESSAGE.format('code', block.line)

            output_block = block.output
            if output_block:
                output_identifier = '_output_' + str(output_block.line)
                expected_output = output_block.contents
                assert expected_output, _ASSERTION_MESSAGE.format(
                    'expected output', block.line)
            else:
                expected_output = ''
            identifier = code_identifier + output_identifier
            builder.add_test_case(identifier, code, expected_output)
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            assert session, _ASSERTION_MESSAGE.format('session', block.line)
            builder.add_interactive_session(str(block.line), session)
            number_of_test_cases += 1

    if number_of_test_cases == 0:
        if args.fail_nocode:
            test_function = inspect.getsource(test_nothing_fails)
        else:
            test_function = inspect.getsource(test_nothing_passes)
        builder.add_source(test_function)
    return str(builder)
