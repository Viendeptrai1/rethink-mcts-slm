"""
Bytecode Control Flow Graph (CFG) analyzer matching §8.2 of RethinkMCTS spec.
Builds basic blocks from Python 3.11 bytecode via `dis` module.
"""

import dis
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set


@dataclass(frozen=True)
class BytecodeBlock:
    block_id: str
    code_object_name: str
    start_offset: int
    end_offset: int
    line_span: Tuple[int, int]
    source_snippet: str
    target_offsets: Tuple[int, ...] = field(default_factory=tuple)
    is_terminal: bool = False


@dataclass
class CodeCFG:
    blocks: Dict[str, BytecodeBlock] = field(default_factory=dict)
    offset_to_block_id: Dict[tuple[str, int, int], str] = field(default_factory=dict)
    line_to_block_ids: Dict[int, List[str]] = field(default_factory=dict)


import types

def _gather_code_objects(code_obj: types.CodeType) -> List[types.CodeType]:
    res = [code_obj]
    for c in code_obj.co_consts:
        if isinstance(c, types.CodeType):
            res.extend(_gather_code_objects(c))
    return res


def build_cfg_for_code(source_code: str) -> CodeCFG:
    """
    Constructs basic blocks from source code via bytecode dis instructions (§8.2).
    Includes module, functions, and nested code objects.
    """
    top_code_obj = compile(source_code, "<candidate>", "exec")
    lines = source_code.splitlines()

    all_code_objs = _gather_code_objects(top_code_obj)
    cfg = CodeCFG()
    global_block_counter = 0

    for code_obj in all_code_objs:
        instructions = list(dis.get_instructions(code_obj))
        if not instructions:
            continue

        jump_targets: Set[int] = set()
        terminators: Set[int] = set()

        for inst in instructions:
            if inst.is_jump_target:
                jump_targets.add(inst.offset)
            if inst.opcode in dis.hasjrel or inst.opcode in dis.hasjabs or inst.opname in ("RETURN_VALUE", "RETURN_CONST", "RAISE_VARARGS", "RERAISE"):
                terminators.add(inst.offset)
                if (inst.opcode in dis.hasjrel or inst.opcode in dis.hasjabs) and isinstance(inst.argval, int):
                    jump_targets.add(inst.argval)

        boundary_offsets = {0}
        boundary_offsets.update(jump_targets)
        for i, inst in enumerate(instructions[:-1]):
            if inst.offset in terminators:
                boundary_offsets.add(instructions[i + 1].offset)

        sorted_boundaries = sorted(list(boundary_offsets))

        for b_idx, start_off in enumerate(sorted_boundaries):
            end_off = sorted_boundaries[b_idx + 1] if b_idx + 1 < len(sorted_boundaries) else float("inf")
            block_insts = [inst for inst in instructions if start_off <= inst.offset < end_off]
            if not block_insts:
                continue

            global_block_counter += 1
            block_id = f"bb_{global_block_counter}"

            min_line = min((inst.positions.lineno for inst in block_insts if inst.positions and inst.positions.lineno), default=code_obj.co_firstlineno)
            max_line = min_line
            for inst in block_insts:
                if hasattr(inst, "positions") and inst.positions and inst.positions.lineno:
                    max_line = max(max_line, inst.positions.lineno)
                    min_line = min(min_line, inst.positions.lineno)

            snippet_lines = lines[min_line - 1: max_line] if min_line <= len(lines) else []
            snippet = "\n".join(snippet_lines)

            targets = []
            is_term = False
            last_inst = block_insts[-1]
            if last_inst.opname in ("RETURN_VALUE", "RETURN_CONST", "RAISE_VARARGS", "RERAISE"):
                is_term = True
            elif (last_inst.opcode in dis.hasjrel or last_inst.opcode in dis.hasjabs) and isinstance(last_inst.argval, int):
                targets.append(last_inst.argval)

            if not is_term and last_inst.opname not in ("JUMP_FORWARD", "JUMP_BACKWARD", "JUMP_ABSOLUTE", "JUMP_BACKWARD_NO_INTERRUPT"):
                if b_idx + 1 < len(sorted_boundaries):
                    targets.append(sorted_boundaries[b_idx + 1])
            block = BytecodeBlock(
                block_id=block_id,
                code_object_name=code_obj.co_name,
                start_offset=start_off,
                end_offset=block_insts[-1].offset,
                line_span=(min_line, max(min_line, max_line)),
                source_snippet=snippet,
                target_offsets=tuple(targets),
                is_terminal=is_term
            )
            cfg.blocks[block_id] = block

            for inst in block_insts:
                cfg.offset_to_block_id[(code_obj.co_qualname, code_obj.co_firstlineno, inst.offset)] = block_id

            for line_no in range(min_line, max(min_line, max_line) + 1):
                if line_no not in cfg.line_to_block_ids:
                    cfg.line_to_block_ids[line_no] = []
                if block_id not in cfg.line_to_block_ids[line_no]:
                    cfg.line_to_block_ids[line_no].append(block_id)

    return cfg
