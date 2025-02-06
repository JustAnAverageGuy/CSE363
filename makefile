# Makefile for converting Markdown files to PDF

# List of Markdown files
MD_FILES := $(wildcard *.md)

# Corresponding PDF files
PDF_FILES := $(patsubst %.md, processed-md/%.pdf, $(MD_FILES))

# Default target
all: $(PDF_FILES)

# Rule to convert .md to .pdf
processed-md/%.pdf: %.md
	@mkdir -p processed-md
	pandoc $< -o $@

# Clean up generated PDF files
clean:
	rm -rf processed-md/*.pdf

.PHONY: all clean
