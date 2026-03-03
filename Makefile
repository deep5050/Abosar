# Variables
PYTHON = python3
PIP = pip3

# Default target
.PHONY: all
all: crawl-all update-all

# Update target (README and HTML Generation)
.PHONY: update-all
update-all: readme html

# Help target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make crawl             - Run standard crawlers (Rabibasariya and Onno Alo)"
	@echo "  make crawl-premium     - Fetch premium stories and bypass paywalls"
	@echo "  make crawl-all         - Run all crawlers (standard + premium)"
	@echo "  make readme            - Generate README.md from story lists"
	@echo "  make html              - Generate index.html and story pages"
	@echo "  make install           - Install dependencies from requirements file"
	@echo "  make clean             - Remove __pycache__ and temporary files"
	@echo "  make all               - Run standard crawl, readme, and html"
	@echo "  make bot               - Start the Telegram bot"

# Installation
.PHONY: install
install:
	$(PIP) install -r requirements

# Crawling targets
.PHONY: crawl
crawl: crawl-rabibasariya crawl-onnoalo

.PHONY: crawl-rabibasariya
crawl-rabibasariya:
	$(PYTHON) rabibasariya.py

.PHONY: crawl-onnoalo
crawl-onnoalo:
	@if [ -f url ] && [ -s url ]; then \
		$(PYTHON) onnoalo.py; \
	else \
		echo "Error: 'url' file is empty or not found. Please add a Prothom Alo story URL to 'url' file."; \
	fi

.PHONY: crawl-premium
crawl-premium:
	$(PYTHON) premium_story_link_fetcher.py
	$(PYTHON) scraper_bypass_paywall.py
	$(PYTHON) premium_stories_readme_generator.py

.PHONY: crawl-all
crawl-all: crawl-rabibasariya crawl-onnoalo crawl-premium

# README generation
.PHONY: readme
readme:
	$(PYTHON) readme-generator.py

# HTML generation
.PHONY: html
html:
	$(PYTHON) generate_index.py

# Bot
.PHONY: bot
bot:
	$(PYTHON) telegram-bot.py

# Utilities
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f output_file.txt scraped_history.txt premium_stories_url
