import curses
import time


def main(screen):
    curses.curs_set(0)
    screen.timeout(80)
    score_left = score_right = 0
    serve_direction = 1

    while max(score_left, score_right) < 5:
        height, width = screen.getmaxyx()
        if width < 30 or height < 12:
            screen.erase()
            screen.addnstr(0, 0, "Powieksz terminal do co najmniej 30x12. Esc konczy.", width - 1)
            if screen.getch() == 27:
                return
            continue

        left_y = right_y = height // 2
        ball_x, ball_y = width // 2, height // 2
        dx, dy = serve_direction, 1
        last_move = time.monotonic()

        while True:
            key = screen.getch()
            if key == 27:
                return
            if key in (ord("w"), ord("W")):
                left_y = max(3, left_y - 1)
            elif key in (ord("s"), ord("S")):
                left_y = min(height - 4, left_y + 1)
            elif key == curses.KEY_UP:
                right_y = max(3, right_y - 1)
            elif key == curses.KEY_DOWN:
                right_y = min(height - 4, right_y + 1)

            if time.monotonic() - last_move < 0.08:
                continue
            last_move = time.monotonic()

            next_x, next_y = ball_x + dx, ball_y + dy
            if next_y <= 1 or next_y >= height - 2:
                dy = -dy
                next_y = ball_y + dy

            if dx < 0 and next_x == 2 and abs(next_y - left_y) <= 1:
                dx = 1
            elif dx > 0 and next_x == width - 3 and abs(next_y - right_y) <= 1:
                dx = -1
            elif next_x < 1:
                score_right += 1
                serve_direction = -1
                break
            elif next_x > width - 2:
                score_left += 1
                serve_direction = 1
                break

            ball_x, ball_y = next_x, next_y

            screen.erase()
            screen.addnstr(0, 2, f"P1 {score_left}  P2 {score_right}  Esc: koniec", width - 4)
            for x in range(width):
                screen.addch(1, x, "-")
                screen.addch(height - 2, x, "-")
            for y in range(1, height - 1):
                screen.addch(y, 0, "|")
                screen.addch(y, width - 1, "|")
            for offset in (-1, 0, 1):
                screen.addch(left_y + offset, 2, "#")
                screen.addch(right_y + offset, width - 3, "#")
            screen.addch(ball_y, ball_x, "o")
            screen.refresh()

    screen.erase()
    winner = "Gracz 1" if score_left == 5 else "Gracz 2"
    message = f"{winner} wygrywa! Nacisnij klawisz."
    screen.addnstr(height // 2, 0, message, width - 1)
    screen.timeout(-1)
    screen.getch()


if __name__ == "__main__":
    curses.wrapper(main)
