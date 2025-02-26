" Basic .vimrc Configuration
" ---------------------

" General Settings
" ---------------
set nocompatible              " Use Vim settings, rather than Vi settings
filetype plugin indent on     " Enable file type detection and do language-dependent indenting
syntax enable                 " Enable syntax highlighting
set encoding=utf-8            " Set default encoding to UTF-8
set hidden                    " Allow buffer switching without saving
set history=1000              " Store lots of :cmdline history
set showcmd                   " Show incomplete commands at the bottom
set showmode                  " Show current mode at the bottom
set gcr=a:blinkon0            " Disable cursor blink
set visualbell                " No sounds
set autoread                  " Reload files changed outside vim
set backspace=indent,eol,start" Make backspace work as expected

" UI Configuration
" ---------------
set number                    " Show line numbers
set relativenumber            " Use relative line numbers
set ruler                     " Show the cursor position
set wrap                      " Wrap lines
set linebreak                 " Break lines at word (requires Wrap lines)
set scrolloff=3               " Keep 3 lines below and above the cursor
set laststatus=2              " Always show status line
set showmatch                 " Show matching brackets when text indicator is over them
set mat=2                     " How many tenths of a second to blink when matching brackets
set wildmenu                  " Visual autocomplete for command menu
set wildmode=list:longest     " Complete files like a shell
set cursorline                " Highlight current line

" Search Settings
" --------------
set incsearch                 " Find the next match as we type the search
set hlsearch                  " Highlight searches by default
set ignorecase                " Ignore case when searching...
set smartcase                 " ...unless you type a capital

" Indentation Settings
" -------------------
set autoindent                " Auto-indent new lines
set smartindent               " Enable smart indentation
set expandtab                 " Use spaces instead of tabs
set smarttab                  " Be smart when using tabs
set shiftwidth=4              " Number of spaces to use for each step of indent
set tabstop=4                 " Number of spaces a tab counts for
set softtabstop=4             " Edit as if tabs are 4 characters wide

" Hook in plugins
source ~/.vim/plugins.vim

" Color and Theme
" --------------
set background=dark           " Use dark background
colorscheme catppuccin_latte  " Set color scheme

" Key Mappings
" -----------
" Map leader to space
let mapleader = "\<Space>"

" Quickly save file with <Leader>w
nnoremap <Leader>w :w<CR>

" Quickly quit with <Leader>q
nnoremap <Leader>q :q<CR>

" Clear search highlighting with <Leader>/
nnoremap <Leader>/ :nohlsearch<CR>

" Move between windows with Ctrl + h/j/k/l
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" File Explorer Mappings
" ---------------------
" Toggle NERDTree with Ctrl+n
nnoremap <C-n> :NERDTreeToggle<CR>
" Find current file in NERDTree
nnoremap <Leader>f :NERDTreeFind<CR>
" Open fuzzy file finder
nnoremap <Leader>p :Files<CR>
" Search in files with Ripgrep
nnoremap <Leader>g :Rg<CR>

" Advanced Settings
" ---------------
" Enable folding based on indentation
set foldmethod=indent
set foldlevelstart=99        " Start with all folds open

" File backups
set nobackup                  " No backup before overwriting file
set noswapfile                " Don't create swapfiles
set noundofile                " Don't keep an undo file

" Set a character limit line at column 80
set colorcolumn=80

" Enable mouse support in all modes
set mouse=a

" Comments for different languages in a different color
highlight Comment ctermfg=grey

" Easy alignment for markdown tables and similar content
if has('autocmd')
  " Auto-resize splits when Vim window is resized
  autocmd VimResized * wincmd =
  
  " Remember last position
  autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif
