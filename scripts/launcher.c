#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    // Determine Resources directory
    char resources_path[4096];
    char *exe_path = argv[0];
    char *p = strstr(exe_path, "/MacOS/");
    if (p) {
        size_t pl = p - exe_path;
        memcpy(resources_path, exe_path, pl);
        strcpy(resources_path + pl, "/Resources");
    } else {
        // Fallback
        strcpy(resources_path, "OpenBalance.app/Contents/Resources");
    }

    if (chdir(resources_path) != 0) return 1;

    const char *script = "main_script.py";
    struct stat st;
    if (stat(script, &st) != 0) return 1;

    // Try known Python paths
    const char *pypaths[] = {
        "/usr/local/bin/python3",
        "/opt/homebrew/bin/python3",
        "/usr/bin/python3",
        NULL
    };

    char check[4096];
    for (int i = 0; pypaths[i]; i++) {
        if (access(pypaths[i], X_OK) != 0) continue;
        snprintf(check, sizeof(check), "\"%s\" -c \"import rumps\" 2>/dev/null", pypaths[i]);
        if (system(check) == 0) {
            execl(pypaths[i], pypaths[i], script, (char *)NULL);
            return 1;
        }
    }

    // Fallback
    execl("/usr/bin/python3", "python3", script, (char *)NULL);
    return 1;
}
