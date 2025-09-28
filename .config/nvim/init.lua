vim.g.mapleader = ' '
vim.g.maplocalleader = ' '

vim.g.have_nerd_font = true

vim.o.shiftwidth = 4
vim.o.softtabstop = -1 -- same as shiftwidth

vim.o.number = true
vim.o.relativenumber = true

vim.o.mouse = 'a'

vim.o.showmode = false -- already in the status line

vim.schedule(function()
	vim.o.clipboard = 'unnamedplus'
end)
