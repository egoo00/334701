#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <chrono>
#include <conio.h>

using namespace std;

const int WIDTH = 40;
const int HEIGHT = 40;

enum Direction { UP, DOWN, LEFT, RIGHT };

struct Point {
    int x, y;
};

class Snake {
public:
    Snake() {
        body.push_back({WIDTH / 2, HEIGHT / 2});
        direction = RIGHT;
    }

    void move() {
        Point head = body[0];
        switch (direction) {
            case UP:
                head.y--;
                if (head.y < 0) head.y = HEIGHT - 1;
                break;
            case DOWN:
                head.y++;
                if (head.y >= HEIGHT) head.y = 0;
                break;
            case LEFT:
                head.x--;
                if (head.x < 0) head.x = WIDTH - 1;
                break;
            case RIGHT:
                head.x++;
                if (head.x >= WIDTH) head.x = 0;
                break;
        }

        body.insert(body.begin(), head);
        if (!eating) {
            body.pop_back();
        } else {
            eating = false;
        }
    }

    bool checkCollision() {
        Point head = body[0];
        for (size_t i = 1; i < body.size(); ++i) {
            if (head.x == body[i].x && head.y == body[i].y) {
                return true;
            }
        }
        return false;
    }

    void setDirection(Direction newDirection) {
        if ((newDirection == UP && direction == DOWN) ||
            (newDirection == DOWN && direction == UP) ||
            (newDirection == LEFT && direction == RIGHT) ||
            (newDirection == RIGHT && direction == LEFT)) {
            return;
        }
        direction = newDirection;
    }

    vector<Point> getBody() {
        return body;
    }

    void eat() {
        eating = true;
    }

private:
    vector<Point> body;
    Direction direction;
    bool eating = false;
};

class Food {
public:
    Food() {
        generateFood();
    }

    void generateFood() {
        food.x = rand() % WIDTH;
        food.y = rand() % HEIGHT;
    }

    Point getFood() {
        return food;
    }

private:
    Point food;
};

void draw(const Snake& snake, const Food& food) {
    system("cls");

    vector<Point> snakeBody = snake.getBody();
    Point foodPos = food.getFood();

    for (int i = 0; i < HEIGHT; ++i) {
        for (int j = 0; j < WIDTH; ++j) {
            if (i == foodPos.y && j == foodPos.x) {
                cout << "F";
            } else {
                bool isSnakeBody = false;
                for (const auto& segment : snakeBody) {
                    if (i == segment.y && j == segment.x) {
                        cout << "O";
                        isSnakeBody = true;
                        break;
                    }
                }
                if (!isSnakeBody) {
                    cout << ".";
                }
            }
        }
        cout << endl;
    }
}

int main() {
    srand(time(0));

    Snake snake;
    Food food;

    char input;

    while (true) {
        draw(snake, food);

        if (_kbhit()) {
            input = _getch();
            switch (input) {
                case 'w':
                    snake.setDirection(UP);
                    break;
                case 's':
                    snake.setDirection(DOWN);
                    break;
                case 'a':
                    snake.setDirection(LEFT);
                    break;
                case 'd':
                    snake.setDirection(RIGHT);
                    break;
                case 'q':
                    return 0;
            }
        }

        snake.move();

        if (snake.getBody()[0].x == food.getFood().x && snake.getBody()[0].y == food.getFood().y) {
            snake.eat();
            food.generateFood();
        }

        if (snake.checkCollision()) {
            cout << "Game Over!" << endl;
            return 0;
        }

        this_thread::sleep_for(chrono::milliseconds(100));
    }

    return 0;
}