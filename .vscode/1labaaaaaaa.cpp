#include <iostream>
#include <limits>
#include <windows.h>
#include <locale>
#include <conio.h>

using namespace std;

// Инициализация консоли под UTF-8 и русскую локаль
void initConsole() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);
    setlocale(LC_ALL, "ru_RU.UTF-8");
}

// Меню программы с очисткой буфера после ввода
int menu() {
    system("CLS");
    int n;
    cout << "[1] Записать данные в COM2\n"
         << "[2] Прочитать данные из COM1\n"
         << "[3] Изменить паритет в COM1\n"
         << "[4] Изменить паритет в COM2\n"
         << "[5] Показать номера портов и переданных байт\n"
         << "[6] Закрыть COM-порты и выйти\n> ";
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Очистка буфера ввода
    return n;
}

// Пауза до нажатия Enter
void pause() {
    cout << "Нажмите Enter для продолжения...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

// Стандартные параметры порта: 600 бод, 8 бит, без паритета, 1 стоп-бит
void setDefault(HANDLE h) {
    DCB dcb = {0};
    dcb.DCBlength = sizeof(dcb);
    if (!GetCommState(h, &dcb)) return;
    dcb.BaudRate = CBR_600;
    dcb.ByteSize = 8;
    dcb.Parity   = NOPARITY;
    dcb.StopBits = ONESTOPBIT;
    dcb.fBinary  = TRUE;
    dcb.fParity  = FALSE; // Отключена проверка паритета при NOPARITY
    SetCommState(h, &dcb);
}

// Неблокирующее чтение – ReadFile возвращает сразу 0, если буфер пуст
void setReadTimeouts(HANDLE h) {
    COMMTIMEOUTS timeouts = {0};
    timeouts.ReadIntervalTimeout = MAXDWORD;
    timeouts.ReadTotalTimeoutMultiplier = 0;
    timeouts.ReadTotalTimeoutConstant = 0;
    SetCommTimeouts(h, &timeouts);
}

// Смена паритета на выбранном порту
void newParity(HANDLE h) {
    DCB dcb = {0};
    dcb.DCBlength = sizeof(dcb);
    if (!GetCommState(h, &dcb)) {
        cout << "Ошибка GetCommState\n"; pause(); return;
    }

    cout << "Выберите паритет:\n"
         << "[0] NOPARITY  (без паритета)\n"
         << "[1] ODDPARITY (нечётный)\n"
         << "[2] EVENPARITY(чётный)\n> ";
    int c; cin >> c;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    switch (c) {
        case 0:
            dcb.Parity = NOPARITY;
            dcb.fParity = FALSE;
            break;
        case 1:
            dcb.Parity = ODDPARITY;
            dcb.fParity = TRUE;
            break;
        case 2:
            dcb.Parity = EVENPARITY;
            dcb.fParity = TRUE;
            break;
        default:
            cout << "Неверный выбор\n"; pause(); return;
    }

    if (!SetCommState(h, &dcb)) {
        cout << "Ошибка SetCommState\n"; pause(); return;
    }

    cout << "Установлен паритет: "
         << (dcb.Parity == ODDPARITY   ? "ODDPARITY"
             : dcb.Parity == EVENPARITY ? "EVENPARITY"
                                        : "NOPARITY")
         << "\n";
    pause();
}

// Запись фиксированной строки в COM2 и накопление байт
void writeData(HANDLE h, int &bytesSent) {
    const char msg[] = "Hello!!!";
    DWORD w = 0;
    if (!WriteFile(h, msg, sizeof(msg) - 1, &w, NULL)) {
        cout << "Ошибка записи: " << GetLastError() << "\n";
    } else {
        bytesSent += w;
        cout << "Отправлено байт: " << w << "\n";
    }
    pause();
}

// Чтение из COM1 без блокировки и вывод результата
void readData(HANDLE h) {
    char ch;
    DWORD r = 0;
    bool got = false;

    cout << "Принято: ";
    while (ReadFile(h, &ch, 1, &r, NULL) && r > 0) {
        cout << ch;
        got = true;
    }
    if (!got) {
        cout << "<Нет данных>";
    }
    cout << "\n";
    pause();
}

int main() {
    initConsole();

    // Открываем COM1 для чтения и COM2 для записи
    HANDLE hRead  = CreateFileW(L"\\\\.\\COM1", GENERIC_READ,  0, NULL, OPEN_EXISTING, 0, NULL);
    HANDLE hWrite = CreateFileW(L"\\\\.\\COM2", GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hRead == INVALID_HANDLE_VALUE || hWrite == INVALID_HANDLE_VALUE) {
        cout << "Не удалось открыть COM-порты\n";
        return 1;
    }

    // Настройка портов
    setDefault(hRead);
    setReadTimeouts(hRead);
    setDefault(hWrite);

    int bytesSent = 0;
    while (true) {
        switch (menu()) {
            case 1: writeData(hWrite, bytesSent); break;
            case 2: readData(hRead);              break;
            case 3: newParity(hRead);             break;
            case 4: newParity(hWrite);            break;
            case 5:
                cout << "COM1 (читает): COM2 (пишет)\n"
                     << "Порт чтения: COM1\n"
                     << "Порт записи: COM2\n"
                     << "Всего отправлено байт: " << bytesSent << "\n";
                pause();
                break;
            case 6:
                CloseHandle(hRead);
                CloseHandle(hWrite);
                return 0;
            default:
                cout << "Неверный пункт меню\n";
                pause();
        }
    }
}
