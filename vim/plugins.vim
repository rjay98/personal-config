" plugins.vim - Vim Plugin Management
" -----------------------------------

" Initialize vim-plug
call plug#begin('~/.vim/plugged')

" User Interface
Plug 'catppuccin/vim', { 'as': 'catppuccin' } " Catppuccin theme
Plug 'vim-airline/vim-airline'        " Status/tabline
Plug 'vim-airline/vim-airline-themes' " Themes for airline
Plug 'preservim/nerdtree'             " File system explorer

" Development Tools
Plug 'tpope/vim-fugitive'             " Git integration
Plug 'airblade/vim-gitgutter'         " Shows git diff in the sign column
Plug 'dense-analysis/ale'             " Asynchronous Lint Engine
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } } " Fuzzy finder
Plug 'junegunn/fzf.vim'               " Fuzzy finder vim integration

" Editing Enhancements
Plug 'tpope/vim-surround'             " Easily delete, change and add surroundings
Plug 'jiangmiao/auto-pairs'           " Insert or delete brackets, quotes in pair
Plug 'preservim/nerdcommenter'        " Comment functions
Plug 'godlygeek/tabular'              " Text alignment

" Language Support
Plug 'sheerun/vim-polyglot'           " Language pack for vim

" Add your plugins here...

" Initialize plugin system
call plug#end()

" Plugin Settings
" --------------

" NERDTree settings
let g:NERDTreeShowHidden=1
let g:NERDTreeIgnore = ['\\.git$', '\\.DS_Store$', '__pycache__', '\\.pyc$']
let g:NERDTreeDirArrowExpandable = '▸'
let g:NERDTreeDirArrowCollapsible = '▾'
" Close vim if NERDTree is the only window remaining
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif
" Open NERDTree automatically when vim starts up on opening a directory
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists('s:std_in') | execute 'NERDTree' argv()[0] | wincmd p | enew | endif

" Gruvbox theme settings
let g:gruvbox_contrast_dark = 'medium'
let g:gruvbox_italic = 1

" Airline settings
let g:airline_powerline_fonts = 1
let g:airline_theme = 'catppuccin'

" Add your plugin settings here...
