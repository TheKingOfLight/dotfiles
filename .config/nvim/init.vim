set             nocompatible            " Disable compatibility with vi which can cause unexpected issues.

filetype        on                      " Enable type file detection. Vim will be able to try to detect the type of file in use.
filetype        plugin on               " Enable plugins and load plugin for the detected file type.
filetype        indent on               " Load an indent file for the detected file type.

syntax          on                      " Turn syntax highlighting on.

:set            number                  " Add numbers to each line on the left-hand side.
:augroup numbertoggle                   " Swich numbering based on the mode
:  autocmd!
:  autocmd BufEnter,FocusGained,InsertLeave,WinEnter * if &nu && mode() != "i" | set rnu   | endif
:  autocmd BufLeave,FocusLost,InsertEnter,WinLeave   * if &nu                  | set nornu | endif
:augroup END



set             cursorline              " Highlight cursor line underneath the cursor horizontally.
"set            cursorcolumn            " Highlight cursor line underneath the cursor vertically.

" set           shiftwidth=4            " Set shift width to 4 spaces.
" set           tabstop=4               " Set tab width to 4 columns.
set             expandtab               " Use space characters instead of tabs.

"set            nobackup                " Do not save backup files.

"set            scrolloff=10            " Do not let cursor scroll below or above N number of lines when scrolling.
"set            nowrap                  " Do not wrap lines. Allow long lines to extend as far as the line goes.

set             incsearch               " While searching though a file incrementally highlight matching characters as you type.
"set            ignorecase              " Ignore capital letters during search.
set             smartcase               " Override the ignorecase option if searching for capital letters.
set             showmatch               " Show matching words during a search.
set             hlsearch                " Use highlighting when doing a search.

" set           showcmd                 " Show partial command you type in the last line of the screen.
set             showmode                " Show the mode you are on the last line.

set             history=1000            " Set the commands to save in history default number is 20.

set t_Co=256
"colorscheme atom-dark-256

set foldmethod=indent
set foldlevel=99

" Show Diff
command DiffOrig vert new | set buftype=nofile | read ++edit # | 0d_
        \ | diffthis | wincmd p | diffthis


"for python
au BufNewFile, BufRead *.py
	\ set tabstop=4
	\ set softtabstop=4
	\ set shiftwidth=79
	\ set autoindent
	\ set fileformat=unix

:packadd doctest
:packadd jedi-vim

" ALE
let g:ale_completion_enabled = 1
set omnifunc=ale#completion#OmniFunc

" let g:ale_echo_msg_format = '%linter% says %s'
let g:ale_echo_msg_error_str = 'E'
let g:ale_echo_msg_warning_str = 'W'
let g:ale_echo_msg_format = '[%linter%] %s [%severity%]'

let g:ale_linters = {
\   'python': ['bandit', 'cspell', 'flake8', 'jedils', 'prospector', 'pyflakes', 'pylint', 'pyre', 'refurb', 'ruff', 'vulture'],
\}
" removed mypy
let g:ale_fixers = {
\   '*': ['remove_trailing_lines', 'trim_whitespace'],
\   'python': ['add_blank_lines_for_python_control_statements',
\               'autopep8', 'isort'],
\}
" let g:ale_fixers = ['remove_trailing_lines', 'trim_whitespace']
" let g:ale_fixers = {'python': ['add_blank_lines_for_python_control_statements', 'autopep8']}
let g:ale_python_flake8_options = 'ignore=E501'
let g:ale_python_pylint_options = '--disable=line-too-long'

nmap <silent> <C-k> <Plug>(ale_previous_wrap)
nmap <silent> <C-j> <Plug>(ale_next_wrap)

let g:ale_fix_on_save = 1



" Vim-Test
"let test#strategy = "neovim"
"let test#python#runner = 'pyunit'
" Runners available are 'pytest', 'nose', 'nose2', 'djangotest', 'djangonose', 'mamba', and Python's built-in unittest as 'pyunit'
"
"let test#strategy = "neovim"
"let test#python#runner = 'pytest'
"let test#pytest#options = "--doctest-modules"
