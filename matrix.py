import random
import shutil
import time


CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*+-"


def main():
    width, height = shutil.get_terminal_size((80, 24))
    drops = [random.randint(-height, 0) for _ in range(width)]

    print("\033[2J\033[?25l", end="", flush=True)
    try:
        while True:
            width, height = shutil.get_terminal_size((80, 24))
            drops = (drops + [random.randint(-height, 0) for _ in range(width)])[:width]
            frame = [[" " for _ in range(width)] for _ in range(height)]

            for x, head in enumerate(drops):
                for tail in range(random.randint(5, 15)):
                    y = head - tail
                    if 0 <= y < height:
                        frame[y][x] = random.choice(CHARS)
                drops[x] = head + random.choice((0, 1, 1, 1))
                if drops[x] - 15 > height:
                    drops[x] = random.randint(-height, 0)

            print("\033[H\033[32m" + "\n".join("".join(row) for row in frame), flush=True)
            time.sleep(0.06)
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[0m\033[?25h\033[2J", end="", flush=True)


if __name__ == "__main__":
    main()
