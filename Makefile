# Makefile for Poetry environment management

.PHONY: install shell remove clean info add remove-lib

# Install dependencies and create a virtual environment
install:
	poetry install

# Activate the Poetry shell
shell:
	poetry run $$SHELL

# Remove the current virtual environment
remove:
	poetry env remove $$(poetry env list --full-path)

# Completely clean and reinstall the virtual environment and dependencies
clean: remove install

# Display information about the current Poetry virtual environment
info:
	poetry env info

# Add a new library (usage: make add package=your-package)
add:
	poetry add $(package)

# Remove an existing library (usage: make remove-lib package=your-package)
remove-lib:
	poetry remove $(package)