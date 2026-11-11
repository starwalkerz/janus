"""Launch the JANUS API and UI."""

import argparse

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the JANUS trading bot")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8400)
    parser.add_argument("--reload", action="store_true")
    arguments = parser.parse_args()
    uvicorn.run(
        "janus.api:app",
        host=arguments.host,
        port=arguments.port,
        reload=arguments.reload,
    )


if __name__ == "__main__":
    main()