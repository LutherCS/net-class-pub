# net-class-pub

CS430 public repository

## Set up

1. Install `uv`
   - `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Create an environment and install dependencies
   - `uv sync`
3. Activate the environment
    - `source .venv/bin/activate`
4. Implement project *hello*
   - `vi src/projects/hello/server.py`
   - `vi src/projects/hello/client.py`
5. Test project *hello*
   - `pytest tests/projects/hello`

## References

- [uv](https://docs.astral.sh/uv/)
- [pytest documentation](https://docs.pytest.org/en/stable/)
