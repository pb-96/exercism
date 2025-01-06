from typing import Any, List
from pathlib import Path
import re


class Grep:
    def __init__(self, flags: List[str], pattern: str, _files: List[str]) -> None:
        self._files = _files
        self.multiple = len(_files) > 1
        self.files_with_matches = []
        self.current_file = None
        self.x = False
        self.v = False
        self.l = False
        self.n = False
        self.i = False
        self.raw_pattern = pattern

        for flag in flags:
            flag = flag.replace("-", "")
            self.__setattr__(flag, True)

        if self.i:
            self.pattern = re.compile(pattern, re.IGNORECASE)
        else:
            self.pattern = re.compile(pattern)

    def process_n(self, line: str, line_idx: int):
        return f"{line_idx}:{line}"

    def match_pattern(self, line: str, line_no: int):
        matched_tuple = (self.x, self.v)
        return_line = None

        match matched_tuple:
            case (True, True):
                if self.i and self.raw_pattern.lower() != line.lower():
                    return_line = line + "\n"
                elif self.raw_pattern != line:
                    return_line = line + "\n"
            case (True, False):
                if self.i and self.raw_pattern.lower() == line.lower():
                    return_line = line + "\n"
                elif self.raw_pattern == line:
                    return_line = line + "\n"
            case (False, True):
                matched = self.pattern.search(line)
                if matched is None:
                    return_line = line + "\n"
            case (False, False):
                matched = self.pattern.search(line)
                if matched is not None:
                    return_line = line + "\n"

        if return_line and return_line != "\n":
            if self.n:
                return_line = self.process_n(return_line, line_no)
            if self.multiple:
                return f"{self.current_file}:{return_line}"
        return return_line

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        from grep_test import FILE_TEXT

        matches = []
        for _file in self._files:
            curr = []
            self.current_file = _file
            if _file in FILE_TEXT:
                raw_data = FILE_TEXT[_file]
            else:
                raw_data = Path(self._file).read_text()

            for idx, line in enumerate(raw_data.split("\n"), start=1):
                matched = self.match_pattern(line, idx)
                if matched is None:
                    continue
                if matched == "\n":
                    continue
                curr.append(matched)

            if len(curr):
                self.files_with_matches.append(_file + "\n")
                matches.extend(curr)

        if self.l:
            return self.files_with_matches

        return matches


def grep(pattern, flags, files):
    matches = []
    grep_object = Grep(flags=flags, pattern=pattern, _files=files)
    matches.extend(grep_object())
    return "".join(matches)


if __name__ == "__main__":
    l, r = (
        grep("a", "-v", ["iliad.txt", "midsummer-night.txt", "paradise-lost.txt"]),
        "iliad.txt:Achilles sing, O Goddess! Peleus' son;\n"
        "iliad.txt:The noble Chief Achilles from the son\n"
        "midsummer-night.txt:If I refuse to wed Demetrius.\n",
    )
    print(l)
    print(r)
    print(l == r)
