ONESHELL:

.PHONY: env
env:
	@find . -name ".env.example" | while read file; do \
		cp "$$file" "$$(dirname $$file)/.env"; \
	done

.PHONY: sync
sync:
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv venv
	@uv sync --frozen --all-extras

.PHONY: upd_hooks
upd_hooks:
	@pre-commit clean
	@pre-commit install --install-hooks

.PHONY: check
check:
	@git add .
	@pre-commit run
