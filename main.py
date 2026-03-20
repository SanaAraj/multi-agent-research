import argparse
from graph import run_research
from agents import set_mock_mode
from tools import web_search


def main():
    parser = argparse.ArgumentParser(description="Multi-agent research system")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM responses")
    args = parser.parse_args()

    set_mock_mode(args.mock)

    print(f"Researching: {args.topic}\n")
    report = run_research(args.topic, search_func=web_search)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
