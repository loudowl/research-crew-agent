#!/usr/bin/env python3
"""
research-crew-agent
-------------------
A three-agent CrewAI pipeline that researches any topic and produces
a structured markdown brief.

Usage:
    python main.py "edge AI inference in 2026"
    python main.py "the state of open-source LLM fine-tuning" --output my_report.md
    python main.py  # interactive prompt
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from crew import run  # noqa: E402 — import after env load


def parse_args():
    parser = argparse.ArgumentParser(
        description="Research any topic with a three-agent AI crew.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "topic",
        nargs="*",
        help="The topic to research (wrap in quotes if it contains spaces)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="report.md",
        help="Output file path for the markdown report (default: report.md)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Resolve topic from args or interactive prompt
    if args.topic:
        topic = " ".join(args.topic)
    else:
        topic = input("Enter research topic: ").strip()

    if not topic:
        print("Error: please provide a topic.")
        sys.exit(1)

    output_path = args.output

    print(f"\n🔍 Launching research crew")
    print(f"   Topic  : {topic}")
    print(f"   Output : {output_path}")
    print("=" * 60 + "\n")

    try:
        result = run(topic=topic, output_path=output_path)
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(f"✅  Report saved to: {Path(output_path).resolve()}")
    print("=" * 60 + "\n")
    print(result)


if __name__ == "__main__":
    main()
