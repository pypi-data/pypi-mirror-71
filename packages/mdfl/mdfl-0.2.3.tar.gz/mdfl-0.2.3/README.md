# PyMDFL
A command-line application to generate data packs based on [CRISPYrice](https://github.com/CRISPYricePC/MDFL-Spec/blob/master/spec.md)'s MDFL specification.

## Installation
Install with pip: `python -m pip install mdfl`

If pip doesn't add the package to PATH correctly, you can start the program with `python -m mdfl`.

## Usage
`mdfl --help` will output usage information:
```
PyMDFL: A command-line tool for parsing MDFL and generating Data Packs.

Usage:
    mdfl <script> [--output=<path>]
    mdfl <script> [--tree]
    mdfl -h | --help
    mdfl -V | --version

Options:
    -h --help        Show this screen.
    -V --version     Show version.
    --output=<path>  Output path for the datapack.
    --tree           Print a syntax tree without compiling.
```

The `<script>` argument specifies a file that conforms to the MDFL spec. For example, given a file `gems.mdfl`:
```
namespace diamonds {
  // Namespace for obtaining diamonds.

  fun get {
    // Give the caller a diamond.
    give @s minecraft:diamond;
  }
}

namespace emeralds {
  // Namespace for obtaining emeralds.

  fun get {
    // Give the caller an emerald.
    give @s minecraft:emerald;
  }
}
```
Run `mdfl gems.mdfl` and enter a description for your data pack.
```
$ mdfl gems.mdfl
Description of gems: All your gems are belong to @s
```
This will generate a zip file `gems.zip` with the following structure:
```
├── data
│  ├── emeralds
│  │  └── functions
│  │     └── get.mcfunction
│  └── diamonds
│     └── functions
│        └── get.mcfunction
└── pack.mcmeta
```
