#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <conio.h> // For non-buffered keyboard input

using namespace std;

const int WIDTH = 30;
const int HEIGHT = 30;

enum Direction { UP, DOWN, LEFT, RIGHT };

struct Point {
    int x, y;
};

void initialize(vector<Point>& snake, Point& food) {
    snake.clear();
    snake.push_back({WIDTH / 2, HEIGHT / 2}); // Initial snake position
    food.x = rand() % WIDTH;
    food.y = rand() % HEIGHT;
}

void draw(const vector<Point>& snake, const Point& food) {
    system("cls"); // Clear the console

    for (int i = 0; i < HEIGHT; ++i) {
        for (int j = 0; j < WIDTH; ++j) {
            if (i == food.y && j == food.x) {
                cout << "F"; // Food
            } else {
                bool isSnake = false;
                for (const auto& segment : snake) {
                    if (i == segment.y && j == segment.x) {
                        cout << "S"; // Snake
                        isSnake = true;
                        break;
                    }
                }
                if (!isSnake) {
                    cout << "."; // Empty space
                }
            }
        }
        cout << endl;
    }
}

void update(vector<Point>& snake, Point& food, Direction dir, bool& gameOver, bool& ateFood) {
    Point head = snake.front();
    Point newHead = head;

    switch (dir) {
        case UP:
            newHead.y--;
            break;
        case DOWN:
            newHead.y++;
            break;
        case LEFT:
            newHead.x--;
            break;
        case RIGHT:
            newHead.x++;
            break;
    }

    // Check for collisions with walls
    if (newHead.x < 0 || newHead.x >= WIDTH || newHead.y < 0 || newHead.y >= HEIGHT) {
        gameOver = true;
        return;
    }

    // Check for collisions with itself
    for (const auto& segment : snake) {
        if (newHead.x == segment.x && newHead.y == segment.y) {
            gameOver = true;
            return;
        }
    }

    snake.insert(snake.begin(), newHead); // Add new head

    // Check if food was eaten
    if (newHead.x == food.x && newHead.y == food.y) {
        food.x = rand() % WIDTH;
        food.y = rand() % HEIGHT;
        ateFood = true;
    } else {
        snake.pop_back(); // Remove tail if no food eaten
        ateFood = false;
    }
}

int main() {
    srand(time(0));

    vector<Point> snake;
    Point food;
    Direction dir = RIGHT;
    bool gameOver = false;
    bool ateFood = false;

    initialize(snake, food);

    while (!gameOver) {
        draw(snake, food);

        // Get input (non-blocking)
        if (_kbhit()) {
            char input = _getch();
            switch (input) {
                case 'w':
                    dir = UP;
                    break;
                case 's':
                    dir = DOWN;
                    break;
                case 'a':
                    dir = LEFT;
                    break;
                case 'd':
                    dir = RIGHT;
                    break;
                case 'x':
                    gameOver = true; // Exit the game
                    break;
            }
        }

        update(snake, food, dir, gameOver, ateFood);

        // Sleep for a short time to control game speed
        _sleep(100);
    }

    cout << "Game Over!" << endl;

    return 0;
}