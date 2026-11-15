#include <stdio.h>
#include <string.h>

/* Bilerek basit yerel eğitim örneği. Gerçek güvenlik/lisans kontrolü değildir. */
int main(void) {
    char input[64];
    const char demo_key[] = "LOCAL-DEMO-ONLY";

    fputs("Egitim anahtarini girin: ", stdout);
    if (fgets(input, sizeof input, stdin) == NULL) {
        fputs("Girdi okunamadi.\n", stderr);
        return 1;
    }
    input[strcspn(input, "\r\n")] = '\0';

    if (strcmp(input, demo_key) == 0) {
        puts("Demo kabul edildi.");
    } else {
        puts("Demo reddedildi.");
    }
    return 0;
}
