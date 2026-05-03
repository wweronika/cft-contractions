import argparse
from pathlib import Path
from itertools import product

from entropy_graph_2 import EntropyGraph2


def read_pairing_file(path):
    path = Path(path)

    edges = []
    for line in path.read_text().splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        edges.append(line)

    return edges


def default_outdir(n, pairing_path):
    pairing_path = Path(pairing_path)
    stem = pairing_path.stem
    return Path(f"output_n_{n}_{stem}")


def draw_pairing_cmd(args):
    n = args.n
    pairing_path = Path(args.pairing)
    outdir = Path(args.outdir) if args.outdir else default_outdir(n, pairing_path)

    outdir.mkdir(parents=True, exist_ok=True)

    edges_to_cut = read_pairing_file(pairing_path)

    g = EntropyGraph2(n)
    g.draw_with_highlighted_edges(
        edges_to_cut,
        show_names=args.show_names,
        title=f"n_{n}_{pairing_path.stem}",
        outdir=outdir,
    )


def run_single_channel_cmd(args):
    n = args.n
    pairing_path = Path(args.pairing)
    outdir = Path(args.outdir) if args.outdir else default_outdir(n, pairing_path)

    outdir.mkdir(parents=True, exist_ok=True)

    edges_to_cut = read_pairing_file(pairing_path)
    channel = args.channel

    if len(channel) != len(edges_to_cut):
        raise ValueError(
            f"Channel string has length {len(channel)}, "
            f"but pairing has {len(edges_to_cut)} edges."
        )

    if any(c not in {"s", "t"} for c in channel):
        raise ValueError("Channel string must contain only 's' and 't'.")

    g = EntropyGraph2(n)
    g.cut_edges(edges_to_cut, channel)

    counts = g.count_components()

    print(f"channel: {channel}")
    print(f"n_loops: {counts['n_loops']}")
    print(f"n_lines: {counts['n_lines']}")
    print(f"n_other: {counts['n_other']}")

    g.draw(
        show_names=args.show_names,
        title=channel,
        outdir=outdir,
    )


def run_all_channels_cmd(args):
    n = args.n
    pairing_path = Path(args.pairing)
    outdir = Path(args.outdir) if args.outdir else default_outdir(n, pairing_path)

    outdir.mkdir(parents=True, exist_ok=True)

    edges_to_cut = read_pairing_file(pairing_path)

    if args.draw_pairing:
        g0 = EntropyGraph2(n)
        g0.draw_with_highlighted_edges(
            edges_to_cut,
            show_names=args.show_names,
            title=f"n_{n}_before_cutting",
            outdir=outdir,
        )

    log_path = outdir / "log.txt"

    with log_path.open("w") as log:
        log.write(f"n = {n}\n")
        log.write(f"pairing = {pairing_path}\n")
        log.write(f"n_edges = {len(edges_to_cut)}\n\n")
        log.write("channel,n_loops,n_lines,n_other\n")

        for channel_tuple in product(["s", "t"], repeat=len(edges_to_cut)):
            channel = "".join(channel_tuple)

            g = EntropyGraph2(n)
            g.cut_edges(edges_to_cut, channel)

            counts = g.count_components()

            log.write(
                f"{channel},"
                f"{counts['n_loops']},"
                f"{counts['n_lines']},"
                f"{counts['n_other']}\n"
            )

            g.draw(
                show_names=args.show_names,
                title=channel,
                outdir=outdir,
            )

    print(f"Wrote results to {outdir}")
    print(f"Wrote log to {log_path}")


def str_to_bool(x):
    if isinstance(x, bool):
        return x

    x = x.lower()

    if x in {"true", "1", "yes", "y"}:
        return True

    if x in {"false", "0", "no", "n"}:
        return False

    raise argparse.ArgumentTypeError("Expected true or false.")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Entropy graph pairing/channel CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # draw_pairing
    p = subparsers.add_parser("draw_pairing")
    p.add_argument("--n", "-n", type=int, required=True)
    p.add_argument("--pairing", type=str, required=True)
    p.add_argument("--outdir", type=str, default=None)
    p.add_argument("--show-names", action="store_true")
    p.set_defaults(func=draw_pairing_cmd)

    # run_all_channels
    p = subparsers.add_parser("run_all_channels")
    p.add_argument("--n", "-n", type=int, required=True)
    p.add_argument("--pairing", type=str, required=True)
    p.add_argument("--draw-pairing", type=str_to_bool, default=True)
    p.add_argument("--outdir", type=str, default=None)
    p.add_argument("--show-names", action="store_true")
    p.set_defaults(func=run_all_channels_cmd)

    # run_single_channel
    p = subparsers.add_parser("run_single_channel")
    p.add_argument("--n", "-n", type=int, required=True)
    p.add_argument("--pairing", type=str, required=True)
    p.add_argument("--channel", type=str, required=True)
    p.add_argument("--outdir", type=str, default=None)
    p.add_argument("--show-names", action="store_true")
    p.set_defaults(func=run_single_channel_cmd)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()