// C++ rewrite of menu.py and sndctl.py using pigpio
// Dependencies: libvlc, taglib, FreeType, ST7789 framebuffer driver, pigpio

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stack>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>
#include <vlc/vlc.h>
#include <taglib/fileref.h>
#include <taglib/tag.h>
#include <png.h> // or stb_image if preferred
#include <pigpio.h>
#include "st7789.h" // assumed you have a driver for this

// --- Constants ---
const std::string SONG_PATH = "library/Music/94_from up on silent hill - Savage Ga$p.mp3";
const int VOLUME = 40;

// --- Globals ---
libvlc_instance_t* vlcInstance = nullptr;
libvlc_media_player_t* player = nullptr;
bool showPlayer = true;

// --- Helpers ---
int kbhit() {
    termios term;
    tcgetattr(0, &term);
    termios term2 = term;
    term2.c_lflag &= ~ICANON;
    tcsetattr(0, TCSANOW, &term2);
    int bytesWaiting;
    ioctl(0, FIONREAD, &bytesWaiting);
    tcsetattr(0, TCSANOW, &term);
    return bytesWaiting;
}

char getInput() {
    if (kbhit()) {
        char ch;
        read(0, &ch, 1);
        return ch;
    }
    return '\0';
}

// --- Audio Player ---
void initPlayer() {
    if (vlcInstance) return;
    const char* args[] = {"--aout=alsa"};
    vlcInstance = libvlc_new(1, args);
    libvlc_media_t* media = libvlc_media_new_path(vlcInstance, SONG_PATH.c_str());
    player = libvlc_media_player_new_from_media(media);
    libvlc_media_release(media);
    libvlc_audio_set_volume(player, VOLUME);
    libvlc_media_player_play(player);
}

void updateMetadata(std::string& title, std::string& artist, std::string& album) {
    TagLib::FileRef f(SONG_PATH.c_str());
    if (!f.isNull() && f.tag()) {
        TagLib::Tag *tag = f.tag();
        title = tag->title().toCString(true);
        artist = tag->artist().toCString(true);
        album = tag->album().toCString(true);
    } else {
        title = "Unknown";
        artist = "Unknown";
        album = "Unknown";
    }
}

// --- UI/Display ---
void drawScreen(const std::string& title, const std::string& album, const std::string& artist) {
    // Replace this with actual ST7789 screen drawing code
    std::cout << "\033[2J\033[1;1H"; // clear terminal
    std::cout << "Now Playing\n";
    std::cout << "Title: " << title << "\n";
    std::cout << "Album: " << album << "\n";
    std::cout << "Artist: " << artist << "\n";

    int elapsed = libvlc_media_player_get_time(player) / 1000;
    int total = libvlc_media_player_get_length(player) / 1000;
    std::cout << "Progress: " << elapsed << "/" << total << " seconds\n";
}

// --- Input Handlers ---
void handleInput(char input) {
    switch (input) {
        case 'r': std::cout << "menu up\n"; break;
        case 'f': std::cout << "menu down\n"; break;
        case 's': std::cout << "select\n"; break;
        case 'w': showPlayer = false; break;
        case 'd': libvlc_media_player_next(player); break;
        case 'x':
            if (libvlc_media_player_is_playing(player))
                libvlc_media_player_pause(player);
            else
                libvlc_media_player_play(player);
            break;
        case 'a': std::cout << "previous\n"; break;
        default: break;
    }
}

// --- Main Loop ---
int main() {
    if (gpioInitialise() < 0) {
        std::cerr << "Failed to initialize pigpio" << std::endl;
        return 1;
    }

    initPlayer();

    while (showPlayer) {
        char input = getInput();
        if (input != '\0') handleInput(input);

        std::string title, artist, album;
        updateMetadata(title, artist, album);
        drawScreen(title, album, artist);

        usleep(125000); // 8 FPS
    }

    libvlc_media_player_stop(player);
    libvlc_media_player_release(player);
    libvlc_release(vlcInstance);
    gpioTerminate();
    return 0;
}
