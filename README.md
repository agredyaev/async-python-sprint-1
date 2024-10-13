# Weather Data Analysis
[![Linting and Testing](https://github.com/agredyaev/async-python-sprint-1/actions/workflows/app-testing.yml/badge.svg)](https://github.com/agredyaev/async-python-sprint-1/actions/workflows/app-testing.yml)
![Python](https://img.shields.io/badge/python-3.13-blue)
![Pydantic](https://img.shields.io/badge/pydantic-red)
![HTTPX](https://img.shields.io/badge/httpx-green)
![UV](https://img.shields.io/badge/uv-lemon)
![Ruff](https://img.shields.io/badge/ruff-linter-orange)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Project Overview

This project analyzes weather conditions using data from the Yandex Weather API. The task involves retrieving weather data for a list of cities, calculating the average temperature and analyzing precipitation conditions for a specific period within a day.

### Key Features
- **FetchTask**: Fetches weather data from an external API (e.g., YandexWeatherAPI).
- **ExtractTask**: Extracts and validates relevant weather data.
- **TransformTask**: Processes and transforms raw weather data into structured formats.
- **AnalyzeTask**: Analyzes transformed data to compute key metrics like weather scores.
