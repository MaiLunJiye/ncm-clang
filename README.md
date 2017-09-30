clang completion integration for
[nvim-completion-manager](https://github.com/roxma/nvim-completion-manager)

If you're using cmake, add `set(CMAKE_EXPORT_COMPILE_COMMANDS, 1)` into
`CMakeLists.txt` so that `compile_commands.json` will be generated.

If your project is not using cmake, store the compile flags into a file named
`.clang_complete`.

This plugin only support completion, for go to declaration support, you could
try , for example, [vim-clang](https://github.com/justmao945/vim-clang)

