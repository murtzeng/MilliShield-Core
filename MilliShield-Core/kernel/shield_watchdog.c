#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <signal.h>

#define PID_FILE "/root/MilliShield_Core/.shield_server.pid"
#define SERVICE_CMD "/root/MilliShield_Core/shield_service.sh start"

int is_process_running(pid_t pid) {
    if (pid <= 0) return 0;
    return (kill(pid, 0) == 0);
}

pid_t get_shield_pid() {
    FILE *fp = fopen(PID_FILE, "r");
    if (!fp) return -1;
    pid_t pid = -1;
    fscanf(fp, "%d", &pid);
    fclose(fp);
    return pid;
}

int main() {
    printf("[+] MilliShield Anti-Tamper Watchdog Aktiflesiyor...\n");

    // Daemon
    pid_t pid = fork();
    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);

    umask(0);
    setsid();

    while (1) {
        pid_t current_pid = get_shield_pid();

        // Eğer PID yoksa veya süreç gerçekten ölmüşse DİRİLT
        if (current_pid == -1 || !is_process_running(current_pid)) {
            system(SERVICE_CMD);
            sleep(5); // Tekrar denemek için 5 saniye bekle, döngüye girme
        }

        sleep(3); // Denetim periyodu 3 saniye
    }

    return 0;
}