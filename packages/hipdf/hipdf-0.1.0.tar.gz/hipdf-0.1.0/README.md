# hipdf - pdf highlighter

Highlight the first word of English sentences in PDF file.

## Installation
```commandline
pip install hipdf
```

## Usage

* Basic usage:

```commandline
hipdf <path_to_file>
```

Hipdf will save the highlighted file in the same folder of the original file, with prefix like "[highlighted.{count}][{time}]" 

* Specify an out name:

```commandline
hipdf <path_to_file> -o <out_path>
```

The `out_path` is relative to the current working directory. Examples: `../my docs/highlighted.pdf` or `./highlighted/doc.pdf` 

* Specify a prefix:

```commandline
hipdf <path_to_file> -p <prefix>
```

or with `-o`:

```commandline
hipdf <path_to_file> -o <out_path> -p <prefix>
```

prefix will only affect filename but not file path.
