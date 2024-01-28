" Disable compatibility with vi which can cause unexpected issues.
set nocompatible

" Enable type file detection. Vim will be able to try to detect the type of file in use.
filetype on

" Enable plugins and load plugin for the detected file type.
filetype plugin on

" Load an indent file for the detected file type.
filetype indent on

" Turn syntax highlighting on.
syntax on

" Add numbers to each line on the left-hand side.
"set number
:set number

:augroup numbertoggle
:  autocmd!
:  autocmd BufEnter,FocusGained,InsertLeave,WinEnter * if &nu && mode() != "i" | set rnu   | endif
:  autocmd BufLeave,FocusLost,InsertEnter,WinLeave   * if &nu                  | set nornu | endif
:augroup END



" Highlight cursor line underneath the cursor horizontally.
set cursorline

" Highlight cursor line underneath the cursor vertically.
"set cursorcolumn

" Set shift width to 4 spaces.
" set shiftwidth=4

" Set tab width to 4 columns.
" set tabstop=4

" Use space characters instead of tabs.
set expandtab

" Do not save backup files.
"set nobackup

" Do not let cursor scroll below or above N number of lines when scrolling.
"set scrolloff=10

" Do not wrap lines. Allow long lines to extend as far as the line goes.
"set nowrap

" While searching though a file incrementally highlight matching characters as you type.
set incsearch

" Ignore capital letters during search.
"set ignorecase

" Override the ignorecase option if searching for capital letters.
" This will allow you to search specifically for capital letters.
set smartcase

" Show partial command you type in the last line of the screen.
" set showcmd

" Show the mode you are on the last line.
set showmode

" Show matching words during a search.
set showmatch

" Use highlighting when doing a search.
set hlsearch

" Set the commands to save in history default number is 20.
set history=1000


set t_Co=256
"colorscheme atom-dark-256

set foldmethod=indent

set foldlevel=99

"for python
au BufNewFile, BufRead *.py
	\ set tabstop=4
	\ set softtabstop=4
	\ set shiftwidth=79
	\ set autoindent
	\ set fileformat=unix
let g:ale_linters = {'pytho': ['flake8']}


" Autopep8
autocmd FileType python noremap <buffer> <F8> :call Autopep8()<CR>
let g:autopep8_disable_show_diff=1


"Syntastic
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

let g:syntastic_python_checkers = ['python', 'flake8', 'pylint', 'doctest']
let g:syntastic_aggregate_errors = 1
let g:syntastic_python_pylint_args = "--disable C0111 --max-nested-blocks 3"

